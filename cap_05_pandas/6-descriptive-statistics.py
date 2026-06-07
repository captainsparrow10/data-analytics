"""
Summarizing and Computing Descriptive Statistics (Section 5.3)

pandas objects are equipped with a set of common mathematical and statistical
methods. Most fall into the category of *reductions* or *summary statistics*:
methods that extract a single value (like a sum or mean) from a Series, or a
Series of values from the rows/columns of a DataFrame. Compared with the
equivalent NumPy methods, the pandas versions have built-in handling for missing
data — by default NA values are skipped. This file also covers correlation and
covariance between columns, and the trio for working with the distinct contents
of a column: unique values, value counts, and membership tests.

DESCRIPTIVE / SUMMARY STATISTICS
METHOD     DESCRIPTION
sum        Sum of values (NA skipped unless skipna=False)
mean       Mean of values (needs at least one non-NA value)
idxmax     Index label where the maximum is attained
cumsum     Cumulative sum (an accumulation, not a reduction)
describe   Multiple summary statistics at once (alternative set for non-numeric)
corr / cov Correlation / covariance of overlapping, aligned values
corrwith   Pairwise correlations of a DataFrame's columns with another object

UNIQUE / COUNTS / MEMBERSHIP
unique         Array of distinct values, in order of first appearance
value_counts   Series of value frequencies, sorted descending
isin           Boolean membership test over a collection
get_indexer    Integer indices mapping values into an array of distinct values

Run:
    poetry run python cap_05_pandas/6-descriptive-statistics.py
"""

import numpy as np
import pandas as pd


def explain_summarizing() -> None:
    """
    Problem: reduce a DataFrame to summary statistics, handling missing data.
    Why: sum/mean skip NA by default (skipna=False propagates NA); the `axis`
    argument picks rows vs. columns; idxmax returns the LABEL of the maximum;
    cumsum accumulates; describe reports many statistics at once (and a
    different set for non-numeric data).
    """
    print("== Summarizing and computing reductions ==")

    df = pd.DataFrame(
        [[1.4, np.nan], [7.1, -4.5], [np.nan, np.nan], [0.75, -1.3]],
        index=["a", "b", "c", "d"],
        columns=["one", "two"],
    )
    print(df)
    print(df.sum())                         # column sums (NA skipped) -> Series
    print(df.sum(axis="columns"))           # row sums
    # skipna=False makes any NA in a row/column propagate to the result.
    print(df.sum(axis="index", skipna=False))
    print(df.mean(axis="columns"))          # mean needs >=1 non-NA per row

    print(df.idxmax())                      # label of the max in each column
    print(df.cumsum())                      # cumulative sum down the rows

    # describe gives count/mean/std/min/quartiles/max for numeric data...
    print(df.describe())
    # ...and a different summary (count/unique/top/freq) for non-numeric data.
    obj = pd.Series(["a", "a", "b", "c"] * 4)
    print(obj.describe())


def explain_correlation_and_covariance() -> None:
    """
    Problem: measure how columns move together.
    Why: `corr`/`cov` between two Series use only the overlapping, aligned,
    non-NA values; on a DataFrame they return a full correlation/covariance
    matrix; `corrwith` computes pairwise correlations of every column with
    another Series or DataFrame.
    """
    print("== Correlation and covariance ==")

    # The book downloads Yahoo! Finance data; we synthesize comparable returns
    # with a seeded generator so the output is deterministic and offline.
    rng = np.random.default_rng(seed=12345)
    tickers = ["AAPL", "GOOG", "IBM", "MSFT"]
    returns = pd.DataFrame(
        rng.standard_normal((100, 4)) * 0.02,
        columns=tickers,
    )

    # corr/cov between two columns use only the aligned, overlapping values.
    # (.loc[:, col] selects one column as a Series unambiguously.)
    print(returns.loc[:, "MSFT"].corr(returns.loc[:, "IBM"]))
    print(returns.loc[:, "MSFT"].cov(returns.loc[:, "IBM"]))

    # On a DataFrame, corr/cov return the full matrix.
    print(returns.corr())
    print(returns.cov())

    # corrwith correlates each column against another Series (here, one column).
    print(returns.corrwith(returns.loc[:, "IBM"]))
    # Passing a DataFrame correlates matching column names pair-wise.
    volume = pd.DataFrame(rng.standard_normal((100, 4)), columns=tickers)
    print(returns.corrwith(volume))


def explain_unique_counts_membership() -> None:
    """
    Problem: inspect the distinct contents of a column.
    Why: `unique` lists distinct values in first-seen order; `value_counts`
    tallies frequencies (descending) — note pandas 3.0 removed the top-level
    `pd.value_counts`, so use the Series/DataFrame method; `isin` filters to a
    set of values; and
    `Index.get_indexer` maps possibly-duplicated values into the positions of a
    distinct-value array (useful for joins/alignment).
    """
    print("== Unique values, value counts, and membership ==")

    obj = pd.Series(["c", "a", "d", "a", "a", "b", "b", "c", "c"])
    print(obj.unique())          # distinct values, order of first appearance
    print(obj.value_counts())    # frequencies, sorted descending
    # pandas 3.0: the top-level pd.value_counts was removed; wrap a sequence in
    # a Series and call the method instead.
    print(pd.Series(obj.to_numpy()).value_counts(sort=False))

    # isin is a vectorized membership test, handy for filtering.
    mask = obj.isin(["b", "c"])
    print(mask)
    print(obj[mask])

    # Index.get_indexer maps each value into an array of distinct values.
    to_match = pd.Series(["c", "a", "b", "b", "c", "a"])
    unique_vals = pd.Series(["c", "b", "a"])
    print(pd.Index(unique_vals).get_indexer(to_match))

    # Histogram across several columns: apply value_counts to each column.
    data = pd.DataFrame(
        {"Qu1": [1, 3, 4, 3, 4], "Qu2": [2, 3, 1, 2, 3], "Qu3": [1, 5, 2, 4, 4]}
    )
    print(data["Qu1"].value_counts().sort_index())
    # pandas 3.0: pd.value_counts is gone, so apply Series.value_counts per column.
    print(data.apply(lambda col: col.value_counts()).fillna(0))
    # DataFrame.value_counts counts whole rows (as tuples) instead.
    data2 = pd.DataFrame({"a": [1, 1, 1, 2, 2], "b": [0, 0, 1, 0, 0]})
    print(data2.value_counts())


def main() -> None:
    explain_summarizing()
    explain_correlation_and_covariance()
    explain_unique_counts_membership()


main()
