"""
Bitly Data from 1.USA.gov (Section 13.1)

In 2011 the URL-shortening service Bitly partnered with the US government site
USA.gov to publish an anonymous feed of users who shortened links ending in
.gov or .mil. Each line of the hourly snapshot is a JSON object describing one
click: the time zone (`tz`), the user agent (`a`), location, and more. This file
reproduces the book's first worked example end to end: load the JSON-lines file,
count the most common time zones first in pure Python (a hand-rolled dict, then
`collections.defaultdict` and `collections.Counter`), then again with pandas
(`value_counts`, `fillna`, a top-10 horizontal bar chart drawn headless with
seaborn), and finally decompose the agent field into Windows vs. non-Windows
users with `np.where`, `groupby`, `unstack`, and a normalized stacked bar plot.

The dataset is downloaded on demand into a git-ignored `datasets/` cache. If the
download fails (offline), every analysis function prints a hint and returns, so
the file still exits 0.

WHAT THIS FILE COVERS
STEP                        TECHNIQUE
load JSON lines             json.loads on each line -> list[dict]
count time zones (Python)   dict, collections.defaultdict, collections.Counter
count time zones (pandas)   DataFrame, Series.value_counts, fillna
top-10 bar chart            seaborn.barplot (headless, saved to a temp dir)
agent field analysis        Series split, value_counts, np.where, groupby/unstack

Run:
    poetry run python cap_13_examples/1-bitly-usagov.py
"""

import json
import os
import tempfile
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

# HEADLESS: pick the non-interactive Agg backend BEFORE importing pyplot.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

# Where downloaded datasets are cached (git-ignored) and the book's raw-data base.
DATA_DIR = os.path.join(os.path.dirname(__file__), "datasets")
RAW_BASE = "https://raw.githubusercontent.com/wesm/pydata-book/3rd-edition/datasets"


def ensure(rel_path: str, url: str) -> str | None:
    """
    Return a local path to the dataset, downloading it once if needed.

    The file is cached under datasets/<rel_path> so it is fetched only the first
    time. On any failure (no network, 404) we return None and print a manual
    hint; callers GUARD on None so the script still exits 0 offline.
    """
    dest = os.path.join(DATA_DIR, rel_path)
    if os.path.exists(dest):
        return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        print(f"[download] fetching {rel_path} (one-time) ...")
        urllib.request.urlretrieve(url, dest)  # one-time cached download
        return dest
    except Exception as e:
        print(f"[skip] could not fetch {rel_path}: {e}")
        print(f"       download manually from {url} into {DATA_DIR}/")
        return None


def _load_records() -> list[dict[str, object]] | None:
    """Load the JSON-lines file into a list of dicts, or None if unavailable."""
    path = ensure("bitly_usagov/example.txt", f"{RAW_BASE}/bitly_usagov/example.txt")
    if path is None:
        return None
    # Each line is a separate JSON object; json.loads parses one record at a time.
    with open(path) as f:
        records = [json.loads(line) for line in f]
    return records


def explain_counting_time_zones_pure_python() -> None:
    """
    Problem: find the most common time zones (the `tz` field) without pandas.
    Why: a plain dict counter shows the mechanics, then the standard library's
    `defaultdict` (auto-initializing values) and `Counter` (with `most_common`)
    do the same thing far more concisely. Not every record HAS a `tz`, so we
    guard the comprehension with `if "tz" in rec` exactly like the book.
    """
    print("== Counting time zones in pure Python ==")

    records = _load_records()
    if records is None:
        print("[guard] bitly data not available; skipping.")
        return

    # Extract the time zones, skipping records that have no tz field at all.
    time_zones = [rec["tz"] for rec in records if "tz" in rec]
    print(time_zones[:10])     # first 10 (some are the empty string = unknown)
    print(len(time_zones))     # total records that carried a tz field

    # A from-scratch counter: a dict mapping each time zone to its count.
    def get_counts(sequence: list[str]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for x in sequence:
            counts[x] = counts.get(x, 0) + 1
        return counts

    # The same with defaultdict(int): missing keys initialize to 0 automatically.
    def get_counts2(sequence: list[str]) -> dict[str, int]:
        counts: dict[str, int] = defaultdict(int)
        for x in sequence:
            counts[x] += 1
        return counts

    # tz values are strings; narrow for the typed counters above.
    tz_strings = [tz for tz in time_zones if isinstance(tz, str)]
    counts = get_counts(tz_strings)
    print(counts["America/New_York"])
    print(get_counts2(tz_strings)["America/New_York"])

    # Top-10 by hand: build (count, tz) pairs, sort, take the last 10.
    def top_counts(count_dict: dict[str, int], n: int = 10) -> list[tuple[int, str]]:
        value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
        value_key_pairs.sort()
        return value_key_pairs[-n:]

    print(top_counts(counts))

    # collections.Counter does all of the above in one line.
    counter = Counter(tz_strings)
    print(counter.most_common(10))


def explain_counting_time_zones_pandas() -> None:
    """
    Problem: count time zones the idiomatic pandas way and chart the top 10.
    Why: building a DataFrame from the records lets `Series.value_counts` count in
    one call. We replace missing/empty time zones via `fillna` and Boolean
    indexing so the plot reads cleanly, then draw a horizontal bar chart with
    seaborn (headless, saved to a temp dir). In pandas 3.0 `value_counts` is a
    method on the Series (the old top-level `pd.value_counts` was removed).
    """
    print("== Counting time zones with pandas + seaborn bar chart ==")

    records = _load_records()
    if records is None:
        print("[guard] bitly data not available; skipping.")
        return

    frame = pd.DataFrame(records)
    print(frame["tz"].head())

    # value_counts on the Series counts each distinct time zone, most frequent first.
    tz_counts = frame["tz"].value_counts()
    print(tz_counts.head())

    # Fill missing tz with "Missing", and label the empty-string ones "Unknown".
    clean_tz = frame["tz"].fillna("Missing")
    assert isinstance(clean_tz, pd.Series)  # fillna is typed as a broad union
    # Copy-on-Write: assign through .loc with a Boolean mask.
    clean_tz.loc[clean_tz == ""] = "Unknown"
    tz_counts = clean_tz.value_counts()
    print(tz_counts.head())

    with tempfile.TemporaryDirectory() as tmp:
        # Top-10 horizontal bar plot: y = the time-zone labels, x = the counts.
        subset = tz_counts.head(10)
        sns.barplot(y=subset.index, x=subset.to_numpy())
        path = Path(tmp) / "top_time_zones.png"
        plt.savefig(path)
        print(f"saved top_time_zones.png -> exists={path.exists()}")
        plt.close("all")


def explain_agent_field() -> None:
    """
    Problem: study the `a` (agent) field — the browser/device string.
    Why: splitting on whitespace and taking the first token gives a rough browser
    label whose `value_counts` summarizes user behavior. Then we add an OS column
    with `np.where` ("Windows" if the string contains "Windows"), group by
    (tz, os), reshape with `unstack`, take the top time zones, and draw a
    normalized stacked bar plot of the Windows / non-Windows split.
    """
    print("== Decomposing the agent (a) field: browsers and Windows vs. not ==")

    records = _load_records()
    if records is None:
        print("[guard] bitly data not available; skipping.")
        return

    frame = pd.DataFrame(records)
    print(frame["a"][1])   # a single agent string, e.g. GoogleMaps/RochesterNY

    # First token of each agent string ~ the browser/app; summarize the top ones.
    results = pd.Series([x.split()[0] for x in frame["a"].dropna()])
    print(results.head(5))
    print(results.value_counts().head(8))

    # Drop rows with no agent, then flag Windows vs. not from the agent string.
    cframe = frame[frame["a"].notna()].copy()
    assert isinstance(cframe, pd.DataFrame)  # Boolean indexing is a broad union
    cframe["os"] = np.where(
        cframe["a"].str.contains("Windows"), "Windows", "Not Windows"
    )
    print(cframe["os"].head(5))

    # Group by time zone and OS; size() counts each combo, unstack reshapes to a
    # table (rows = tz, cols = os), and fillna(0) fills the empty combos.
    by_tz_os = cframe.groupby(["tz", "os"])
    agg_counts = by_tz_os.size().unstack().fillna(0)
    print(agg_counts.head())

    # Select the top overall time zones: argsort the row totals, take the last 10.
    indexer = agg_counts.sum(axis="columns").argsort()
    count_subset = agg_counts.take(indexer[-10:])
    print(count_subset)

    # pandas convenience for the same selection: nlargest on the row totals.
    print(agg_counts.sum(axis="columns").nlargest(10))

    with tempfile.TemporaryDirectory() as tmp:
        # stack -> long form so seaborn can plot count by tz, split by os (hue).
        stacked = count_subset.stack()
        stacked.name = "total"
        plot_df = stacked.reset_index()
        sns.barplot(x="total", y="tz", hue="os", data=plot_df)
        path = Path(tmp) / "tz_by_os.png"
        plt.savefig(path)
        print(f"saved tz_by_os.png -> exists={path.exists()}")
        plt.close("all")

        # Normalize each time zone's bars to sum to 1 (relative Windows share).
        def norm_total(group: pd.DataFrame) -> pd.DataFrame:
            group["normed_total"] = group["total"] / group["total"].sum()
            return group

        results_df = plot_df.groupby("tz").apply(norm_total, include_groups=False)
        # apply may return Series per the stubs; it is a DataFrame here.
        assert isinstance(results_df, pd.DataFrame)
        # tz becomes the index level after groupby/apply; restore it as a column.
        results_df = results_df.reset_index()
        sns.barplot(x="normed_total", y="tz", hue="os", data=results_df)
        path = Path(tmp) / "tz_by_os_normalized.png"
        plt.savefig(path)
        print(f"saved tz_by_os_normalized.png -> exists={path.exists()}")
        plt.close("all")


def main() -> None:
    explain_counting_time_zones_pure_python()
    explain_counting_time_zones_pandas()
    explain_agent_field()


main()
