"""
Categorical Data (Section 7.5)

Frequently a column contains repeated instances of a smaller set of distinct
values. Data systems use *dimension tables* that store the distinct values once
and reference them with integer keys — the *categorical* (or dictionary-encoded)
representation: the distinct values are the *categories* and the integer
references are the *codes*. pandas has a `Categorical` extension type built on
this idea, giving large memory savings and faster GroupBy operations for data
with many repeats. This file covers the background, the Categorical type, doing
computations with categoricals, and the `.cat` accessor methods.

CATEGORICAL METHODS FOR SERIES (the .cat accessor)
METHOD                     DESCRIPTION
codes / categories         Integer codes / the array of distinct categories
set_categories             Replace the categories; can add or remove categories
remove_unused_categories   Remove categories not present in the data
add_categories             Append new (unused) categories at the end
as_ordered / as_unordered  Make the categories ordered / unordered
rename_categories          Replace category names (cannot change their number)

Run:
    poetry run python cap_07_cleaning/6-categorical-data.py
"""

import numpy as np
import pandas as pd


def explain_background() -> None:
    """
    Problem: represent a column of repeated values compactly.
    Why: `unique`/`value_counts` extract the distinct values and their counts; the
    dimension-table idea stores those distinct values once (the dimension) and the
    observations as integer keys into it. `take` reconstructs the original Series
    from the keys and the dimension — exactly the categorical representation.
    """
    print("== Background and motivation ==")

    values = pd.Series(["apple", "orange", "apple", "apple"] * 2)
    print(values)
    print(values.unique())          # distinct values
    print(values.value_counts())    # their frequencies

    # Dimension table: integer keys referencing a small set of distinct values.
    values = pd.Series([0, 1, 0, 0] * 2)
    dim = pd.Series(["apple", "orange"])
    print(dim.take(values))         # restore the original strings


def explain_categorical_type() -> None:
    """
    Problem: build and inspect the pandas Categorical extension type.
    Why: converting a column with `astype("category")` yields a `Categorical`
    exposing `.categories` and `.codes`. You can also build one directly with
    `pd.Categorical`, or from existing codes with `pd.Categorical.from_codes`
    (passing `ordered=True` when the categories have a meaningful order).
    """
    print("== Categorical extension type in pandas ==")

    fruits = ["apple", "orange", "apple", "apple"] * 2
    n = len(fruits)
    rng = np.random.default_rng(seed=12345)
    df = pd.DataFrame(
        {
            "fruit": fruits,
            "basket_id": np.arange(n),
            "count": rng.integers(3, 15, size=n),
            "weight": rng.uniform(0, 4, size=n),
        },
        columns=["basket_id", "fruit", "count", "weight"],
    )
    print(df)

    # Convert a column of strings to categorical.
    fruit_cat = df["fruit"].astype("category")
    print(fruit_cat)
    c = fruit_cat.array            # the underlying Categorical object
    # The stub types .array as the generic ExtensionArray; assert the concrete
    # Categorical so its categories/codes attributes resolve.
    assert isinstance(c, pd.Categorical)
    print(type(c))
    print(c.categories)            # Index(['apple', 'orange'])
    print(c.codes)                 # integer code per element
    print(dict(enumerate(c.categories)))   # mapping codes -> categories

    # Build a Categorical directly from a Python sequence.
    my_categories = pd.Categorical(["foo", "bar", "baz", "foo", "bar"])
    print(my_categories)

    # Build from existing codes + categories; ordered=True gives a meaningful order.
    categories = ["foo", "bar", "baz"]
    codes = [0, 1, 2, 0, 0, 1]
    my_cats_2 = pd.Categorical.from_codes(codes, categories)
    print(my_cats_2)
    ordered_cat = pd.Categorical.from_codes(codes, categories, ordered=True)
    print(ordered_cat)                     # foo < bar < baz
    print(my_cats_2.as_ordered())          # make an unordered one ordered


def explain_computations_with_categoricals() -> None:
    """
    Problem: use categoricals in real computations.
    Why: `pd.qcut` returns a Categorical; with `labels` the bins get readable
    names (Q1..Q4). The labeled categorical drops the bin-edge info, so we use
    `groupby` to extract summary statistics, and the resulting "quartile" column
    keeps the categorical ordering. Categoricals also yield large memory savings
    and faster value_counts/GroupBy on big data.
    """
    print("== Computations with categoricals ==")

    rng = np.random.default_rng(seed=12345)
    draws = rng.standard_normal(1000)
    print(draws[:5])

    # qcut returns a Categorical of quantile bins; labels names them Q1..Q4.
    bins = pd.qcut(draws, 4, labels=["Q1", "Q2", "Q3", "Q4"])
    print(pd.Series(bins).value_counts())
    print(pd.Series(bins).cat.codes[:10])

    # The labeled bins drop the edges, so groupby recovers per-bin statistics.
    bins_s = pd.Series(bins, name="quartile")
    results = (
        pd.Series(draws).groupby(bins_s).agg(["count", "min", "max"]).reset_index()
    )
    print(results)
    print(results["quartile"])     # retains the categorical ordering

    # Memory savings: categorical uses far less memory than object strings.
    n = 1_000_000
    labels = pd.Series(["foo", "bar", "baz", "qux"] * (n // 4))
    categories = labels.astype("category")
    print(labels.memory_usage(deep=True))
    print(categories.memory_usage(deep=True))


def explain_categorical_methods() -> None:
    """
    Problem: manage the set of categories independently of the data.
    Why: the `.cat` accessor exposes `codes`/`categories` plus category management.
    `set_categories` declares a wider category set (reflected by `value_counts`);
    `remove_unused_categories` trims categories absent after filtering — both common
    when slicing large categorical datasets.
    """
    print("== Categorical methods (the .cat accessor) ==")

    s = pd.Series(["a", "b", "c", "d"] * 2)
    cat_s = s.astype("category")
    print(cat_s.cat.codes)
    print(cat_s.cat.categories)

    # Declare categories beyond those observed in the data.
    actual_categories = ["a", "b", "c", "d", "e"]
    cat_s2 = cat_s.cat.set_categories(actual_categories)
    print(cat_s2)
    print(cat_s.value_counts())            # only observed categories
    print(cat_s2.value_counts())           # "e" appears with count 0

    # After filtering, drop categories that no longer appear.
    # .loc keeps the result typed as a Series (plain [] is typed as ndarray here).
    cat_s3 = cat_s.loc[cat_s.isin(["a", "b"])]
    print(cat_s3)
    print(cat_s3.cat.remove_unused_categories())

    # get_dummies on a categorical builds the one-hot indicator matrix.
    cat_s = pd.Series(["a", "b", "c", "d"] * 2, dtype="category")
    print(pd.get_dummies(cat_s, dtype=int))


def main() -> None:
    explain_background()
    explain_categorical_type()
    explain_computations_with_categoricals()
    explain_categorical_methods()


main()
