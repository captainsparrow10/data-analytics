"""
Handling Missing Data (Section 7.1)

Missing data occurs commonly in many data analysis applications. One of the goals
of pandas is to make working with missing data as painless as possible: for
example, all of the descriptive statistics on pandas objects exclude missing data
by default. For data with the float64 dtype, pandas uses the floating-point value
NaN (Not a Number) as a *sentinel value*: when present, it indicates a missing
(or null) value. The built-in Python `None` is also treated as NA. This file
covers detecting missing data (`isna`/`notna`), filtering it out (`dropna` with
`how`, `axis`, and `thresh`), and filling it in (`fillna` with a scalar, a dict,
a forward-fill `method`/`limit`, or an imputed statistic like the mean).

NA HANDLING OBJECT METHODS
METHOD    DESCRIPTION
dropna    Filter axis labels based on whether values have missing data, with
          varying thresholds for how much missing data to tolerate
fillna    Fill in missing data with a value or an interpolation method ("ffill"/"bfill")
isna      Return Boolean values indicating which values are missing / NA
notna     Negation of isna; True for non-NA values and False for NA values

Run:
    poetry run python cap_07_cleaning/1-handling-missing-data.py
"""

import numpy as np
import pandas as pd


def explain_detecting_na() -> None:
    """
    Problem: spot the missing values inside a Series.
    Why: NaN is the float64 sentinel for "not available" (NA), and the Python
    `None` value is treated as NA too. `isna` returns a Boolean Series with True
    where values are null, which is the basis for every other missing-data tool.
    """
    print("== Detecting NA in a Series ==")

    float_data = pd.Series([1.2, -3.5, np.nan, 0])
    print(float_data)
    # isna gives a Boolean Series with True where values are null.
    print(float_data.isna())

    # The built-in Python None is also treated as NA.
    string_data = pd.Series(["aardvark", np.nan, None, "avocado"])
    print(string_data)
    print(string_data.isna())

    # Building a float Series with None coerces it to NaN.
    float_data = pd.Series([1, 2, None], dtype="float64")
    print(float_data)
    print(float_data.isna())


def explain_dropna_series() -> None:
    """
    Problem: drop the missing entries from a Series.
    Why: `dropna` returns only the non-null data and index values — equivalent to
    Boolean indexing with `notna`, but more direct.
    """
    print("== Filtering out missing data from a Series ==")

    data = pd.Series([1, np.nan, 3.5, np.nan, 7])
    print(data.dropna())            # keep only the non-null values
    # This is the same thing as doing Boolean indexing with notna.
    print(data[data.notna()])


def explain_dropna_dataframe() -> None:
    """
    Problem: drop rows or columns of a DataFrame that contain missing data.
    Why: with 2D data you have choices. By default `dropna` drops any row
    containing a missing value; `how="all"` drops only rows that are entirely NA;
    `axis="columns"` switches the operation to columns. These return new objects
    and do not modify the original.
    """
    print("== Filtering out missing data from a DataFrame ==")

    data = pd.DataFrame(
        [[1.0, 6.5, 3.0], [1.0, np.nan, np.nan], [np.nan, np.nan, np.nan], [np.nan, 6.5, 3.0]]
    )
    print(data)
    print(data.dropna())                 # default: drop any row with an NA
    print(data.dropna(how="all"))        # drop only rows that are ALL NA

    # Add an all-NA column, then drop all-NA columns with axis="columns".
    data[4] = np.nan
    print(data)
    print(data.dropna(axis="columns", how="all"))


def explain_dropna_thresh() -> None:
    """
    Problem: keep rows that have at least a minimum number of valid observations.
    Why: `thresh=N` keeps only rows containing at least N non-NA values, a softer
    rule than "drop any row with a missing value".
    """
    print("== dropna with a threshold (thresh) ==")

    # Seeded generator replaces the book's legacy np.random.standard_normal global.
    rng = np.random.default_rng(seed=12345)
    df = pd.DataFrame(rng.standard_normal((7, 3)))
    # Punch holes into the data: NA in column 1 for first 4 rows, column 2 for first 2.
    df.iloc[:4, 1] = np.nan
    df.iloc[:2, 2] = np.nan
    print(df)
    print(df.dropna())              # drop any row containing an NA
    print(df.dropna(thresh=2))      # keep rows with at least 2 non-NA values


def explain_fillna() -> None:
    """
    Problem: fill the "holes" in the data instead of discarding them.
    Why: `fillna` is the workhorse. A scalar replaces every NA; a dict uses a
    different fill value per column; `ffill()` propagates the last valid
    observation forward (pandas 3.0 replaced `fillna(method="ffill")` with this
    dedicated method, keeping the optional `limit` on consecutive fills); and you
    can impute with a statistic such as the mean.
    """
    print("== Filling in missing data with fillna ==")

    rng = np.random.default_rng(seed=12345)
    df = pd.DataFrame(rng.standard_normal((7, 3)))
    df.iloc[:4, 1] = np.nan
    df.iloc[:2, 2] = np.nan

    print(df.fillna(0))                  # replace every NA with a constant
    print(df.fillna({1: 0.5, 2: 0}))     # a different fill value per column

    # The same interpolation methods used for reindexing work with fillna.
    df2 = pd.DataFrame(rng.standard_normal((6, 3)))
    df2.iloc[2:, 1] = np.nan
    df2.iloc[4:, 2] = np.nan
    print(df2)
    # pandas 3.0: fillna(method="ffill") was removed -> use the dedicated ffill().
    print(df2.ffill())            # forward-fill down each column
    print(df2.ffill(limit=2))     # at most 2 consecutive fills

    # Simple imputation: fill NA with the mean of the present values.
    data = pd.Series([1.0, np.nan, 3.5, np.nan, 7])
    print(data.fillna(data.mean()))


def main() -> None:
    explain_detecting_na()
    explain_dropna_series()
    explain_dropna_dataframe()
    explain_dropna_thresh()
    explain_fillna()


main()
