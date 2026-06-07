"""
Essential Functionality, Part 2: Apply, Sort, Rank (Section 5.2)

This file covers applying functions to pandas objects and ordering their data.
NumPy ufuncs work element-wise on DataFrames; `apply` runs a function along an
axis (and may return a scalar or a whole Series per column/row); `map` applies
an element-wise Python function to every cell of a DataFrame or every value of a
Series. Sorting is done with `sort_index` (by labels) and `sort_values` (by the
data); ranking assigns 1..N ranks with configurable tie-breaking. The file ends
with how selection behaves when axis labels are NOT unique.

RANK TIE-BREAKING METHODS
METHOD     DESCRIPTION
average    Default: average rank assigned to each member of an equal group
min        Use the minimum rank for the whole group
max        Use the maximum rank for the whole group
first      Assign ranks in the order the values appear in the data
dense      Like "min", but ranks increase by 1 between groups (no gaps)

Run:
    poetry run python cap_03_panda/5-function-sorting-ranking.py
"""

import numpy as np
import pandas as pd


def explain_function_application() -> None:
    """
    Problem: apply NumPy and Python functions across a DataFrame.
    Why: ufuncs operate element-wise; `apply` runs a function once per column
    (default) or per row (axis="columns") and can return a scalar OR a Series;
    `map` formats every element. (In pandas 3.0 `DataFrame.applymap` was removed
    in favor of `DataFrame.map`.)
    """
    print("== Function application and mapping ==")

    rng = np.random.default_rng(seed=12345)
    frame = pd.DataFrame(
        rng.standard_normal((4, 3)),
        columns=list("bde"),
        index=["Utah", "Ohio", "Texas", "Oregon"],
    )
    print(frame)
    print(np.abs(frame))  # a ufunc applied element-wise

    # apply runs a function over one-dimensional slices: once per column...
    def f1(x: pd.Series) -> float:
        return float(x.max() - x.min())

    print(frame.apply(f1))                    # one value per column
    print(frame.apply(f1, axis="columns"))    # one value per row

    # The function passed to apply may return a Series with multiple values.
    def f2(x: pd.Series) -> pd.Series:
        return pd.Series([x.min(), x.max()], index=["min", "max"])

    print(frame.apply(f2))

    # Element-wise formatting: DataFrame.map (was applymap) and Series.map.
    def my_format(x: float) -> str:
        return f"{x:.2f}"

    # pandas 3.0: applymap was removed, use DataFrame.map for element-wise work.
    print(frame.map(my_format))
    print(frame["e"].map(my_format))  # Series.map applies element-wise too


def explain_sorting_and_ranking() -> None:
    """
    Problem: order data by labels or by values, and assign ranks.
    Why: `sort_index` sorts lexicographically by row/column label on either
    axis; `sort_values` sorts by the data (NaNs go to the end by default, or to
    the front with na_position="first"); `rank` numbers values 1..N, breaking
    ties by the chosen method.
    """
    print("== Sorting and ranking ==")

    obj = pd.Series(np.arange(4), index=["d", "a", "b", "c"])
    print(obj.sort_index())  # sort by the index labels

    frame = pd.DataFrame(
        np.arange(8).reshape((2, 4)),
        index=["three", "one"],
        columns=["d", "a", "b", "c"],
    )
    print(frame.sort_index())                              # sort rows by label
    print(frame.sort_index(axis="columns"))               # sort columns by label
    print(frame.sort_index(axis="columns", ascending=False))

    # sort_values orders by the data; missing values sort to the end by default.
    obj2 = pd.Series([4, np.nan, 7, np.nan, -3, 2])
    print(obj2.sort_values())
    print(obj2.sort_values(na_position="first"))  # NaNs first instead

    # For a DataFrame, sort by one or more columns with `by`.
    frame2 = pd.DataFrame({"b": [4, 7, -3, 2], "a": [0, 1, 0, 1]})
    print(frame2.sort_values("b"))
    print(frame2.sort_values(["a", "b"]))

    # rank assigns ranks 1..N; the default "average" splits ties evenly.
    obj3 = pd.Series([7, -5, 7, 4, 2, 0, 4])
    print(obj3.rank())                  # average rank for ties
    print(obj3.rank(method="first"))    # ranks follow the data order
    print(obj3.rank(ascending=False))   # largest value ranks first


def explain_duplicate_labels() -> None:
    """
    Problem: understand selection when axis labels repeat.
    Why: `index.is_unique` reports whether labels are unique. Selecting a label
    that occurs multiple times returns ALL matches (a Series/DataFrame), while a
    unique label returns a scalar/row — so the output TYPE can vary.
    """
    print("== Axis indexes with duplicate labels ==")

    obj = pd.Series(np.arange(5), index=["a", "a", "b", "b", "c"])
    print(obj)
    print(obj.index.is_unique)  # False -> there are duplicate labels

    # A duplicated label returns every match; a unique one returns a scalar.
    print(obj["a"])  # Series with both "a" entries
    print(obj["c"])  # scalar value 4

    rng = np.random.default_rng(seed=12345)
    df = pd.DataFrame(rng.standard_normal((5, 3)), index=["a", "a", "b", "b", "c"])
    print(df.loc["b"])  # both "b" rows as a DataFrame
    print(df.loc["c"])  # the single "c" row as a Series


def main() -> None:
    explain_function_application()
    explain_sorting_and_ranking()
    explain_duplicate_labels()


main()
