"""
Concatenating Along an Axis and Combining Overlapping Data (Section 8.2, part 2)

Beyond key-based merges, pandas can *concatenate* (or "stack") objects together
along an axis, and *combine* two datasets whose indexes overlap. NumPy's
`concatenate` does this for raw arrays; `pandas.concat` generalizes it for
labeled Series and DataFrames, addressing axis alignment, identifiability of the
pieces (`keys`), and discarding default integer labels (`ignore_index`). For
overlapping data, `np.where` gives an array-oriented if-else, while the Series/
DataFrame `combine_first` method patches missing values aligning on the index.

KEY OPERATIONS IN THIS FILE
FUNCTION/METHOD    DESCRIPTION
np.concatenate     Glue raw NumPy arrays along an axis (no label alignment)
pd.concat          Concatenate labeled objects; aligns the other axis
  axis             Concatenate along rows ("index") or columns ("columns")
  join             "outer" (union, default) or "inner" (intersection) of axes
  keys             Build a hierarchical index identifying each piece
  ignore_index     Discard the labels and assign a fresh RangeIndex
combine_first      Patch missing values in one object using another (by index)

Run:
    poetry run python cap_08_wrangling/3-concatenate-and-combine.py
"""

import numpy as np
import pandas as pd


def explain_numpy_concatenate() -> None:
    """
    Problem: glue raw NumPy arrays together along an axis.
    Why: concatenation (a.k.a. stacking) is the array-level building block.
    `np.concatenate` joins arrays with no notion of labels, choosing the axis.
    """
    print("== np.concatenate (raw arrays) ==")

    arr = np.arange(12).reshape((3, 4))
    print(arr)
    print(np.concatenate([arr, arr], axis=1))  # side by side


def explain_concat_series() -> None:
    """
    Problem: concatenate labeled Series, controlling axis and overlap handling.
    Why: `pd.concat` glues values AND indexes. Along axis="index" (default) it
    returns a Series; along axis="columns" it returns a DataFrame, aligning the
    other axis with an outer (union) join by default. `join="inner"` intersects.
    """
    print("== pd.concat with Series (axis, join) ==")

    s1 = pd.Series([0, 1], index=["a", "b"], dtype="Int64")
    s2 = pd.Series([2, 3, 4], index=["c", "d", "e"], dtype="Int64")
    s3 = pd.Series([5, 6], index=["f", "g"], dtype="Int64")

    # Default: stack along the index, producing a longer Series.
    print(pd.concat([s1, s2, s3]))
    # axis="columns" aligns on the other axis -> a DataFrame (union of indexes).
    print(pd.concat([s1, s2, s3], axis="columns"))

    # With overlap, choose inner to intersect the other axis.
    s4 = pd.concat([s1, s3])
    print(pd.concat([s1, s4], axis="columns"))
    print(pd.concat([s1, s4], axis="columns", join="inner"))


def explain_concat_keys() -> None:
    """
    Problem: keep track of which piece each concatenated chunk came from.
    Why: the `keys` argument creates a hierarchical index on the concatenation
    axis (or column headers when concatenating along the columns). Passing a dict
    instead of a list uses its keys for `keys`.
    """
    print("== pd.concat with keys (identifiable pieces) ==")

    s1 = pd.Series([0, 1], index=["a", "b"], dtype="Int64")
    s2 = pd.Series([2, 3, 4], index=["c", "d", "e"], dtype="Int64")
    s3 = pd.Series([5, 6], index=["f", "g"], dtype="Int64")

    # keys form an outer hierarchical index on the row axis.
    result = pd.concat([s1, s1, s3], keys=["one", "two", "three"])
    print(result)
    print(result.unstack())  # the keys become the outer row level

    # Along the columns, the keys become the column headers.
    print(pd.concat([s1, s2, s3], axis="columns", keys=["one", "two", "three"]))

    # The same logic extends to DataFrames.
    df1 = pd.DataFrame(np.arange(6).reshape(3, 2), index=["a", "b", "c"], columns=["one", "two"])
    df2 = pd.DataFrame(5 + np.arange(4).reshape(2, 2), index=["a", "c"], columns=["three", "four"])
    print(pd.concat([df1, df2], axis="columns", keys=["level1", "level2"]))
    # A dict's keys are used for the keys option.
    print(pd.concat({"level1": df1, "level2": df2}, axis="columns"))
    # names labels the created hierarchical column levels.
    print(
        pd.concat(
            [df1, df2], axis="columns", keys=["level1", "level2"], names=["upper", "lower"]
        )
    )


def explain_ignore_index() -> None:
    """
    Problem: concatenate frames whose row index carries no useful information.
    Why: `ignore_index=True` discards each frame's index and assigns a fresh
    default RangeIndex, aligning purely on the (union of) column labels.
    """
    print("== pd.concat with ignore_index ==")

    rng = np.random.default_rng(seed=12345)
    df1 = pd.DataFrame(rng.standard_normal((3, 4)), columns=["a", "b", "c", "d"])
    df2 = pd.DataFrame(rng.standard_normal((2, 3)), columns=["b", "d", "a"])
    print(df1)
    print(df2)
    # Drop the row indexes and renumber from 0; columns still align by name.
    print(pd.concat([df1, df2], ignore_index=True))


def explain_combine_first() -> None:
    """
    Problem: splice two overlapping datasets, filling gaps from the other.
    Why: `np.where(cond, b, a)` is the array-oriented if-else but ignores index
    alignment. To line values up BY index, use `combine_first`, which patches
    missing values in the calling object with values from the passed object. For
    DataFrames it does this column by column, taking the union of columns.
    """
    print("== Combining data with overlap (np.where, combine_first) ==")

    a = pd.Series([np.nan, 2.5, 0.0, 3.5, 4.5, np.nan], index=["f", "e", "d", "c", "b", "a"])
    b = pd.Series([0.0, np.nan, 2.0, np.nan, np.nan, 5.0], index=["a", "b", "c", "d", "e", "f"])
    print(a)
    print(b)

    # Pick from b where a is null, else from a (no index alignment here).
    print(np.where(pd.isna(a), b, a))
    # combine_first aligns on the index and patches a's gaps from b.
    print(a.combine_first(b))

    # DataFrames: patch column by column, union of all columns.
    df1 = pd.DataFrame(
        {"a": [1.0, np.nan, 5.0, np.nan], "b": [np.nan, 2.0, np.nan, 6.0], "c": range(2, 18, 4)}
    )
    df2 = pd.DataFrame({"a": [5.0, 4.0, np.nan, 3.0, 7.0], "b": [np.nan, 3.0, 4.0, 6.0, 8.0]})
    print(df1)
    print(df2)
    print(df1.combine_first(df2))


def main() -> None:
    explain_numpy_concatenate()
    explain_concat_series()
    explain_concat_keys()
    explain_ignore_index()
    explain_combine_first()


main()
