"""
Data Aggregation: Optimized Methods and Custom Functions (Section 10.2)

*Aggregations* refer to any data transformation that produces scalar values from
arrays — `mean`, `count`, `min`, `sum`, and friends. Many common aggregations
have optimized implementations on GroupBy, but you are not limited to them: any
function that aggregates an array can be passed to `aggregate` (alias `agg`),
and you can apply several functions at once, name the outputs, or apply a
different function per column.

This file covers the built-in aggregation methods, custom `agg` functions, the
`describe` shortcut, column-wise and multiple-function application (a list or a
dict of functions, plus (name, function) tuples for custom output names), and
returning aggregated data without the group keys as the row index
(`as_index=False` / `reset_index`).

OPTIMIZED GROUPBY METHODS (Table 10-1, selection)
NAME              DESCRIPTION
count             Number of non-NA values in the group
sum / mean        Sum / arithmetic mean of non-NA values
median            Arithmetic median of non-NA values
std, var          Sample standard deviation and variance
min, max          Minimum and maximum of non-NA values
prod              Product of non-NA values
first, last       First and last non-NA values
nth               The value that would appear at position n if sorted

Run:
    poetry run python cap_10_groupby/2-data-aggregation.py
"""

import numpy as np
import pandas as pd


def _example_frame() -> pd.DataFrame:
    """The book's key1/key2/data1/data2 DataFrame, deterministic via default_rng."""
    rng = np.random.default_rng(seed=12345)
    return pd.DataFrame(
        {
            "key1": ["a", "a", None, "b", "b", "a", None],
            "key2": pd.Series([1, 2, 1, 2, 1, None, 1], dtype="Int64"),
            "data1": rng.standard_normal(7),
            "data2": rng.standard_normal(7),
        }
    )


def _tips() -> pd.DataFrame:
    """
    Build a small tips-like DataFrame in code (the book loads examples/tips.csv).

    It carries the columns the chapter's examples use — total_bill, tip, smoker,
    day, time, size — and we add the derived tip_pct column where the book does.
    Values are generated deterministically so output is reproducible offline.
    """
    rng = np.random.default_rng(seed=10)
    n = 200
    days = rng.choice(["Fri", "Sat", "Sun", "Thur"], size=n, p=[0.1, 0.35, 0.3, 0.25])
    times = np.where(np.isin(days, ["Fri", "Thur"]), rng.choice(["Lunch", "Dinner"], size=n), "Dinner")
    total_bill = np.round(rng.gamma(shape=6.0, scale=3.3, size=n) + 3.0, 2)
    smoker = rng.choice(["No", "Yes"], size=n, p=[0.62, 0.38])
    size = rng.integers(1, 7, size=n)
    # Tip is a noisy fraction of the bill (roughly 12%-22%).
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
    # The book adds tip_pct = tip / total_bill right after loading the data.
    tips["tip_pct"] = tips["tip"] / tips["total_bill"]
    return tips


def explain_builtin_and_custom_aggregations() -> None:
    """
    Problem: aggregate groups with both optimized methods and your own functions.
    Why: besides the optimized methods in Table 10-1, you can call any method
    defined on the grouped object (e.g. `nsmallest`, via a non-optimized path),
    and pass any array->scalar function to `agg`. Custom functions are slower
    than the optimized ones because of per-group call/rearrangement overhead.
    """
    print("== Built-in methods, nsmallest, and custom agg functions ==")

    df = _example_frame()
    grouped = df.groupby("key1")

    # nsmallest is not an optimized GroupBy method but still works per group.
    print(grouped["data1"].nsmallest(2))

    # A custom aggregation: range (max - min) of each group, passed to agg.
    def peak_to_peak(arr: pd.Series) -> float:
        return arr.max() - arr.min()

    print(grouped[["data1", "data2"]].agg(peak_to_peak))

    # describe also works on a GroupBy, though it is not a single aggregation.
    print(grouped[["data1", "data2"]].describe())


def explain_column_wise_multiple_functions() -> None:
    """
    Problem: apply several functions, possibly named, to grouped columns.
    Why: passing the NAME of a function as a string uses the optimized method;
    passing a LIST of functions returns a DataFrame whose columns are named after
    the functions; passing (name, function) tuples lets you choose the output
    names (handy because lambdas are unhelpfully named "<lambda>").
    """
    print("== Column-wise and multiple function application ==")

    tips = _tips()
    grouped = tips.groupby(["day", "smoker"])
    grouped_pct = grouped["tip_pct"]

    # A single function by its string name.
    print(grouped_pct.agg("mean"))

    # A list of functions/names -> columns named after each function.
    def peak_to_peak(arr: pd.Series) -> float:
        return arr.max() - arr.min()

    print(grouped_pct.agg(["mean", "std", peak_to_peak]))

    # (name, function) tuples give custom column names. (np.std is replaced by
    # the string "std" — passing the bare numpy ufunc to agg is deprecated.)
    print(grouped_pct.agg([("average", "mean"), ("stdev", "std")]))


def explain_functions_per_column() -> None:
    """
    Problem: apply the same functions to several columns, or different functions
    per column.
    Why: with a DataFrame GroupBy you can pass a list of functions to apply to
    every selected column (producing hierarchical columns), a list of (name, fn)
    tuples for custom names, or a DICT mapping each column to its own function(s).
    """
    print("== Same functions across columns, and per-column functions ==")

    tips = _tips()
    grouped = tips.groupby(["day", "smoker"])

    # The same three statistics for two columns -> hierarchical columns.
    functions = ["count", "mean", "max"]
    result = grouped[["tip_pct", "total_bill"]].agg(functions)
    print(result)
    print(result["tip_pct"])  # select one top-level column group

    # Custom names via (name, function) tuples. (np.var -> the string "var".)
    ftuples = [("Average", "mean"), ("Variance", "var")]
    print(grouped[["tip_pct", "total_bill"]].agg(ftuples))

    # A dict maps each column to its own function(s). (np.max -> "max".)
    print(grouped.agg({"tip": "max", "size": "sum"}))
    print(grouped.agg({"tip_pct": ["min", "max", "mean", "std"], "size": "sum"}))


def explain_returning_data_without_row_indexes() -> None:
    """
    Problem: get aggregated data back with the group keys as columns, not as the
    (possibly hierarchical) row index.
    Why: by default aggregation puts the unique group keys in the row index.
    Passing `as_index=False` to groupby keeps them as columns instead and avoids
    some unnecessary index computations; `reset_index` on the result is the
    always-available alternative.
    """
    print("== Returning aggregated data without row indexes ==")

    tips = _tips()
    # Only numeric columns are aggregated; keys stay as plain columns.
    numeric = tips[["day", "smoker", "total_bill", "tip", "size", "tip_pct"]]
    print(numeric.groupby(["day", "smoker"], as_index=False).mean())

    # Equivalent result via reset_index on the default (indexed) aggregation.
    # .mean() is typed broadly; narrow to a DataFrame so .reset_index() resolves.
    aggregated = numeric.groupby(["day", "smoker"]).mean()
    assert isinstance(aggregated, pd.DataFrame)
    print(aggregated.reset_index())


def main() -> None:
    explain_builtin_and_custom_aggregations()
    explain_column_wise_multiple_functions()
    explain_functions_per_column()
    explain_returning_data_without_row_indexes()


main()
