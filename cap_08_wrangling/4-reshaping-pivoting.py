"""
Reshaping and Pivoting (Section 8.3)

There are a number of basic operations for rearranging tabular data, referred to
as *reshape* or *pivot* operations. Hierarchical indexing provides a consistent
way to reshape: `stack` rotates columns into rows, and `unstack` pivots rows into
columns. On top of that, `pivot` turns "long" (stacked) data into "wide" form,
and `melt` is its inverse, merging multiple columns into one to make data longer.

This file covers reshaping with hierarchical indexing (`stack`/`unstack`,
including `level=` selection and the `dropna` behavior), pivoting long-to-wide
with `pivot`, and pivoting wide-to-long with `melt`.

KEY OPERATIONS IN THIS FILE
METHOD          DESCRIPTION
stack           Pivot columns into a (new innermost) row level
unstack         Pivot a row level into columns; level= picks which level
pivot           Long -> wide: (index, columns, values) build a wide table
melt            Wide -> long: collapse value columns into one, keeping id_vars

Run:
    poetry run python cap_08_wrangling/4-reshaping-pivoting.py
"""

import numpy as np
import pandas as pd


def explain_stack_unstack_basics() -> None:
    """
    Problem: rotate a small DataFrame between wide and long shapes.
    Why: `stack` pivots the columns into the rows, producing a hierarchically
    indexed Series; `unstack` rearranges it back into a DataFrame. By default the
    INNERMOST level is (un)stacked, but you can target a different level by
    passing a level number or name.
    """
    print("== stack / unstack basics (level selection) ==")

    data = pd.DataFrame(
        np.arange(6).reshape((2, 3)),
        index=pd.Index(["Ohio", "Colorado"], name="state"),
        columns=pd.Index(["one", "two", "three"], name="number"),
    )
    print(data)

    # stack pivots the columns into an inner row level -> a Series.
    result = data.stack()
    print(result)
    # unstack rearranges it back into a DataFrame.
    print(result.unstack())
    # Unstack a specific level by number or by name.
    print(result.unstack(level=0))
    print(result.unstack(level="state"))


def explain_stack_dropna() -> None:
    """
    Problem: understand the missing-data behavior of stack/unstack.
    Why: unstacking can introduce NaN when a level value is absent from some
    subgroups. In the book's older pandas, `stack` dropped those missing values by
    default and `dropna=False` kept them. pandas 3.0 reworked `stack`: it now
    KEEPS the NA placeholders and the `dropna` argument was removed (it raises if
    passed), so to drop the gaps you filter explicitly with `dropna()`.
    """
    print("== stack/unstack and missing data (dropna) ==")

    s1 = pd.Series([0, 1, 2, 3], index=["a", "b", "c", "d"], dtype="Int64")
    s2 = pd.Series([4, 5, 6], index=["c", "d", "e"], dtype="Int64")
    data2 = pd.concat([s1, s2], keys=["one", "two"])
    print(data2)

    # Unstacking introduces <NA> where a label is missing in a subgroup.
    print(data2.unstack())
    # The new (pandas 3.0) stack keeps the <NA> placeholders.
    print(data2.unstack().stack())
    # Drop the gaps explicitly to recover the original, NA-free Series.
    print(data2.unstack().stack().dropna())


def explain_unstack_in_dataframe() -> None:
    """
    Problem: unstack/stack a chosen level when the data is already a DataFrame.
    Why: when you unstack in a DataFrame, the unstacked level becomes the LOWEST
    level in the resulting columns. As with unstack, when calling stack you can
    name which axis level to stack.
    """
    print("== unstack/stack a named level in a DataFrame ==")

    data = pd.DataFrame(
        np.arange(6).reshape((2, 3)),
        index=pd.Index(["Ohio", "Colorado"], name="state"),
        columns=pd.Index(["one", "two", "three"], name="number"),
    )
    result = data.stack()
    df = pd.DataFrame(
        {"left": result, "right": result + 5},
        columns=pd.Index(["left", "right"], name="side"),
    )
    print(df)
    # The unstacked "state" level becomes the lowest level in the columns.
    print(df.unstack(level="state"))
    # Stack a named axis level back down.
    print(df.unstack(level="state").stack(level="side"))


def explain_pivot_long_to_wide() -> None:
    """
    Problem: reshape "long" (stacked) time series into "wide" columns.
    Why: long format stores one observation per row (date, item, value) — common
    in SQL. `DataFrame.pivot(index, columns, values)` turns the distinct `item`
    values into columns indexed by `date`. Omitting `values` with several value
    columns yields hierarchical columns. (The book loads examples/macrodata.csv;
    here we build a tiny equivalent inline so the file runs offline.)
    """
    print("== Pivoting long to wide (pivot) ==")

    # A tiny stand-in for the book's macrodata, in long format.
    data = pd.DataFrame(
        {
            "year": [1959, 1959, 1959, 1960],
            "quarter": [1, 2, 3, 1],
            "realgdp": [2710.349, 2778.801, 2775.488, 2847.699],
            "infl": [0.00, 2.34, 2.74, 2.31],
            "unemp": [5.8, 5.1, 5.3, 5.2],
        }
    )
    # Build a PeriodIndex from year+quarter, then a daily timestamp (book In [147]).
    # pandas 3.0 replaced the PeriodIndex(year=, quarter=) constructor with the
    # PeriodIndex.from_fields factory (which has no `name`, so we rename after).
    periods = pd.PeriodIndex.from_fields(
        year=data.pop("year"), quarter=data.pop("quarter"), freq="Q"
    ).rename("date")
    data.index = periods.to_timestamp("D")
    data.columns.name = "item"
    print(data.head())

    # Reshape to long format: stack -> reset_index -> name the value column.
    long_data = (
        data.stack().reset_index().rename(columns={0: "value"})
    )
    print(long_data[:10])

    # pivot turns the item values into columns, indexed by date.
    pivoted = long_data.pivot(index="date", columns="item", values="value")
    print(pivoted.head())

    # With two value columns and no `values`, the result has hierarchical columns.
    rng = np.random.default_rng(seed=12345)
    long_data["value2"] = rng.standard_normal(len(long_data))
    pivoted2 = long_data.pivot(index="date", columns="item")
    print(pivoted2.head())
    print(pivoted2["value"].head())

    # pivot is equivalent to set_index followed by unstack.
    unstacked = long_data.set_index(["date", "item"]).unstack(level="item")
    print(unstacked.head())


def explain_melt_wide_to_long() -> None:
    """
    Problem: collapse several value columns into a single one (wide -> long).
    Why: `pandas.melt` is the inverse of `pivot`: it merges multiple columns into
    one, producing a longer frame. `id_vars` marks the group-indicator columns to
    keep; `value_vars` optionally restricts which columns are melted. With `pivot`
    you can reshape back, then `reset_index` to move the row labels into a column.
    """
    print("== Pivoting wide to long (melt) ==")

    df = pd.DataFrame(
        {"key": ["foo", "bar", "baz"], "A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}
    )
    print(df)

    # "key" is the group indicator; A/B/C become rows under variable/value.
    melted = pd.melt(df, id_vars="key")
    print(melted)

    # Reshape back with pivot, then move the row labels into a column.
    reshaped = melted.pivot(index="key", columns="variable", values="value")
    print(reshaped)
    print(reshaped.reset_index())

    # Restrict which columns are melted with value_vars.
    print(pd.melt(df, id_vars="key", value_vars=["A", "B"]))
    # melt works without any group identifiers too.
    print(pd.melt(df, value_vars=["A", "B", "C"]))
    print(pd.melt(df, value_vars=["key", "A", "B"]))


def main() -> None:
    explain_stack_unstack_basics()
    explain_stack_dropna()
    explain_unstack_in_dataframe()
    explain_pivot_long_to_wide()
    explain_melt_wide_to_long()


main()
