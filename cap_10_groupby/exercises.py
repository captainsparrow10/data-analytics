"""
Aggregation & Group Operations: Practice Exercises

This file is a hands-on companion to Chapter 10. Each exercise builds its own
small in-code DataFrame and works the split-apply-combine paradigm from a
slightly different angle: grouping by one or more keys, iterating over groups,
aggregating with one or several functions, transforming group-wise, filtering
whole groups, bucketing with cut/qcut, and reshaping with pivot_table and
crosstab. The frames here describe an imaginary chain of coffee shops (orders,
baristas, regions) so the numbers stay concrete and easy to reason about. Every
problem statement says what result to expect; the body is one worked solution
with inline commentary.

Run:
    poetry run python cap_10_groupby/exercises.py
"""

import numpy as np
import pandas as pd


def exercise_01() -> None:
    """
    Exercise 1: Group by a single key and aggregate

    Problem: Given coffee-shop orders tagged by `region`, compute the total
    `revenue` taken in each region.

    Purpose: The simplest split-apply-combine: split rows by one key, apply a
    sum to one numeric column, combine into a per-group Series.

    Expected Output: a Series indexed by region (East, North, South) whose
    values are the summed revenue per region (East: 31.0, North: 18.5,
    South: 27.0).
    """
    orders = pd.DataFrame(
        {
            "region": ["North", "South", "North", "East", "South", "East"],
            "revenue": [8.0, 12.0, 10.5, 15.0, 15.0, 16.0],
        }
    )
    # Split by region, then sum the single numeric column.
    revenue_by_region = orders.groupby("region")["revenue"].sum()
    print(revenue_by_region)


def exercise_02() -> None:
    """
    Exercise 2: Group by multiple keys

    Problem: For the same orders, broken down by `region` and `drink`, compute
    the mean `revenue` of each (region, drink) combination.

    Purpose: Passing a list of keys produces a hierarchical index: one row per
    observed combination of the two keys.

    Expected Output: a Series with a MultiIndex (region, drink) of mean revenue,
    e.g. (North, Latte) -> 9.0, (South, Mocha) -> 13.5.
    """
    orders = pd.DataFrame(
        {
            "region": ["North", "North", "South", "South", "East", "East"],
            "drink": ["Latte", "Latte", "Mocha", "Mocha", "Latte", "Mocha"],
            "revenue": [8.0, 10.0, 12.0, 15.0, 16.0, 14.0],
        }
    )
    # Two keys -> grouped result carries a (region, drink) MultiIndex.
    mean_revenue = orders.groupby(["region", "drink"])["revenue"].mean()
    print(mean_revenue)


def exercise_03() -> None:
    """
    Exercise 3: Iterate over groups

    Problem: Print each region's name followed by the number of orders in that
    region by iterating over the GroupBy object directly.

    Purpose: A GroupBy is iterable, yielding (group_key, sub_frame) pairs — handy
    when you need to inspect or process each group with plain Python.

    Expected Output: one line per region of the form "North: 2 orders".
    """
    orders = pd.DataFrame(
        {
            "region": ["North", "South", "North", "East", "South"],
            "revenue": [8.0, 12.0, 10.5, 15.0, 9.0],
        }
    )
    # Each iteration yields the group key and the matching sub-DataFrame.
    for region, group in orders.groupby("region"):
        print(f"{region}: {len(group)} orders")


def exercise_04() -> None:
    """
    Exercise 4: Select one column within a group

    Problem: Group orders by `barista` and report the largest single `tip` each
    barista earned.

    Purpose: Selecting a column on the GroupBy (df.groupby(k)["col"]) restricts
    the aggregation to just that column, which is both clearer and faster than
    aggregating the whole frame and slicing afterwards.

    Expected Output: a Series indexed by barista with each one's max tip
    (Ana: 3.0, Beto: 2.5).
    """
    orders = pd.DataFrame(
        {
            "barista": ["Ana", "Beto", "Ana", "Beto", "Ana"],
            "tip": [1.5, 2.0, 3.0, 2.5, 2.0],
            "revenue": [8.0, 9.0, 11.0, 10.0, 7.0],
        }
    )
    # Narrow to the `tip` column before aggregating, ignoring `revenue`.
    max_tip = orders.groupby("barista")["tip"].max()
    print(max_tip)


def exercise_05() -> None:
    """
    Exercise 5: Multiple aggregations with .agg (list form)

    Problem: For each `drink`, compute the count, mean, and max of `revenue` in a
    single pass.

    Purpose: Passing a list of functions to .agg produces a DataFrame with one
    column per function, avoiding three separate groupby calls.

    Expected Output: a DataFrame indexed by drink with columns count, mean, max.
    """
    orders = pd.DataFrame(
        {
            "drink": ["Latte", "Mocha", "Latte", "Mocha", "Latte"],
            "revenue": [8.0, 12.0, 10.0, 14.0, 9.0],
        }
    )
    # A list of reducers -> one output column each.
    summary = orders.groupby("drink")["revenue"].agg(["count", "mean", "max"])
    print(summary)


def exercise_06() -> None:
    """
    Exercise 6: Named aggregations (named-tuple form)

    Problem: For each `region`, build a tidy summary with clearly named columns:
    `orders` (row count), `total_revenue` (sum), and `avg_tip` (mean tip).

    Purpose: Named aggregation (column=("source", "func")) lets you aggregate
    different source columns with different functions and choose the output
    names, producing a clean, self-describing result frame.

    Expected Output: a DataFrame indexed by region with columns orders,
    total_revenue, avg_tip.
    """
    orders = pd.DataFrame(
        {
            "region": ["North", "North", "South", "South", "East"],
            "revenue": [8.0, 10.0, 12.0, 15.0, 16.0],
            "tip": [1.0, 2.0, 1.5, 2.5, 3.0],
        }
    )
    # Each kwarg names an output column and pairs (source_column, reducer).
    summary = orders.groupby("region").agg(
        orders=("revenue", "count"),
        total_revenue=("revenue", "sum"),
        avg_tip=("tip", "mean"),
    )
    print(summary)


def exercise_07() -> None:
    """
    Exercise 7: Apply a custom function per group

    Problem: For each `region`, return the two orders with the highest `revenue`
    (the region's top sellers), keeping the original row data.

    Purpose: .apply is the most general tool — when no built-in aggregation fits,
    you hand each group's sub-frame to your own function. Here it returns a frame
    per group (a "top-N" selection), and pandas stitches the pieces together.

    Expected Output: a DataFrame holding the two highest-revenue rows of each
    region, with a (region, original_index) MultiIndex.
    """
    orders = pd.DataFrame(
        {
            "region": ["North", "North", "North", "South", "South", "South"],
            "drink": ["Latte", "Mocha", "Tea", "Latte", "Mocha", "Tea"],
            "revenue": [8.0, 14.0, 6.0, 12.0, 9.0, 15.0],
        }
    )

    def top_two(group: pd.DataFrame) -> pd.DataFrame:
        # Sort this group's rows by revenue and keep the two largest.
        return group.sort_values("revenue", ascending=False).head(2)

    # include_groups=False: the function gets only non-key columns, so the
    # grouping column is not re-appended (pandas 3.0 behavior).
    top_sellers = orders.groupby("region").apply(top_two, include_groups=False)
    print(top_sellers)


def exercise_08() -> None:
    """
    Exercise 8: Group-wise normalization with transform

    Problem: Add a `z_score` column expressing each order's `revenue` relative to
    its own region (subtract the region mean, divide by the region std).

    Purpose: transform returns a result aligned to the ORIGINAL rows (same shape),
    not one row per group — exactly what you need to attach a group-relative
    statistic back onto every record.

    Expected Output: the orders frame with a new z_score column whose values are
    centered within each region (each region's z-scores sum to ~0).
    """
    orders = pd.DataFrame(
        {
            "region": ["North", "North", "North", "South", "South", "South"],
            "revenue": [8.0, 10.0, 12.0, 14.0, 18.0, 22.0],
        }
    )
    grouped = orders.groupby("region")["revenue"]
    # transform broadcasts the per-group mean/std back to every row.
    orders["z_score"] = (orders["revenue"] - grouped.transform("mean")) / grouped.transform("std")
    print(orders)


def exercise_09() -> None:
    """
    Exercise 9: Fill missing values with the group mean

    Problem: Some `rating` values are missing. Fill each gap with the mean rating
    of the same `drink` rather than a single global average.

    Purpose: A classic transform use case: compute a per-group statistic and use
    it to impute missing values, so each gap is filled with a contextually
    appropriate number.

    Expected Output: the frame with no NaN ratings; each former NaN equals the
    mean rating of its drink (Latte gaps -> 4.0, Mocha gaps -> 3.0).
    """
    reviews = pd.DataFrame(
        {
            "drink": ["Latte", "Latte", "Latte", "Mocha", "Mocha", "Mocha"],
            "rating": [4.5, np.nan, 3.5, 2.0, np.nan, 4.0],
        }
    )
    # group_mean is aligned to the original rows, so fillna lines up per drink.
    group_mean = reviews.groupby("drink")["rating"].transform("mean")
    reviews["rating"] = reviews["rating"].fillna(group_mean)
    print(reviews)


def exercise_10() -> None:
    """
    Exercise 10: Filter whole groups by a condition

    Problem: Keep only the orders belonging to baristas who served at least 3
    orders; drop every order from less active baristas.

    Purpose: filter operates at the GROUP level — its predicate returns one
    bool per group, and pandas keeps or discards all rows of that group
    together. This differs from row-level boolean masking.

    Expected Output: a DataFrame containing only Ana's rows (she has 3 orders);
    Beto and Cris (fewer than 3 each) are removed entirely.
    """
    orders = pd.DataFrame(
        {
            "barista": ["Ana", "Beto", "Ana", "Cris", "Ana", "Beto"],
            "revenue": [8.0, 9.0, 11.0, 10.0, 7.0, 12.0],
        }
    )
    # The lambda receives each group; True keeps all of that group's rows.
    busy = orders.groupby("barista").filter(lambda g: len(g) >= 3)
    print(busy)


def exercise_11() -> None:
    """
    Exercise 11: Equal-width buckets with cut, then group

    Problem: Bucket each order's `revenue` into three equal-width price bands and
    report how many orders fall in each band.

    Purpose: pd.cut slices a numeric range into equal-WIDTH intervals; grouping by
    the resulting categorical turns a continuous variable into a histogram-like
    summary.

    Expected Output: a Series indexed by the three revenue intervals giving the
    count of orders per band.
    """
    orders = pd.DataFrame({"revenue": [5.0, 7.0, 9.0, 12.0, 15.0, 18.0, 20.0, 25.0]})
    # cut -> 3 equal-width bins spanning [min, max].
    bands = pd.cut(orders["revenue"], bins=3)
    counts = orders.groupby(bands, observed=True)["revenue"].count()
    print(counts)


def exercise_12() -> None:
    """
    Exercise 12: Quantile buckets with qcut, then aggregate

    Problem: Split orders into two equal-sized halves by `revenue` (low vs high
    spenders) and compute the mean `tip` of each half.

    Purpose: pd.qcut splits by QUANTILE, giving groups with roughly equal counts
    rather than equal widths — the right tool for "top half vs bottom half"
    questions. Labels make the result readable.

    Expected Output: a Series indexed by ["low", "high"] with each half's mean
    tip; the high half should show the larger average tip.
    """
    orders = pd.DataFrame(
        {
            "revenue": [6.0, 8.0, 9.0, 11.0, 16.0, 20.0],
            "tip": [0.5, 1.0, 1.0, 2.0, 3.0, 3.5],
        }
    )
    # qcut into 2 equal-frequency halves, with friendly labels.
    halves = pd.qcut(orders["revenue"], q=2, labels=["low", "high"])
    mean_tip = orders.groupby(halves, observed=True)["tip"].mean()
    print(mean_tip)


def exercise_13() -> None:
    """
    Exercise 13: pivot_table with margins and fill_value

    Problem: Build a region-by-drink table of mean `revenue`, filling absent
    (region, drink) combinations with 0 and adding an "All" row/column of overall
    means.

    Purpose: pivot_table is the declarative counterpart to groupby for two-key
    aggregations: index and columns name the two keys, aggfunc the reducer,
    fill_value patches empty cells, and margins adds the grand totals.

    Expected Output: a DataFrame indexed by region with one column per drink plus
    an "All" margin column, an "All" margin row, and 0 where a combination had no
    orders.
    """
    orders = pd.DataFrame(
        {
            "region": ["North", "North", "South", "South", "East"],
            "drink": ["Latte", "Mocha", "Latte", "Mocha", "Latte"],
            "revenue": [8.0, 12.0, 10.0, 14.0, 16.0],
        }
    )
    # index/columns = the two grouping keys; aggfunc = the reducer.
    table = orders.pivot_table(
        values="revenue",
        index="region",
        columns="drink",
        aggfunc="mean",
        fill_value=0,
        margins=True,
    )
    print(table)


def exercise_14() -> None:
    """
    Exercise 14: Frequency cross-tabulation with crosstab

    Problem: Count how many orders each `region` placed for each `drink` (a
    contingency table of counts), including row and column totals.

    Purpose: pd.crosstab is a shortcut for pivot_table when the aggregation is a
    simple frequency count of two categorical variables — it takes the two
    factors directly and returns their cross-tabulation.

    Expected Output: a counts DataFrame (regions x drinks) with an "All" margin
    row and column.
    """
    orders = pd.DataFrame(
        {
            "region": ["North", "North", "South", "South", "South", "East"],
            "drink": ["Latte", "Mocha", "Latte", "Latte", "Mocha", "Mocha"],
        }
    )
    # crosstab counts occurrences of each (region, drink) pair.
    table = pd.crosstab(orders["region"], orders["drink"], margins=True)
    print(table)


def main() -> None:
    print("=== Exercise 1: Group by a single key and aggregate ===")
    exercise_01()

    print("\n=== Exercise 2: Group by multiple keys ===")
    exercise_02()

    print("\n=== Exercise 3: Iterate over groups ===")
    exercise_03()

    print("\n=== Exercise 4: Select one column within a group ===")
    exercise_04()

    print("\n=== Exercise 5: Multiple aggregations with .agg (list form) ===")
    exercise_05()

    print("\n=== Exercise 6: Named aggregations (named-tuple form) ===")
    exercise_06()

    print("\n=== Exercise 7: Apply a custom function per group ===")
    exercise_07()

    print("\n=== Exercise 8: Group-wise normalization with transform ===")
    exercise_08()

    print("\n=== Exercise 9: Fill missing values with the group mean ===")
    exercise_09()

    print("\n=== Exercise 10: Filter whole groups by a condition ===")
    exercise_10()

    print("\n=== Exercise 11: Equal-width buckets with cut, then group ===")
    exercise_11()

    print("\n=== Exercise 12: Quantile buckets with qcut, then aggregate ===")
    exercise_12()

    print("\n=== Exercise 13: pivot_table with margins and fill_value ===")
    exercise_13()

    print("\n=== Exercise 14: Frequency cross-tabulation with crosstab ===")
    exercise_14()


main()
