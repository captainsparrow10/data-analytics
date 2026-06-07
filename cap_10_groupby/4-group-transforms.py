"""
Group Transforms and "Unwrapped" GroupBys (Section 10.4)

`transform` is similar to `apply` but imposes more constraints on the function:
it can produce a scalar to be *broadcast* to the shape of the group, or an
object of the *same shape* as the input group, and it must not mutate its input.
This makes it ideal for producing a result aligned to the original rows — e.g.
replacing each value with its group mean, ranking within groups, or normalizing.

This file covers `transform` with scalar-producing functions (broadcast),
same-shape functions, string aliases for the built-in aggregations, a custom
normalization, and "unwrapped" group operations — doing arithmetic between the
outputs of several GroupBy operations instead of writing one apply function,
which often vectorizes faster.

KEY OPERATIONS IN THIS FILE
METHOD/CONCEPT       DESCRIPTION
transform(func)      Apply func per group, aligning the result to the input rows
transform("mean")    String alias uses the optimized aggregation, then broadcasts
unwrapped op         Combine GroupBy outputs with arithmetic (vectorized fast path)

Run:
    poetry run python cap_10_groupby/4-group-transforms.py
"""

import pandas as pd
import numpy as np


def _example_frame() -> pd.DataFrame:
    """The book's small key/value frame: keys a,b,c repeated, values 0..11."""
    return pd.DataFrame({"key": ["a", "b", "c"] * 4, "value": np.arange(12.0)})


def explain_transform_basics() -> None:
    """
    Problem: build a Series the same shape as a column but with values replaced
    by the group statistic.
    Why: `transform` runs a function per group and aligns the output back to the
    original rows. A function returning a scalar (the group mean) is broadcast to
    every row of its group; the string alias "mean" does the same via the fast,
    optimized aggregation path.
    """
    print("== transform basics: broadcasting a group statistic ==")

    df = _example_frame()
    print(df)

    g = df.groupby("key")["value"]
    print(g.mean())  # one value per group (the aggregation)

    # transform broadcasts each group's mean back across that group's rows.
    def get_mean(group: pd.Series) -> float:
        return group.mean()

    print(g.transform(get_mean))
    # Built-in aggregations can be named by their string alias (fast path).
    print(g.transform("mean"))


def explain_transform_same_shape() -> None:
    """
    Problem: transform with functions that return a Series the same size as input.
    Why: `transform` also accepts functions returning a same-shaped object, as
    long as the size matches — e.g. multiplying each group by 2, or ranking each
    group's values in descending order.
    """
    print("== transform with same-shape functions ==")

    df = _example_frame()
    g = df.groupby("key")["value"]

    def times_two(group: pd.Series) -> pd.Series:
        return group * 2

    print(g.transform(times_two))

    def get_ranks(group: pd.Series) -> pd.Series:
        return group.rank(ascending=False)

    print(g.transform(get_ranks))


def explain_transform_vs_apply_normalize() -> None:
    """
    Problem: normalize values within each group (subtract mean, divide by std).
    Why: a transformation composed from simple aggregations gives the same result
    through `transform` or `apply` here. transform aligns automatically to the
    rows, which is exactly what within-group normalization needs.
    """
    print("== transform vs apply: group normalization ==")

    df = _example_frame()
    g = df.groupby("key")["value"]

    def normalize(x: pd.Series) -> pd.Series:
        return (x - x.mean()) / x.std()

    print(g.transform(normalize))
    print(g.apply(normalize))


def explain_unwrapped_group_operation() -> None:
    """
    Problem: get the normalization result while leaning on the fast aggregation
    path.
    Why: built-in aggregations like "mean"/"std" have an optimized "fast path"
    under `transform`. Doing arithmetic directly between the broadcast outputs of
    several GroupBy operations — instead of writing a function for apply — is an
    "unwrapped" group operation, and the vectorized math often outperforms a
    general apply.
    """
    print("== Unwrapped group operation ==")

    df = _example_frame()
    g = df.groupby("key")["value"]

    print(g.transform("mean"))
    # Arithmetic between two transform outputs reproduces normalize, vectorized.
    normalized = (df["value"] - g.transform("mean")) / g.transform("std")
    print(normalized)


def main() -> None:
    explain_transform_basics()
    explain_transform_same_shape()
    explain_transform_vs_apply_normalize()
    explain_unwrapped_group_operation()


main()
