"""
Hierarchical Indexing: Multiple Index Levels on an Axis (Section 8.1)

Hierarchical indexing is an important feature of pandas that lets you have
multiple (two or more) index *levels* on an axis. Another way of thinking about
it is that it gives you a way to work with higher dimensional data in a lower
dimensional form. It plays a central role in reshaping data and in group-based
operations like forming a pivot table.

This file covers creating a Series/DataFrame with a MultiIndex, partial
indexing, `unstack`/`stack`, MultiIndex on the columns, reordering and sorting
levels (`swaplevel`, `sort_index(level=)`), summary statistics by level
(`groupby(level=)`), and moving between a DataFrame's columns and its row index
(`set_index`/`reset_index`).

KEY OPERATIONS IN THIS FILE
METHOD/ATTRIBUTE   DESCRIPTION
MultiIndex         The index type holding two or more levels on one axis
unstack / stack    Pivot an inner index level into columns / and back again
swaplevel          Return a new object with two index levels interchanged
sort_index(level=) Sort lexicographically by one or more chosen levels
groupby(level=)    Aggregate descriptive statistics by a named/numbered level
set_index          Build a new row index from one or more DataFrame columns
reset_index        Move hierarchical index levels back into the columns

Run:
    poetry run python cap_08_wrangling/1-hierarchical-indexing.py
"""

import numpy as np
import pandas as pd


def explain_multiindex_series() -> None:
    """
    Problem: build a Series whose index has two levels and select subsets.
    Why: passing a list of lists (or arrays) as the index creates a MultiIndex.
    The "gaps" in the printed index mean "use the label directly above". With a
    hierarchically indexed object, *partial* indexing lets you concisely select
    subsets of the data, including from an inner level via `loc[:, ...]`.
    """
    print("== Creating a MultiIndex Series and partial indexing ==")

    # A fixed RNG (the book uses np.random.uniform; default_rng is the modern API).
    rng = np.random.default_rng(seed=12345)
    data = pd.Series(
        rng.uniform(size=9),
        index=[["a", "a", "a", "b", "b", "c", "c", "d", "d"], [1, 2, 3, 1, 3, 1, 2, 2, 3]],
    )
    print(data)
    print(data.index)  # a MultiIndex with the tuples (a,1), (a,2), ...

    # Partial indexing selects subsets using the outer level.
    print(data["b"])           # everything under the outer label "b"
    print(data["b":"c"])       # an outer-level slice
    print(data.loc[["b", "d"]])  # a list of outer labels

    # Selection is even possible from an inner level.
    print(data.loc[:, 2])      # all values whose second index level equals 2


def explain_unstack_stack() -> None:
    """
    Problem: rearrange a hierarchically indexed Series into a 2-D table and back.
    Why: hierarchical indexing is the backbone of reshaping. `unstack` pivots an
    inner row level into columns (producing a DataFrame, with NaN where a
    combination is missing); `stack` is its inverse, collapsing columns back into
    an inner row level.
    """
    print("== unstack and stack (reshaping a MultiIndex Series) ==")

    rng = np.random.default_rng(seed=12345)
    data = pd.Series(
        rng.uniform(size=9),
        index=[["a", "a", "a", "b", "b", "c", "c", "d", "d"], [1, 2, 3, 1, 3, 1, 2, 2, 3]],
    )

    # unstack rotates the inner index level into a set of columns.
    print(data.unstack())
    # stack is the inverse operation.
    print(data.unstack().stack())


def explain_multiindex_dataframe() -> None:
    """
    Problem: give BOTH axes of a DataFrame a hierarchical index, name the levels,
    and select groups of columns.
    Why: either axis can carry a MultiIndex. The levels can have names (which
    supersede the single-level `name` attribute and are NOT part of the row
    labels). `nlevels` reports how many levels an index has, and partial column
    indexing selects whole groups of columns at once.
    """
    print("== MultiIndex on both axes; level names; partial column indexing ==")

    frame = pd.DataFrame(
        np.arange(12).reshape((4, 3)),
        index=[["a", "a", "b", "b"], [1, 2, 1, 2]],
        columns=[["Ohio", "Ohio", "Colorado"], ["Green", "Red", "Green"]],
    )
    print(frame)

    # Name the levels of each axis (these names are separate from the labels).
    frame.index.names = ["key1", "key2"]
    frame.columns.names = ["state", "color"]
    print(frame)
    print(frame.index.nlevels)  # 2

    # Partial column indexing selects a group of columns.
    print(frame["Ohio"])

    # A MultiIndex can be created on its own and then reused.
    print(
        pd.MultiIndex.from_arrays(
            [["Ohio", "Ohio", "Colorado"], ["Green", "Red", "Green"]],
            names=["state", "color"],
        )
    )


def explain_reordering_sorting_levels() -> None:
    """
    Problem: rearrange the order of index levels and sort the data by one level.
    Why: `swaplevel` takes two level numbers or names and returns a new object
    with the levels interchanged (data otherwise unaltered). `sort_index` sorts
    lexicographically using all levels by default, but `level=` restricts the
    sort to a single level. Selection performance is best when the index is
    lexicographically sorted starting with the outermost level.
    """
    print("== Reordering and sorting levels (swaplevel, sort_index) ==")

    frame = pd.DataFrame(
        np.arange(12).reshape((4, 3)),
        index=[["a", "a", "b", "b"], [1, 2, 1, 2]],
        columns=[["Ohio", "Ohio", "Colorado"], ["Green", "Red", "Green"]],
    )
    frame.index.names = ["key1", "key2"]
    frame.columns.names = ["state", "color"]

    # Interchange the two row levels. (The book passes the level names; the pandas
    # stubs only type swaplevel's args as axis positions, so we use the level
    # numbers 0 and 1, which name exactly the same two levels.)
    print(frame.swaplevel(0, 1))
    # Sort using only the level=1 ("key2") values.
    print(frame.sort_index(level=1))
    # Swap, then sort by the (now outer) level 0.
    print(frame.swaplevel(0, 1).sort_index(level=0))


def explain_summary_statistics_by_level() -> None:
    """
    Problem: aggregate descriptive statistics within each value of one level.
    Why: many summary statistics accept a level via `groupby(level=)`, letting you
    sum/mean/etc. by a particular level on either the rows or the columns. (The
    book's older `level=` argument on reductions is now expressed through
    `groupby`; `groupby(axis="columns")` was removed in pandas 2.x, so to
    aggregate across the column levels we transpose, group by the level, then
    transpose back.)
    """
    print("== Summary statistics by level (groupby(level=)) ==")

    frame = pd.DataFrame(
        np.arange(12).reshape((4, 3)),
        index=[["a", "a", "b", "b"], [1, 2, 1, 2]],
        columns=[["Ohio", "Ohio", "Colorado"], ["Green", "Red", "Green"]],
    )
    frame.index.names = ["key1", "key2"]
    frame.columns.names = ["state", "color"]

    # Aggregate the rows by the "key2" level.
    print(frame.groupby(level="key2").sum())
    # Aggregate the columns by the "color" level (transpose -> group -> transpose).
    # .sum() is typed broadly (could be a scalar); narrow to a DataFrame so the
    # final .T resolves cleanly.
    by_color = frame.T.groupby(level="color").sum()
    assert isinstance(by_color, pd.DataFrame)
    print(by_color.T)


def explain_indexing_with_columns() -> None:
    """
    Problem: move DataFrame columns into the row index and back out again.
    Why: it is common to use one or more columns as the row index (`set_index`),
    or to move the index levels back into the columns (`reset_index`). By default
    `set_index` removes the chosen columns; pass `drop=False` to keep them too.
    """
    print("== Indexing with a DataFrame's columns (set_index/reset_index) ==")

    frame = pd.DataFrame(
        {
            "a": range(7),
            "b": range(7, 0, -1),
            "c": ["one", "one", "one", "two", "two", "two", "two"],
            "d": [0, 1, 2, 0, 1, 2, 3],
        }
    )
    print(frame)

    # Build a hierarchical row index from columns "c" and "d".
    frame2 = frame.set_index(["c", "d"])
    print(frame2)
    # Keep the columns in place as well.
    print(frame.set_index(["c", "d"], drop=False))
    # reset_index does the opposite: index levels move back to columns.
    print(frame2.reset_index())


def main() -> None:
    explain_multiindex_series()
    explain_unstack_stack()
    explain_multiindex_dataframe()
    explain_reordering_sorting_levels()
    explain_summary_statistics_by_level()
    explain_indexing_with_columns()


main()
