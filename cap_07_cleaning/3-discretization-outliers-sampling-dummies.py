"""
Discretization, Outliers, Sampling, and Dummy Variables (Section 7.2, part 2)

The second half of section 7.2 covers four common modeling transformations:
discretizing continuous data into bins (`pd.cut`, `pd.qcut`, with `labels`,
`right`, `precision`), detecting and filtering/capping outliers with array
operations, permutation and random sampling (`permutation`, `take`, `sample`),
and computing indicator/dummy variables (`pd.get_dummies`, including the
multiple-membership movies/genres example via `str.get_dummies`).

KEY FUNCTIONS IN THIS FILE
FUNCTION             DESCRIPTION
pd.cut               Bin values into intervals defined by explicit or equal-width edges
pd.qcut              Bin values into roughly equal-size groups using sample quantiles
take                 Reorder/select rows by an array of integer positions
sample               Draw a random subset of rows (with or without replacement)
pd.get_dummies       Convert a categorical column into a 0/1 (boolean) indicator matrix
str.get_dummies      Indicator matrix from a delimited multiple-membership string

Run:
    poetry run python cap_07_cleaning/3-discretization-outliers-sampling-dummies.py
"""

import numpy as np
import pandas as pd


def explain_discretization_and_binning() -> None:
    """
    Problem: group continuous values into discrete buckets.
    Why: `pd.cut` bins by explicit edges, returning a Categorical of interval
    labels (a parenthesis is open/exclusive, a bracket is closed/inclusive); the
    `.codes`/`.categories` attributes expose the encoding. `right=False` flips
    which side is closed, `labels=` names the bins, an integer count makes
    equal-width bins, and `precision` limits the decimals. `pd.qcut` instead bins
    by sample quantiles, yielding roughly equal-size groups.
    """
    print("== Discretization and binning ==")

    ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
    bins = [18, 25, 35, 60, 100]
    age_categories = pd.cut(ages, bins)
    # With an array-like input, pd.cut returns a Categorical at runtime; assert it
    # so the loosely-typed stub union narrows for the attribute access below.
    assert isinstance(age_categories, pd.Categorical)
    print(age_categories)
    print(age_categories.codes)            # integer code per value
    print(age_categories.categories)       # the IntervalIndex of bins
    # pandas 3.0: the top-level pd.value_counts was removed; use the method.
    print(age_categories.value_counts())   # bin counts

    # right=False makes the left side closed: [18, 25) instead of (18, 25].
    print(pd.cut(ages, bins, right=False))

    # Override interval labels with your own names.
    group_names = ["Youth", "YoungAdult", "MiddleAged", "Senior"]
    print(pd.cut(ages, bins, labels=group_names))

    # An integer number of bins makes equal-width bins from the data range.
    rng = np.random.default_rng(seed=12345)
    data = rng.uniform(size=20)
    print(pd.cut(data, 4, precision=2))    # precision limits decimals to 2

    # qcut bins by sample quantiles -> roughly equal-size groups.
    data2 = rng.standard_normal(1000)
    quartiles = pd.qcut(data2, 4, precision=2)
    print(pd.Series(quartiles).value_counts())
    # You can also pass your own quantiles (numbers between 0 and 1).
    print(pd.Series(pd.qcut(data2, [0, 0.1, 0.5, 0.9, 1.0])).value_counts())


def explain_outliers() -> None:
    """
    Problem: find and cap extreme values.
    Why: filtering or transforming outliers is largely a matter of array
    operations. A Boolean test (`col.abs() > 3`) selects extreme values in one
    column; wrapping it with `.any(axis="columns")` selects whole rows with any
    extreme value; and assignment combined with `np.sign` caps values to a range.
    """
    print("== Detecting and filtering outliers ==")

    rng = np.random.default_rng(seed=12345)
    data = pd.DataFrame(rng.standard_normal((1000, 4)))
    print(data.describe())

    # Values in one column exceeding 3 in absolute value.
    col = data[2]
    print(col[col.abs() > 3])

    # Rows having any value exceeding 3 or -3 (parentheses needed before .any()).
    print(data[(data.abs() > 3).any(axis="columns")])

    # Cap values outside the interval -3 to 3. np.sign yields 1/-1 by sign.
    data[data.abs() > 3] = np.sign(data) * 3
    print(data.describe())
    # np.sign on a DataFrame returns a DataFrame at runtime; numpy's stub types it
    # as ndarray, so route through DataFrame.apply to keep the typed .head().
    print(data.apply(np.sign).head())


def explain_permutation_and_sampling() -> None:
    """
    Problem: randomly reorder rows or draw a random sample.
    Why: a random permutation of integer positions (from a seeded generator) can
    drive `take`/`iloc` to reorder rows (or columns via `axis`). `sample` draws a
    random subset without replacement by default, or with `replace=True` to allow
    repeats — useful for bootstrap-style sampling.
    """
    print("== Permutation and random sampling ==")

    df = pd.DataFrame(np.arange(5 * 7).reshape((5, 7)))
    print(df)

    # numpy 2.x: use a Generator; permutation(5) returns a shuffled 0..4 array.
    rng = np.random.default_rng(seed=12345)
    sampler = rng.permutation(5)
    print(sampler)
    print(df.take(sampler))     # reorder rows by integer position
    print(df.iloc[sampler])     # equivalent with iloc

    # Permute columns by passing axis="columns".
    column_sampler = rng.permutation(7)
    print(column_sampler)
    print(df.take(column_sampler, axis="columns"))

    # Random subset without replacement.
    print(df.sample(n=3))

    # Sample WITH replacement (repeat choices allowed).
    choices = pd.Series([5, 7, -1, 6, 4])
    print(choices.sample(n=10, replace=True))


def explain_dummy_variables() -> None:
    """
    Problem: turn a categorical column into an indicator (0/1) matrix.
    Why: `pd.get_dummies` derives a column of indicators per distinct value — a
    standard step for statistical modeling / machine learning. pandas 3.0 returns
    boolean columns by default; pass `dtype=int` for 0/1 integers. A `prefix`
    namespaces the new columns. For multiple membership encoded as a delimited
    string (the MovieLens genres), the Series `str.get_dummies` splits on the
    delimiter. Combining `get_dummies` with `cut` is a handy modeling recipe.
    """
    print("== Computing indicator / dummy variables ==")

    df = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "b"], "data1": range(6)})
    print(df)
    # pandas 3.0 returns boolean columns by default; dtype=int gives 0/1.
    print(pd.get_dummies(df["key"], dtype=int))

    # Add a prefix, then join the dummies back to the original data.
    dummies = pd.get_dummies(df["key"], prefix="key", dtype=int)
    df_with_dummy = df[["data1"]].join(dummies)
    print(df_with_dummy)

    # Multiple-membership: the MovieLens genres column is a "|"-delimited string.
    # The book reads datasets/movielens/movies.dat; we build the same shape inline.
    movies = pd.DataFrame(
        {
            "movie_id": range(1, 11),
            "title": [
                "Toy Story (1995)", "Jumanji (1995)", "Grumpier Old Men (1995)",
                "Waiting to Exhale (1995)", "Father of the Bride Part II (1995)",
                "Heat (1995)", "Sabrina (1995)", "Tom and Huck (1995)",
                "Sudden Death (1995)", "GoldenEye (1995)",
            ],
            "genres": [
                "Animation|Children's|Comedy", "Adventure|Children's|Fantasy",
                "Comedy|Romance", "Comedy|Drama", "Comedy", "Action|Crime|Thriller",
                "Comedy|Romance", "Adventure|Children's", "Action",
                "Action|Adventure|Thriller",
            ],
        }
    )
    print(movies[:10])
    # str.get_dummies splits the delimited string into one indicator per genre.
    genre_dummies = movies["genres"].str.get_dummies("|")
    print(genre_dummies.iloc[:10, :6])
    # Combine with the movies frame, prefixing the genre columns.
    movies_windic = movies.join(genre_dummies.add_prefix("Genre_"))
    print(movies_windic.iloc[0])

    # A useful recipe: combine get_dummies with a discretization like cut.
    rng = np.random.default_rng(seed=12345)
    values = rng.uniform(size=10)
    print(values)
    bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
    print(pd.get_dummies(pd.cut(values, bins), dtype=int))


def main() -> None:
    explain_discretization_and_binning()
    explain_outliers()
    explain_permutation_and_sampling()
    explain_dummy_variables()


main()
