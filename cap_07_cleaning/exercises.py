"""
Data Cleaning & Preparation: Practice Exercises

This file collects hands-on practice for the chapter 7 toolkit: detecting and
handling missing data, dropping and filling values, removing duplicates,
replacing and renaming, mapping columns through a dictionary, discretizing with
`cut`/`qcut`, detecting and capping outliers, cleaning text with the `.str`
accessor, and encoding categories with `Categorical`/`get_dummies`. Each exercise
states the problem and the expected result in its docstring, then solves it on a
small in-code DataFrame or Series, printing every intermediate step so you can
follow the reasoning.

Run:
    poetry run python cap_07_cleaning/exercises.py
"""

import numpy as np
import pandas as pd


def exercise_01() -> None:
    """
    Exercise 1: Detect missing values

    Problem: Given a Series with some missing entries, produce a Boolean mask of
    which positions are missing and count how many are present (non-missing).

    Expected result: a mask [False, True, False, True, False] and "Present: 3".
    """
    s = pd.Series([10.0, np.nan, 30.0, np.nan, 50.0])
    mask = s.isna()  # True where the value is NA
    present = int(s.notna().sum())  # notna() flips the mask; sum() counts the Trues
    print(mask.tolist())
    print(f"Present: {present}")


def exercise_02() -> None:
    """
    Exercise 2: Drop rows that contain any missing value

    Problem: Drop every row of a DataFrame that has at least one NA, then drop
    only the rows that are entirely NA.

    Expected result: dropna() keeps only the fully-populated row; how="all" keeps
    every row except the all-NA one.
    """
    df = pd.DataFrame(
        {
            "a": [1.0, np.nan, np.nan, 4.0],
            "b": [np.nan, 2.0, np.nan, 8.0],
        }
    )
    print(df)
    print("-- drop rows with ANY NA --")
    print(df.dropna())  # default how="any": a row survives only if fully populated
    print("-- drop rows that are ALL NA --")
    print(df.dropna(how="all"))  # only the row where every column is NA is removed


def exercise_03() -> None:
    """
    Exercise 3: Drop columns with too many missing values via thresh

    Problem: Keep only the columns that have at least 3 non-NA values; drop the
    rest. Use the `thresh` argument along axis="columns".

    Expected result: the sparse column "c" (only 1 real value) is dropped.
    """
    df = pd.DataFrame(
        {
            "a": [1.0, 2.0, 3.0, 4.0],  # 4 non-NA
            "b": [1.0, np.nan, 3.0, 4.0],  # 3 non-NA
            "c": [np.nan, np.nan, 3.0, np.nan],  # 1 non-NA -> dropped
        }
    )
    print(df)
    # thresh=3 means "require at least 3 non-NA values to KEEP the column".
    cleaned = df.dropna(axis="columns", thresh=3)
    print("-- columns with >= 3 non-NA --")
    print(cleaned)


def exercise_04() -> None:
    """
    Exercise 4: Fill missing values with a scalar and with a per-column dict

    Problem: First replace every NA with 0, then instead fill column "a" with 100
    and column "b" with 200 using a dictionary.

    Expected result: scalar fill puts 0 everywhere; the dict fill uses a different
    constant per column.
    """
    df = pd.DataFrame(
        {
            "a": [1.0, np.nan, 3.0],
            "b": [np.nan, 5.0, np.nan],
        }
    )
    print(df)
    print("-- fillna(0) --")
    print(df.fillna(0))  # one scalar for the whole frame
    print("-- fillna per-column dict --")
    print(df.fillna({"a": 100, "b": 200}))  # the dict keys map column -> fill value


def exercise_05() -> None:
    """
    Exercise 5: Forward-fill and mean-fill missing values

    Problem: Carry the last valid observation forward to fill gaps in a Series;
    separately, fill the gaps with the Series mean instead.

    Expected result: ffill propagates the previous value; mean-fill uses the
    average of the non-missing values.
    """
    s = pd.Series([1.0, np.nan, np.nan, 4.0, np.nan, 6.0])
    print("-- forward fill --")
    print(s.ffill().tolist())  # each NA takes the last seen non-NA value
    print("-- mean fill --")
    print(s.fillna(s.mean()).tolist())  # mean() ignores NA by default


def exercise_06() -> None:
    """
    Exercise 6: Remove duplicate rows with keep and subset

    Problem: From a DataFrame of orders, (a) drop full-row duplicates keeping the
    first, (b) drop duplicates of column "sku" keeping the last occurrence.

    Expected result: (a) removes the exact repeated row; (b) leaves one row per
    sku, namely the last one seen.
    """
    df = pd.DataFrame(
        {
            "sku": ["A1", "A1", "B2", "B2", "A1"],
            "qty": [1, 1, 5, 7, 9],
        }
    )
    print(df)
    print("-- drop full-row duplicates (keep first) --")
    print(df.drop_duplicates())  # the second A1/1 row is an exact duplicate
    print("-- one row per sku, keep last --")
    print(df.drop_duplicates(subset="sku", keep="last"))


def exercise_07() -> None:
    """
    Exercise 7: Replace sentinel values with NA

    Problem: A column uses -999 and -1 as "missing" sentinels. Replace both with
    a proper NaN so downstream NA handling works.

    Expected result: the two sentinel readings become NaN; real values are kept.
    """
    s = pd.Series([23.5, -999.0, 19.0, -1.0, 21.0])
    print(s.tolist())
    cleaned = s.replace([-999.0, -1.0], np.nan)  # a list of values -> one replacement
    print(cleaned.tolist())


def exercise_08() -> None:
    """
    Exercise 8: Rename axis labels

    Problem: Uppercase the row index labels and rename specific columns
    ("temp" -> "temperature", "hum" -> "humidity") using rename.

    Expected result: index labels become uppercase; only the two named columns
    are renamed.
    """
    df = pd.DataFrame(
        {"temp": [20, 22], "hum": [55, 60]},
        index=["day1", "day2"],
    )
    print(df)
    renamed = df.rename(
        index=str.upper,  # a function applied to every index label
        columns={"temp": "temperature", "hum": "humidity"},  # explicit mapping
    )
    print(renamed)


def exercise_09() -> None:
    """
    Exercise 9: Map a column through a dictionary

    Problem: Translate two-letter country codes in a column to full names using a
    lookup dict. Use map with `lambda x: d[x]` so an unknown code raises a
    KeyError instead of silently becoming NaN.

    Expected result: each code is expanded to its full country name.
    """
    df = pd.DataFrame({"code": ["AR", "BR", "CL", "AR"]})
    names = {"AR": "Argentina", "BR": "Brazil", "CL": "Chile"}
    print(df)
    # Using `lambda x: names[x]` (not map(names)) makes a missing key an explicit
    # error rather than a silent NaN, which catches dirty data early.
    df["country"] = df["code"].map(lambda x: names[x])
    print(df)


def exercise_10() -> None:
    """
    Exercise 10: Discretize a continuous column with cut

    Problem: Bin a column of ages into the ranges (0, 18], (18, 35], (35, 65],
    (65, 120] labeled minor/young/adult/senior, then count how many fall in each.

    Expected result: each age is assigned its band, and value_counts reports the
    per-band totals.
    """
    ages = pd.Series([5, 17, 22, 34, 40, 64, 70, 90])
    bins = [0, 18, 35, 65, 120]
    labels = ["minor", "young", "adult", "senior"]
    bands = pd.cut(ages, bins=bins, labels=labels)  # fixed edges -> ordered categories
    assert isinstance(bands, pd.Series)  # narrow: cut overloads can return a tuple
    print(bands.tolist())
    # value_counts on a categorical respects category order when sort=False.
    print(bands.value_counts(sort=False))


def exercise_11() -> None:
    """
    Exercise 11: Discretize into equal-size buckets with qcut

    Problem: Split 12 values into 4 quartile buckets (Q1..Q4) so each bucket holds
    roughly the same number of observations, then count per bucket.

    Expected result: four quartile labels with 3 values each (12 / 4).
    """
    rng = np.random.default_rng(seed=7)
    data = pd.Series(rng.integers(0, 100, size=12))
    print(data.tolist())
    # qcut splits by sample quantiles, so bucket SIZES are balanced (unlike cut,
    # which splits by value RANGE).
    quartiles = pd.qcut(data, q=4, labels=["Q1", "Q2", "Q3", "Q4"])
    assert isinstance(quartiles, pd.Series)  # narrow: qcut overloads can return a tuple
    print(quartiles.tolist())
    print(quartiles.value_counts(sort=False))


def exercise_12() -> None:
    """
    Exercise 12: Detect and cap outliers

    Problem: In a numeric Series, find values whose absolute magnitude exceeds 3,
    report them, then cap (clip) every value to the range [-3, 3].

    Expected result: the extreme readings are listed, and after clipping no value
    lies outside [-3, 3].
    """
    rng = np.random.default_rng(seed=42)
    s = pd.Series(rng.normal(0, 1, size=200))
    # Manually seed a couple of clear outliers so the exercise is deterministic.
    s.loc[0] = 6.5  # Copy-on-Write: assign through .loc
    s.loc[1] = -4.2
    outliers = s[s.abs() > 3]  # Boolean mask selects the extreme values
    print(f"Outliers found: {outliers.round(2).tolist()}")
    capped = s.clip(lower=-3, upper=3)  # clip squeezes values into the range
    print(f"Max after cap: {capped.max():.2f}, Min after cap: {capped.min():.2f}")


def exercise_13() -> None:
    """
    Exercise 13: Clean strings with the .str accessor

    Problem: A column of user-entered emails has stray whitespace and mixed case.
    Strip and lowercase them, flag which contain "@example.com", and extract the
    username (the part before the @).

    Expected result: normalized emails, a Boolean membership flag, and the
    extracted usernames.
    """
    s = pd.Series(["  Alice@Example.com ", "BOB@other.com", " carol@example.COM"])
    cleaned = s.str.strip().str.lower()  # chain vectorized string ops
    print(cleaned.tolist())
    is_example = cleaned.str.contains("@example.com")  # substring membership test
    print(is_example.tolist())
    # extract returns a DataFrame of capture groups; take column 0 for the username.
    usernames = cleaned.str.extract(r"^([^@]+)@")[0]
    print(usernames.tolist())


def exercise_14() -> None:
    """
    Exercise 14: Convert to Categorical and build dummy variables

    Problem: Convert a "size" column to an ordered Categorical (S < M < L), then
    one-hot encode it into integer indicator columns with get_dummies.

    Expected result: the dtype becomes ordered category, and get_dummies yields
    integer 0/1 columns size_S, size_M, size_L.
    """
    df = pd.DataFrame({"size": ["M", "S", "L", "M", "S"]})
    size_type = pd.CategoricalDtype(categories=["S", "M", "L"], ordered=True)
    df["size"] = df["size"].astype(size_type)  # ordered category enables comparisons
    print(df["size"].dtype)
    print((df["size"] >= "M").tolist())  # ordering makes >= meaningful
    # dtype=int gives 0/1 ints instead of pandas 3.0's default booleans.
    dummies = pd.get_dummies(df["size"], prefix="size", dtype=int)
    print(dummies)


def main() -> None:
    print("=== Exercise 1: Detect missing values ===")
    exercise_01()

    print("\n=== Exercise 2: Drop rows with missing values ===")
    exercise_02()

    print("\n=== Exercise 3: Drop columns via thresh ===")
    exercise_03()

    print("\n=== Exercise 4: Fill with scalar and dict ===")
    exercise_04()

    print("\n=== Exercise 5: Forward-fill and mean-fill ===")
    exercise_05()

    print("\n=== Exercise 6: Remove duplicates (keep/subset) ===")
    exercise_06()

    print("\n=== Exercise 7: Replace sentinels with NA ===")
    exercise_07()

    print("\n=== Exercise 8: Rename axis labels ===")
    exercise_08()

    print("\n=== Exercise 9: Map a column via a dict ===")
    exercise_09()

    print("\n=== Exercise 10: Discretize with cut ===")
    exercise_10()

    print("\n=== Exercise 11: Discretize with qcut ===")
    exercise_11()

    print("\n=== Exercise 12: Detect and cap outliers ===")
    exercise_12()

    print("\n=== Exercise 13: Clean strings with .str ===")
    exercise_13()

    print("\n=== Exercise 14: Categorical and get_dummies ===")
    exercise_14()


main()
