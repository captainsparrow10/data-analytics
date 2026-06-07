"""
Pivot Tables and Cross-Tabulation (Section 10.5)

A *pivot table* summarizes a table of data by one or more keys, arranging the
data in a rectangle with some group keys along the rows and some along the
columns. In pandas this is built on the `groupby` facility combined with
hierarchical-index reshaping; `DataFrame.pivot_table` (and the top-level
`pandas.pivot_table`) provide a convenient interface and can add partial totals,
known as *margins*.

A *cross-tabulation* (or *crosstab*) is a special case of a pivot table that
computes group frequencies.

This file covers `pivot_table` with default mean aggregation, choosing the
row/column keys and `values`, partial totals via `margins=True`, alternative
`aggfunc`s (count/len for cross-tabulations), `fill_value` for empty cells, and
`pd.crosstab`.

PIVOT_TABLE OPTIONS (Table 10-2, selection)
ARGUMENT          DESCRIPTION
values            Column(s) to aggregate; by default all numeric columns
index             Keys to group on the rows of the result
columns           Keys to group on the columns of the result
aggfunc           Aggregation function or list (default "mean")
fill_value        Replace missing values in the result table
margins           Add row/column subtotals and a grand total (the "All" labels)

Run:
    poetry run python cap_10_groupby/5-pivot-tables-crosstab.py
"""

from io import StringIO

import numpy as np
import pandas as pd


def _tips() -> pd.DataFrame:
    """Small tips-like DataFrame built in code (the book loads examples/tips.csv)."""
    rng = np.random.default_rng(seed=10)
    n = 200
    days = rng.choice(["Fri", "Sat", "Sun", "Thur"], size=n, p=[0.1, 0.35, 0.3, 0.25])
    times = np.where(np.isin(days, ["Fri", "Thur"]), rng.choice(["Lunch", "Dinner"], size=n), "Dinner")
    total_bill = np.round(rng.gamma(shape=6.0, scale=3.3, size=n) + 3.0, 2)
    smoker = rng.choice(["No", "Yes"], size=n, p=[0.62, 0.38])
    size = rng.integers(1, 7, size=n)
    tip = np.round(total_bill * rng.uniform(0.10, 0.25, size=n), 2)
    tips = pd.DataFrame(
        {
            "total_bill": total_bill,
            "tip": tip,
            "smoker": smoker,
            "day": days,
            "time": times,
            "size": size,
        }
    )
    tips["tip_pct"] = tips["tip"] / tips["total_bill"]
    return tips


def explain_pivot_table_basics() -> None:
    """
    Problem: summarize a table by keys on the rows (and optionally the columns).
    Why: `pivot_table` defaults to the group MEAN. Pass `index` for the row keys;
    it could be reproduced with `groupby(...).mean()`. Adding `columns` and
    restricting `values` reshapes selected statistics into a grid — group keys
    split across both axes.
    """
    print("== pivot_table basics ==")

    tips = _tips()
    print(tips.head())

    # Group means arranged by day and smoker on the rows. The book aggregates all
    # numeric columns; pandas 3.0 would try to average the string `time` column
    # too, so we name the numeric `values` explicitly (the same set the book shows).
    print(
        tips.pivot_table(
            index=["day", "smoker"], values=["size", "tip", "tip_pct", "total_bill"]
        )
    )

    # Average of only tip_pct and size, with smoker on the columns.
    print(
        tips.pivot_table(
            index=["time", "day"], columns="smoker", values=["tip_pct", "size"]
        )
    )


def explain_margins_and_aggfunc() -> None:
    """
    Problem: add subtotals/grand totals, and aggregate with something else.
    Why: `margins=True` adds "All" row and column labels holding the statistics
    for each tier of data. A different `aggfunc` ("count"/len) turns the table
    into a cross-tabulation of group sizes; "count" excludes NA values while len
    does not.
    """
    print("== margins and alternative aggfunc ==")

    tips = _tips()

    # Partial totals (the "All" labels) added on both axes.
    print(
        tips.pivot_table(
            index=["time", "day"],
            columns="smoker",
            values=["tip_pct", "size"],
            margins=True,
        )
    )

    # aggfunc=len gives a cross-tabulation (frequency) of group sizes.
    print(
        tips.pivot_table(
            index=["time", "smoker"],
            columns="day",
            values="tip_pct",
            aggfunc=len,
            margins=True,
        )
    )


def explain_fill_value() -> None:
    """
    Problem: replace empty/NA combinations in a pivot table with a value.
    Why: some key combinations may be empty (NA). `fill_value` substitutes a
    chosen value (here 0) for those cells so the table is fully populated.
    """
    print("== fill_value for empty combinations ==")

    tips = _tips()
    print(
        tips.pivot_table(
            index=["time", "size", "smoker"],
            columns="day",
            values="tip_pct",
            fill_value=0,
        )
    )


def explain_crosstab() -> None:
    """
    Problem: compute group frequencies (a contingency table).
    Why: `pd.crosstab` is a convenience for the count special case of a pivot
    table. Its first two arguments can each be an array, Series, or list of
    arrays; `margins=True` adds the row/column totals.
    """
    print("== Cross-tabulations: crosstab ==")

    raw = """Sample\tNationality\tHandedness
1\tUSA\tRight-handed
2\tJapan\tLeft-handed
3\tUSA\tRight-handed
4\tJapan\tRight-handed
5\tJapan\tLeft-handed
6\tJapan\tRight-handed
7\tUSA\tRight-handed
8\tUSA\tLeft-handed
9\tJapan\tRight-handed
10\tUSA\tRight-handed"""
    data = pd.read_table(StringIO(raw), sep="\t")
    print(data)

    # Summarize counts by nationality vs. handedness, with totals.
    print(pd.crosstab(data["Nationality"], data["Handedness"], margins=True))

    # crosstab also accepts a list of arrays for either axis (tips example).
    tips = _tips()
    print(pd.crosstab([tips["time"], tips["day"]], tips["smoker"], margins=True))


def main() -> None:
    explain_pivot_table_basics()
    explain_margins_and_aggfunc()
    explain_fill_value()
    explain_crosstab()


main()
