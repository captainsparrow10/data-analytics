"""
Essential Functionality, Part 1: Reindex, Drop, Select, Align (Section 5.2)

This file walks through the fundamental mechanics of interacting with the data
in a Series or DataFrame: reshaping to a new set of labels (reindex), removing
entries (drop), the three styles of indexing/selection/filtering (`[]`, Boolean
masks, and the label/integer operators `loc`/`iloc`), and arithmetic with
automatic data alignment (including filling and broadcasting). The recurring
theme is that pandas operations align on the index, introducing missing values
wherever labels do not line up.

REINDEX ARGUMENTS
ARGUMENT     DESCRIPTION
index        New sequence to use as the row labels
columns      New sequence to use as the column labels
method       Fill method: "ffill" forward-fills, "bfill" back-fills
fill_value   Substitute value for newly introduced missing entries

INDEXING ON A DATAFRAME
SYNTAX             DESCRIPTION
df[col]            Select a column (or list of columns); a slice/mask selects rows
df.loc[rows, cols] Select by label (endpoint inclusive for slices)
df.iloc[rows, cols] Select by integer position (endpoint exclusive)

Run:
    poetry run python cap_03_panda/4-essential-functionality.py
"""

import numpy as np
import pandas as pd


def explain_reindexing() -> None:
    """
    Problem: rearrange data to conform to a new set of labels.
    Why: reindex creates a NEW object aligned to the new index, inserting NaN
    for labels that did not exist. `method="ffill"` carries the last value
    forward (useful for ordered data); DataFrames can reindex rows and columns.
    """
    print("== Reindexing ==")

    obj = pd.Series([4.5, 7.2, -5.3, 3.6], index=["d", "b", "a", "c"])
    # Rearranged to the new index; "e" had no value, so it becomes NaN.
    obj2 = obj.reindex(["a", "b", "c", "d", "e"])
    print(obj2)

    # method="ffill" forward-fills values into the new (interpolated) positions.
    obj3 = pd.Series(["blue", "purple", "yellow"], index=[0, 2, 4])
    print(obj3.reindex(np.arange(6), method="ffill"))

    # With a DataFrame, reindex can alter rows, columns, or both.
    frame = pd.DataFrame(
        np.arange(9).reshape((3, 3)),
        index=["a", "c", "d"],
        columns=["Ohio", "Texas", "California"],
    )
    print(frame.reindex(index=["a", "b", "c", "d"]))  # new row "b" -> NaN
    states = ["Texas", "Utah", "California"]
    print(frame.reindex(columns=states))              # reindex the columns


def explain_dropping() -> None:
    """
    Problem: produce a new object with selected entries removed.
    Why: `drop` returns a copy without the named labels. For a DataFrame, labels
    drop from the rows by default; pass `axis=1`/`axis="columns"` or the
    `columns=` keyword to drop columns instead.
    """
    print("== Dropping entries from an axis ==")

    obj = pd.Series(np.arange(5.0), index=["a", "b", "c", "d", "e"])
    print(obj.drop("c"))           # drop a single label
    print(obj.drop(["d", "c"]))    # drop several labels

    data = pd.DataFrame(
        np.arange(16).reshape((4, 4)),
        index=["Ohio", "Colorado", "Utah", "New York"],
        columns=["one", "two", "three", "four"],
    )
    print(data.drop(index=["Colorado", "Ohio"]))   # drop rows
    print(data.drop(columns=["two"]))              # drop a column by keyword
    print(data.drop("two", axis=1))                # drop a column by axis
    print(data.drop(["two", "four"], axis="columns"))


def explain_indexing_series() -> None:
    """
    Problem: select from a Series by label vs. by integer, unambiguously.
    Why: plain `[]` is ambiguous when the index itself holds integers, so pandas
    provides `loc` (always label-based, slices are endpoint-INCLUSIVE) and
    `iloc` (always integer-position based) to make intent explicit.
    """
    print("== Indexing, selection, filtering: Series ==")

    obj = pd.Series(np.arange(4.0), index=["a", "b", "c", "d"])
    print(obj["b"])            # by label
    print(obj[["b", "a", "d"]])  # several labels
    print(obj[obj < 2])        # Boolean mask

    # loc is the preferred, unambiguous label-based selector.
    print(obj.loc[["b", "a", "d"]])

    # With an integer index, prefer loc (labels) and iloc (positions).
    obj1 = pd.Series([1, 2, 3], index=[2, 0, 1])
    obj2 = pd.Series([1, 2, 3], index=["a", "b", "c"])
    print(obj1.iloc[[0, 1, 2]])  # by position
    print(obj2.iloc[[0, 1, 2]])  # by position
    # loc slices are INCLUSIVE of the endpoint (unlike Python slicing).
    print(obj2.loc["b":"c"])
    obj2.loc["b":"c"] = 5        # assignment through a label slice
    print(obj2)


def explain_indexing_dataframe() -> None:
    """
    Problem: select rows, columns, and scalars from a DataFrame three ways.
    Why: `df[col]` selects columns (but a slice/Boolean selects rows); a Boolean
    DataFrame can be used to assign element-wise; `loc`/`iloc` mix row and column
    selection by label / by integer position in one expression.
    """
    print("== Indexing, selection, filtering: DataFrame ==")

    data = pd.DataFrame(
        np.arange(16).reshape((4, 4)),
        index=["Ohio", "Colorado", "Utah", "New York"],
        columns=["one", "two", "three", "four"],
    )
    print(data["two"])                  # a single column as a Series
    print(data[["three", "one"]])       # several columns
    print(data[:2])                     # a row slice (special case)
    print(data[data["three"] > 5])      # rows where the mask is True

    # A Boolean DataFrame can drive an element-wise assignment.
    data[data < 5] = 0
    print(data)

    # loc selects by label; iloc by integer position; both mix rows and columns.
    print(data.loc["Colorado"])                       # one row by label
    print(data.loc["Colorado", ["two", "three"]])     # row + chosen columns
    print(data.iloc[2])                               # one row by position
    print(data.iloc[[1, 2], [3, 0, 1]])               # rows + columns by position
    print(data.loc[:"Utah", "two"])                   # label slice + column
    print(data.iloc[:, :3][data.three > 5])           # positions then a mask


def explain_arithmetic_alignment() -> None:
    """
    Problem: combine objects with different indexes and control the gaps.
    Why: arithmetic aligns on the union of labels, yielding NaN where they do
    not overlap; the `add(..., fill_value=...)` family substitutes a value for
    those gaps. Between a DataFrame and a Series, the Series broadcasts down the
    rows (matching the DataFrame's columns) by default.
    """
    print("== Arithmetic and data alignment ==")

    s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=["a", "c", "d", "e"])
    s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1], index=["a", "c", "e", "f", "g"])
    # Result index is the union; non-overlapping labels become NaN.
    print(s1 + s2)

    df1 = pd.DataFrame(np.arange(12.0).reshape((3, 4)), columns=list("abcd"))
    df2 = pd.DataFrame(np.arange(20.0).reshape((4, 5)), columns=list("abcde"))
    df2.loc[1, "b"] = np.nan
    # Plain + leaves NaN where rows/columns do not overlap...
    print(df1 + df2)
    # ...whereas add with fill_value=0 fills the gaps before adding.
    print(df1.add(df2, fill_value=0))
    # Each operator has a reversed-argument counterpart (rdiv == 1 / df1 here).
    print(df1.rdiv(1))

    # Operations between a DataFrame and a Series broadcast down the rows:
    # the Series's index is matched against the DataFrame's columns.
    frame = pd.DataFrame(
        np.arange(12.0).reshape((4, 3)),
        columns=list("bde"),
        index=["Utah", "Ohio", "Texas", "Oregon"],
    )
    series = frame.iloc[0]
    print(frame - series)
    # To match on the rows instead, use a method and specify axis="index".
    series3 = frame["d"]
    print(frame.sub(series3, axis="index"))


def main() -> None:
    explain_reindexing()
    explain_dropping()
    explain_indexing_series()
    explain_indexing_dataframe()
    explain_arithmetic_alignment()


main()
