"""
USDA Food Database (Section 13.4)

The US Department of Agriculture publishes a nutrient database; Ashley Williams
turned it into JSON. Each of the ~6600 records is one food with identifying
fields (id, description, group, manufacturer) plus a `nutrients` list of dicts
(value, units, description, group). This file reproduces the book's wrangling and
analysis: load the JSON, normalize every food's nutrient list into one big
DataFrame (tagging each with its food id), drop duplicates, build a food-info
table, merge the two, compute the MEDIAN value of each nutrient by food group
(with a headless zinc bar chart), and find the single food highest in each
nutrient using `idxmax`.

The database is downloaded on demand into a git-ignored `datasets/` cache; every
function guards on availability so the file exits 0 offline.

WHAT THIS FILE COVERS
STEP                        TECHNIQUE
load nested JSON            json.load -> list[dict]
normalize nutrients         per-food DataFrame + id, pd.concat, drop_duplicates
build food-info table       pd.DataFrame(db, columns=[...]) + value_counts
merge + rename columns      rename to avoid clashes, pd.merge on "id"
median by food group        groupby([nutrient, fgroup]).quantile(0.5) + plot
max food per nutrient       groupby.apply with Series.idxmax

Run:
    poetry run python cap_13_examples/4-usda-food.py
"""

import json
import os
import tempfile
import urllib.request
from pathlib import Path

import matplotlib

# HEADLESS: pick the non-interactive Agg backend BEFORE importing pyplot.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

DATA_DIR = os.path.join(os.path.dirname(__file__), "datasets")
RAW_BASE = "https://raw.githubusercontent.com/wesm/pydata-book/3rd-edition/datasets"


def ensure(rel_path: str, url: str) -> str | None:
    """Return a cached local path, downloading once; None (with a hint) on failure."""
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


def _load_db() -> list[dict[str, object]] | None:
    """Load the USDA JSON database into a list of food dicts, or None."""
    path = ensure("usda_food/database.json", f"{RAW_BASE}/usda_food/database.json")
    if path is None:
        return None
    with open(path) as f:
        db = json.load(f)
    return db


def explain_explore_structure() -> None:
    """
    Problem: understand the nested record shape before reshaping it.
    Why: each food carries a list of nutrient dicts. Turning ONE food's nutrient
    list into a DataFrame, and building a flat food-info table with a chosen
    column subset, shows the two halves we will later merge. `value_counts` on the
    group column reveals which food groups dominate the database.
    """
    print("== Exploring the USDA record structure ==")

    db = _load_db()
    if db is None:
        print("[guard] USDA data not available; skipping.")
        return

    print(len(db))                              # number of foods
    print(list(db[0].keys()))                   # fields per food
    nutrients = pd.DataFrame(db[0]["nutrients"])  # one food's nutrient list
    print(nutrients.head(7))

    # Flat table of identifying fields per food.
    info_keys = ["description", "group", "id", "manufacturer"]
    info = pd.DataFrame(db, columns=info_keys)
    print(info.head())
    # Distribution of food groups (top 10).
    print(info["group"].value_counts()[:10])


def _assemble() -> pd.DataFrame | None:
    """
    Build the merged nutrient+food table the book calls `ndata`.

    For each food: turn its nutrient list into a DataFrame, tag it with the food
    id, collect them, concat, drop duplicates, then merge with the renamed
    food-info table on "id". Returns None if the database is unavailable.
    """
    db = _load_db()
    if db is None:
        return None

    # One DataFrame per food's nutrients, each tagged with the food id.
    nutrient_frames: list[pd.DataFrame] = []
    for rec in db:
        fnuts = pd.DataFrame(rec["nutrients"])
        fnuts["id"] = rec["id"]
        nutrient_frames.append(fnuts)
    nutrients = pd.concat(nutrient_frames, ignore_index=True)

    # The raw concat contains duplicate rows; drop them.
    nutrients = nutrients.drop_duplicates()

    # "group" and "description" exist in BOTH tables; rename each side to avoid a
    # clash when we merge (food side -> food/fgroup; nutrient side -> nutrient/nutgroup).
    info_keys = ["description", "group", "id", "manufacturer"]
    info = pd.DataFrame(db, columns=info_keys)
    info = info.rename(columns={"description": "food", "group": "fgroup"})
    nutrients = nutrients.rename(
        columns={"description": "nutrient", "group": "nutgroup"}
    )

    # Merge the nutrient rows with their food's info on the shared id.
    ndata = pd.merge(nutrients, info, on="id")
    return ndata


def explain_median_by_food_group() -> None:
    """
    Problem: compare nutrient levels across food groups.
    Why: grouping the merged table by (nutrient, food group) and taking the median
    value summarizes, e.g., how much zinc each food group typically provides. A
    horizontal bar chart of the zinc medians makes the ranking obvious.
    """
    print("== Median nutrient value by food group (zinc chart) ==")

    ndata = _assemble()
    if ndata is None:
        print("[guard] USDA data not available; skipping.")
        return

    print(ndata.iloc[30000])  # a sample merged row

    # Median value of each nutrient within each food group.
    result = ndata.groupby(["nutrient", "fgroup"])["value"].quantile(0.5)
    # Zinc medians by food group, sorted, as a horizontal bar chart. (Indexing the
    # MultiIndex Series is typed as a broad union; narrow to a Series.)
    zinc_all = result["Zinc, Zn"]
    assert isinstance(zinc_all, pd.Series)
    zinc = zinc_all.sort_values()
    print(zinc)

    with tempfile.TemporaryDirectory() as tmp:
        zinc.plot(kind="barh")
        path = Path(tmp) / "zinc_by_group.png"
        plt.savefig(path, bbox_inches="tight")
        print(f"saved zinc_by_group.png -> exists={path.exists()}")
        plt.close("all")


def explain_max_food_per_nutrient() -> None:
    """
    Problem: find the single food highest in each nutrient.
    Why: grouping by (nutrient group, nutrient) and applying a function that uses
    `Series.idxmax` to locate the row with the largest value returns the densest
    food for every nutrient. We trim the food names and show the Amino Acids group
    as the book does.
    """
    print("== Food with the maximum amount of each nutrient ==")

    ndata = _assemble()
    if ndata is None:
        print("[guard] USDA data not available; skipping.")
        return

    by_nutrient = ndata.groupby(["nutgroup", "nutrient"])

    def get_maximum(x: pd.DataFrame) -> pd.Series:
        # idxmax on the value column gives the index label of the densest food.
        return x.loc[x["value"].idxmax()]

    max_foods = by_nutrient.apply(get_maximum, include_groups=False)[["value", "food"]]
    assert isinstance(max_foods, pd.DataFrame)
    # Trim long food descriptions for display.
    max_foods["food"] = max_foods["food"].str[:50]
    print(max_foods.loc["Amino Acids"]["food"])


def main() -> None:
    explain_explore_structure()
    explain_median_by_food_group()
    explain_max_food_per_nutrient()


main()
