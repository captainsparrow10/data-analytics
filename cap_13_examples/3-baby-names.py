"""
US Baby Names 1880-2010 (Section 13.3)

The US Social Security Administration publishes, one file per year, the number of
births for each (name, sex) combination (`yob1880.txt` ... `yob2010.txt`, CSV
with columns name, sex, births). This file reproduces the book's full analysis:
download the per-year files, concatenate them into one DataFrame with a `year`
column, total births by year and sex (with a headless plot), add a per-group
`prop` (fraction of births) column, extract the top-1000 names per year/sex, then
mine naming trends — a few classic names over time (Mary/John/Harry/Marilyn),
rising name DIVERSITY (proportion in the top 1000, and number of names making up
the top 50%), the "last letter" revolution, and names that switched sex (Lesley).

The per-year files are downloaded on demand into a git-ignored `datasets/` cache.
If only SOME years download, the analysis proceeds with whatever is available and
notes the actual range; if none download, every function guards and exits 0.

WHAT THIS FILE COVERS
STEP                        TECHNIQUE
load + concat year files    read_csv per year, add year, pd.concat
births by year and sex      groupby(["year","sex"]).births.sum() + plot
proportion per group        groupby(...).apply add prop column
top-1000 names              sort_values per (year, sex) group, slice [:1000]
naming trends               pivot_table, subplots, cumsum + searchsorted
last-letter revolution      map last letter, pivot, normalize, transpose
sex-switching names         str.contains, isin, normalize within year

Run:
    poetry run python cap_13_examples/3-baby-names.py
"""

import os
import tempfile
import urllib.request
from pathlib import Path

import matplotlib

# HEADLESS: pick the non-interactive Agg backend BEFORE importing pyplot.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

DATA_DIR = os.path.join(os.path.dirname(__file__), "datasets")
RAW_BASE = "https://raw.githubusercontent.com/wesm/pydata-book/3rd-edition/datasets"

# The book uses 1880-2010 inclusive; we attempt that whole range.
YEAR_START = 1880
YEAR_END = 2010


def ensure(rel_path: str, url: str, quiet: bool = False) -> str | None:
    """Return a cached local path, downloading once; None (with a hint) on failure."""
    dest = os.path.join(DATA_DIR, rel_path)
    if os.path.exists(dest):
        return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        urllib.request.urlretrieve(url, dest)  # one-time cached download
        return dest
    except Exception as e:
        if not quiet:
            print(f"[skip] could not fetch {rel_path}: {e}")
            print(f"       download manually from {url} into {DATA_DIR}/")
        return None


# Module-level cache so the four analysis functions share one concat (and one
# download pass) instead of re-fetching 131 files each. (lowercase: mutable state)
_names_cache: pd.DataFrame | None = None
_loaded = False


def _load_names() -> pd.DataFrame | None:
    """
    Download and concatenate the per-year files into a single names DataFrame.

    Proceeds with whatever years are available. Returns None only if NO year
    file could be obtained. Adds a `year` column and a per-group `prop` column.
    """
    global _names_cache, _loaded
    if _loaded:
        return _names_cache

    print(f"[download] fetching baby-name files {YEAR_START}-{YEAR_END} (one-time) ...")
    pieces: list[pd.DataFrame] = []
    available: list[int] = []
    for year in range(YEAR_START, YEAR_END + 1):
        rel = f"babynames/yob{year}.txt"
        # quiet=True: a few missing years should not flood the output; we report
        # the actual coverage afterwards instead.
        path = ensure(rel, f"{RAW_BASE}/{rel}", quiet=True)
        if path is None:
            continue
        frame = pd.read_csv(path, names=["name", "sex", "births"])
        frame["year"] = year
        pieces.append(frame)
        available.append(year)

    if not pieces:
        print("[skip] no baby-name files could be downloaded.")
        print(f"       expected files like {RAW_BASE}/babynames/yob1880.txt")
        _loaded = True
        return None

    # concat stacks the yearly frames by row; ignore_index drops the per-file rows.
    names = pd.concat(pieces, ignore_index=True)
    print(f"loaded {len(available)} year files: {available[0]}-{available[-1]} "
          f"({len(names)} rows)")

    # prop = fraction of that year/sex's births given to each name. The book uses
    # groupby(...).apply(add_prop), but in pandas 3.0 apply with include_groups
    # drops the grouping columns from the result; transform("sum") computes the
    # per-group total aligned to every row without dropping year/sex, so we divide
    # to get prop directly (the same numbers, the idiomatic 3.0 way).
    group_totals = names.groupby(["year", "sex"])["births"].transform("sum")
    names["prop"] = names["births"] / group_totals
    _names_cache = names
    _loaded = True
    return names


def _top1000(names: pd.DataFrame) -> pd.DataFrame:
    """Return the 1000 most common names for each (year, sex) combination."""
    def get_top1000(group: pd.DataFrame) -> pd.DataFrame:
        # __getitem__ slicing is typed broadly; narrow back to a DataFrame.
        result = group.sort_values("births", ascending=False)[:1000]
        assert isinstance(result, pd.DataFrame)
        return result

    # Select all columns back onto the GroupBy so year/sex are kept in each chunk
    # (include_groups=False would drop them, but later pivots need them); the inner
    # function ignores them, sorting only by births.
    grouped = names.groupby(["year", "sex"], group_keys=False)[names.columns]
    top1000 = grouped.apply(get_top1000, include_groups=False)
    assert isinstance(top1000, pd.DataFrame)
    return top1000.reset_index(drop=True)


def explain_births_by_year() -> None:
    """
    Problem: total births by year and sex, and verify the `prop` sanity check.
    Why: a `pivot_table` summing births (index=year, columns=sex) is the natural
    aggregate, plotted as two lines. The per-group `prop` column should sum to 1
    within every (year, sex) group — a quick correctness check on the grouping.
    """
    print("== Total births by year and sex; prop sanity check ==")

    names = _load_names()
    if names is None:
        print("[guard] baby-name data not available; skipping.")
        return

    total_births = names.pivot_table("births", index="year", columns="sex", aggfunc="sum")
    print(total_births.tail())

    with tempfile.TemporaryDirectory() as tmp:
        total_births.plot(title="Total births by sex and year")
        path = Path(tmp) / "total_births.png"
        plt.savefig(path)
        print(f"saved total_births.png -> exists={path.exists()}")
        plt.close("all")

    # prop must sum to 1.0 within each (year, sex) group. (groupby-sum is typed as
    # a broad union; narrow to a Series for .head().)
    prop_sums = names.groupby(["year", "sex"])["prop"].sum()
    assert isinstance(prop_sums, pd.Series)
    print(prop_sums.head())


def explain_naming_trends() -> None:
    """
    Problem: plot the popularity of a few classic names over time.
    Why: from the top-1000 subset, a `pivot_table` summing births (index=year,
    columns=name) yields one time series per name; plotting a handful
    (John/Harry/Mary/Marilyn) as stacked subplots shows their rise and fall.
    """
    print("== Analyzing naming trends: a few classic names over time ==")

    names = _load_names()
    if names is None:
        print("[guard] baby-name data not available; skipping.")
        return

    top1000 = _top1000(names)
    total_births = top1000.pivot_table(
        "births", index="year", columns="name", aggfunc="sum"
    )
    # Only plot names that exist in the available year range.
    wanted = [n for n in ["John", "Harry", "Mary", "Marilyn"] if n in total_births.columns]
    subset = total_births[wanted]
    print(subset.tail())

    with tempfile.TemporaryDirectory() as tmp:
        subset.plot(subplots=True, figsize=(12, 10), title="Number of births per year")
        path = Path(tmp) / "classic_names.png"
        plt.savefig(path)
        print(f"saved classic_names.png -> exists={path.exists()}")
        plt.close("all")


def explain_naming_diversity() -> None:
    """
    Problem: quantify the increase in naming diversity over time.
    Why: two metrics. (1) The proportion of births covered by the top 1000 names,
    by year/sex, declines as parents choose less common names. (2) The number of
    distinct names making up the top 50% of births, computed efficiently with a
    sorted `cumsum` plus `searchsorted(0.5)` rather than a Python loop.
    """
    print("== Measuring the increase in naming diversity ==")

    names = _load_names()
    if names is None:
        print("[guard] baby-name data not available; skipping.")
        return

    top1000 = _top1000(names)

    # Metric 1: share of births in the top 1000, by year and sex.
    table = top1000.pivot_table("prop", index="year", columns="sex", aggfunc="sum")
    with tempfile.TemporaryDirectory() as tmp:
        table.plot(
            title="Sum of table1000.prop by year and sex",
            yticks=np.linspace(0, 1.2, 13),
        )
        path = Path(tmp) / "top1000_prop.png"
        plt.savefig(path)
        print(f"saved top1000_prop.png -> exists={path.exists()}")
        plt.close("all")

    # Metric 2: how many names make up the top 50% of births in a year/sex.
    def get_quantile_count(group: pd.DataFrame, q: float = 0.5) -> int:
        group = group.sort_values("prop", ascending=False)
        # cumsum of the descending props; searchsorted(0.5) = index where the
        # running total crosses 50%; +1 converts 0-based index to a count.
        return int(group["prop"].cumsum().searchsorted(q)) + 1

    diversity = top1000.groupby(["year", "sex"]).apply(
        get_quantile_count, include_groups=False
    )
    diversity = diversity.unstack()
    print(diversity.head())

    with tempfile.TemporaryDirectory() as tmp:
        diversity.plot(title="Number of popular names in top 50%")
        path = Path(tmp) / "diversity.png"
        plt.savefig(path)
        print(f"saved diversity.png -> exists={path.exists()}")
        plt.close("all")


def explain_last_letter_revolution() -> None:
    """
    Problem: show how the distribution of names by FINAL letter changed.
    Why: mapping each name to its last letter and pivoting (index=last letter,
    columns=(sex, year)) reveals a striking shift — boy names ending in "n"
    exploded since the 1960s. Normalizing each column to proportions makes the
    eras comparable; a d/n/y time series for boys shows the trend over time.
    """
    print("== The 'last letter' revolution ==")

    names = _load_names()
    if names is None:
        print("[guard] baby-name data not available; skipping.")
        return

    # Aggregate ALL births (not just top 1000) by final letter, sex, and year.
    last_letters = names["name"].map(lambda x: x[-1])
    last_letters.name = "last_letter"
    table = names.pivot_table(
        "births", index=last_letters, columns=["sex", "year"], aggfunc="sum"
    )

    # Pick representative years that exist in the available range.
    candidate_years = [y for y in (1910, 1960, 2010) if ("M", y) in table.columns]
    if candidate_years:
        subtable = table.reindex(columns=candidate_years, level="year")
        print(subtable.head())
        # Normalize each (sex, year) column to proportions ending in each letter.
        letter_prop = subtable / subtable.sum()
        print(letter_prop.head())

        with tempfile.TemporaryDirectory() as tmp:
            _, axes = plt.subplots(2, 1, figsize=(10, 8))
            letter_prop["M"].plot(kind="bar", rot=0, ax=axes[0], title="Male")
            letter_prop["F"].plot(
                kind="bar", rot=0, ax=axes[1], title="Female", legend=False
            )
            path = Path(tmp) / "last_letter_bars.png"
            plt.savefig(path)
            print(f"saved last_letter_bars.png -> exists={path.exists()}")
            plt.close("all")

    # Boy names ending in d / n / y as a time series (normalize the full table).
    letter_prop = table / table.sum()
    dny_ts = letter_prop.loc[["d", "n", "y"], "M"].T
    print(dny_ts.head())
    with tempfile.TemporaryDirectory() as tmp:
        dny_ts.plot()
        path = Path(tmp) / "dny_trend.png"
        plt.savefig(path)
        print(f"saved dny_trend.png -> exists={path.exists()}")
        plt.close("all")


def explain_sex_switching_names() -> None:
    """
    Problem: find names that flipped from one sex to the other (e.g., Lesley).
    Why: from the top-1000 names, select those starting with "Lesl", filter the
    data to them, then build a (year x sex) table of birth proportions normalized
    within each year. The breakdown shows Lesley/Leslie shifting from a boys' name
    to a girls' name over the century.
    """
    print("== Boy names that became girl names (Lesley) ==")

    names = _load_names()
    if names is None:
        print("[guard] baby-name data not available; skipping.")
        return

    top1000 = _top1000(names)
    all_names = pd.Series(top1000["name"].unique())
    # Boolean indexing is typed as a broad union; narrow to a Series.
    lesley_like = all_names[all_names.str.contains("Lesl")]
    assert isinstance(lesley_like, pd.Series)
    print(lesley_like)

    if len(lesley_like) == 0:
        print("[guard] no 'Lesl*' names in the available year range; skipping plot.")
        return

    filtered = top1000[top1000["name"].isin(lesley_like)]
    print(filtered.groupby("name")["births"].sum())

    # Proportion by sex within each year (rows sum to 1).
    table = filtered.pivot_table("births", index="year", columns="sex", aggfunc="sum")
    table = table.div(table.sum(axis="columns"), axis="index")
    print(table.tail())

    with tempfile.TemporaryDirectory() as tmp:
        # Use the styles the book uses, but only for columns that exist.
        style = {c: ("k-" if c == "M" else "k--") for c in table.columns}
        table.plot(style=style)
        path = Path(tmp) / "lesley_split.png"
        plt.savefig(path)
        print(f"saved lesley_split.png -> exists={path.exists()}")
        plt.close("all")


def main() -> None:
    explain_births_by_year()
    explain_naming_trends()
    explain_naming_diversity()
    explain_last_letter_revolution()
    explain_sex_switching_names()


main()
