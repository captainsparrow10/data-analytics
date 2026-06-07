"""
Apply: General Split-Apply-Combine (Section 10.3)

`apply` is the most general-purpose GroupBy method: it splits the object into
pieces, invokes the passed function on each piece, and then attempts to
concatenate the pieces back together. The function may return a pandas object or
a scalar; everything else is up to you, which makes `apply` the workhorse for
custom group analyses.

This file covers: selecting the top rows per group with `apply`, passing extra
arguments to the applied function, suppressing the group keys
(`group_keys=False`), quantile and bucket analysis with `cut`/`qcut`, and the
worked examples — filling missing values with group-specific values, random
sampling/permutation, group weighted average and correlation, and group-wise
linear regression with `statsmodels`.

WORKED EXAMPLES IN THIS FILE
TOPIC                       TECHNIQUE
top-N per group             apply a sort+slice function to each group
quantile / bucket analysis  cut / qcut -> groupby the Categorical -> apply/agg
fill missing per group      apply a function that calls fillna on each chunk
random sampling             Series.sample within / across groups
weighted average            np.average(group["data"], weights=...) via apply
group correlation           corrwith / corr across yearly groups
group-wise OLS              statsmodels sm.OLS fit per group, returning params

Run:
    poetry run python cap_10_groupby/3-apply-split-apply-combine.py
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm


def _tips() -> pd.DataFrame:
    """Small tips-like DataFrame built in code (the book loads examples/tips.csv)."""
    rng = np.random.default_rng(seed=10)
    n = 200
    days = rng.choice(["Fri", "Sat", "Sun", "Thur"], size=n, p=[0.1, 0.35, 0.3, 0.25])
    times = np.where(np.isin(days, ["Fri", "Thur"]), rng.choice(["Lunch", "Dinner"], size=n), "Dinner")
    total_bill = np.round(rng.gamma(shape=6.0, scale=3.3, size=n) + 3.0, 2)
    smoker = rng.choice(["No", "Yes"], size=n, p=[0.62, 0.38])
    size = rng.integers(1, 7, size=n)
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
    tips["tip_pct"] = tips["tip"] / tips["total_bill"]
    return tips


def explain_apply_basics() -> None:
    """
    Problem: select the rows with the largest values of a column, within groups.
    Why: write a plain function that operates on a DataFrame (sort + slice), then
    hand it to `apply`. pandas calls it on each group and glues the results with
    `pd.concat`, labeling the pieces with the group names — so the result has a
    hierarchical index whose inner level is the original row index. Extra
    arguments to the function are passed after it in the `apply` call.
    """
    print("== apply basics: top-N per group, passing extra arguments ==")

    tips = _tips()

    def top(df: pd.DataFrame, n: int = 5, column: str = "tip_pct") -> pd.DataFrame:
        # __getitem__ slicing is typed broadly; narrow back to a DataFrame.
        result = df.sort_values(column, ascending=False)[:n]
        assert isinstance(result, pd.DataFrame)
        return result

    # The function applied to the whole frame (no grouping yet).
    print(top(tips, n=6))

    # Grouped by smoker: top function runs on each group, results concatenated.
    # (include_groups=False keeps the grouping column out of the applied frame,
    # which pandas 3.0 expects; we re-select the column inside top regardless.)
    print(tips.groupby("smoker")[tips.columns].apply(top, include_groups=False))

    # Passing extra keyword/positional args after the function.
    print(
        tips.groupby(["smoker", "day"])[tips.columns].apply(
            top, n=1, column="total_bill", include_groups=False
        )
    )


def explain_describe_via_apply() -> None:
    """
    Problem: see that GroupBy methods like describe are just apply shortcuts.
    Why: invoking `describe` on a GroupBy is equivalent to applying a function
    that calls `group.describe()` on each chunk — useful for building intuition.
    """
    print("== describe on a GroupBy is an apply shortcut ==")

    tips = _tips()
    result = tips.groupby("smoker")["tip_pct"].describe()
    print(result)
    print(result.unstack("smoker"))  # reshape stats into columns by smoker


def explain_suppressing_group_keys() -> None:
    """
    Problem: drop the group keys that apply prepends to the result index.
    Why: by default apply forms a hierarchical index from the group keys plus the
    index of each piece. Passing `group_keys=False` to groupby suppresses the
    group-key level, leaving just the original row index.
    """
    print("== Suppressing the group keys (group_keys=False) ==")

    tips = _tips()

    def top(df: pd.DataFrame, n: int = 5, column: str = "tip_pct") -> pd.DataFrame:
        # __getitem__ slicing is typed broadly; narrow back to a DataFrame.
        result = df.sort_values(column, ascending=False)[:n]
        assert isinstance(result, pd.DataFrame)
        return result

    print(
        tips.groupby("smoker", group_keys=False)[tips.columns].apply(
            top, include_groups=False
        )
    )


def explain_quantile_and_bucket_analysis() -> None:
    """
    Problem: compute group statistics over buckets/quantiles of a variable.
    Why: `cut` slices data into equal-length bins and `qcut` into equal-size
    quantile bins. The returned Categorical can be passed straight to `groupby`,
    so combining them with apply/agg gives bucket/quantile analysis. (In pandas
    3.0 grouping by a Categorical keeps only observed combos with observed=True;
    we set it explicitly to avoid the future-default warning.)
    """
    print("== Quantile and bucket analysis (cut / qcut) ==")

    rng = np.random.default_rng(seed=12345)
    frame = pd.DataFrame(
        {"data1": rng.standard_normal(1000), "data2": rng.standard_normal(1000)}
    )
    print(frame.head())

    # Equal-length buckets of data1. (pd.cut is typed to return a broad union;
    # passing a Series back gives a Series, so narrow it for the .head() call.)
    quartiles = pd.cut(frame["data1"], 4)
    assert isinstance(quartiles, pd.Series)
    print(quartiles.head(10))

    def get_stats(group: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "min": group.min(),
                "max": group.max(),
                "count": group.count(),
                "mean": group.mean(),
            }
        )

    grouped = frame.groupby(quartiles, observed=True)
    print(grouped.apply(get_stats))
    # The same result, more simply, with agg and a list of method names.
    print(grouped.agg(["min", "max", "count", "mean"]))

    # Equal-size buckets via sample quantiles; labels=False yields bin indices.
    quartiles_samp = pd.qcut(frame["data1"], 4, labels=False)
    assert isinstance(quartiles_samp, pd.Series)  # narrow the broad qcut union
    print(quartiles_samp.head())
    grouped = frame.groupby(quartiles_samp, observed=True)
    print(grouped.apply(get_stats))


def explain_filling_missing_with_group_values() -> None:
    """
    Problem: fill NA values with a value derived from each group.
    Why: `fillna` fills with a fixed or computed value. To make the fill value
    vary by group, group the data and `apply` a function that calls `fillna` on
    each chunk — with the group mean, or with predefined per-group values keyed
    off the chunk's `name` attribute.
    """
    print("== Filling missing values with group-specific values ==")

    states = ["Ohio", "New York", "Vermont", "Florida", "Oregon", "Nevada", "California", "Idaho"]
    group_key = ["East", "East", "East", "East", "West", "West", "West", "West"]
    rng = np.random.default_rng(seed=12345)
    data = pd.Series(rng.standard_normal(8), index=states)
    # Set some values missing (Copy-on-Write: assign via .loc).
    data.loc[["Vermont", "Nevada", "Idaho"]] = np.nan
    print(data)
    print(data.groupby(group_key).mean())

    # Fill each region's NAs with that region's mean.
    def fill_mean(group: pd.Series) -> pd.Series:
        return group.fillna(group.mean())

    print(data.groupby(group_key, group_keys=False).apply(fill_mean))

    # Predefined per-group fill values, read from the chunk's name attribute.
    fill_values = {"East": 0.5, "West": -1.0}

    def fill_func(group: pd.Series) -> pd.Series:
        # The group's name is typed as Hashable; here it is the region string.
        region = group.name
        assert isinstance(region, str)
        return group.fillna(fill_values[region])

    print(data.groupby(group_key, group_keys=False).apply(fill_func))


def explain_random_sampling_and_permutation() -> None:
    """
    Problem: draw random samples, optionally within each group.
    Why: `Series.sample` performs the "draws" (with or without replacement). To
    sample within groups, group first and apply the draw to each chunk. Grouping
    by a key derived from the data (here the card suit) shows sampling per group.
    """
    print("== Random sampling and permutation ==")

    # Build a 52-card deck: values are blackjack-style (face cards = 10, ace = 1).
    suits = ["H", "S", "C", "D"]  # Hearts, Spades, Clubs, Diamonds
    card_val = (list(range(1, 11)) + [10] * 3) * 4
    base_names = ["A"] + list(range(2, 11)) + ["J", "K", "Q"]
    cards: list[str] = []
    for suit in suits:
        cards.extend(str(num) + suit for num in base_names)
    deck = pd.Series(card_val, index=cards)
    print(deck.head(13))

    # Draw a hand of five cards (random_state keeps the demo reproducible).
    def draw(deck: pd.Series, n: int = 5) -> pd.Series:
        return deck.sample(n, random_state=12345)

    print(draw(deck))

    # Two random cards from each suit: group by the suit (last char of the name).
    def get_suit(card: str) -> str:
        return card[-1]  # last letter is the suit

    print(deck.groupby(get_suit).apply(draw, n=2))
    # group_keys=False drops the outer suit index, leaving just the cards.
    print(deck.groupby(get_suit, group_keys=False).apply(draw, n=2))


def explain_group_weighted_average_and_correlation() -> None:
    """
    Problem: compute a weighted average per group, and correlations per group.
    Why: under split-apply-combine, operations between columns of a group (e.g.
    `np.average(data, weights=...)`) are easy via apply. With a financial frame,
    grouping daily returns by year and applying `corrwith`/`corr` yields annual
    correlation tables.
    """
    print("== Group weighted average and correlation ==")

    rng = np.random.default_rng(seed=12345)
    df = pd.DataFrame(
        {
            "category": ["a", "a", "a", "a", "b", "b", "b", "b"],
            "data": rng.standard_normal(8),
            "weights": rng.uniform(size=8),
        }
    )
    print(df)

    def get_wavg(group: pd.DataFrame) -> float:
        return np.average(group["data"], weights=group["weights"])

    print(df.groupby("category").apply(get_wavg, include_groups=False))

    # A small financial frame of daily prices for a few tickers and the index.
    dates = pd.bdate_range("2003-01-01", periods=750)
    px = pd.DataFrame(
        {
            "AAPL": 100 * np.exp(np.cumsum(rng.standard_normal(750) * 0.02)),
            "MSFT": 30 * np.exp(np.cumsum(rng.standard_normal(750) * 0.02)),
            "XOM": 70 * np.exp(np.cumsum(rng.standard_normal(750) * 0.02)),
            "SPX": 1000 * np.exp(np.cumsum(rng.standard_normal(750) * 0.012)),
        },
        index=dates,
    )
    print(px.tail(4))

    # Daily percent-change returns; fill_method=None is required in pandas 3.0.
    rets = px.pct_change(fill_method=None).dropna()

    # Yearly correlation of each column with SPX.
    def spx_corr(group: pd.DataFrame) -> pd.Series:
        spx = group["SPX"]
        assert isinstance(spx, pd.Series)  # single-column indexing is a broad union
        return group.corrwith(spx)

    def get_year(x: pd.Timestamp) -> int:
        return x.year

    by_year = rets.groupby(get_year)
    print(by_year.apply(spx_corr))

    # Annual correlation between two specific columns. (Single-column indexing is
    # typed as a broad union; narrow both columns to Series for Series.corr.)
    def corr_aapl_msft(group: pd.DataFrame) -> float:
        aapl, msft = group["AAPL"], group["MSFT"]
        assert isinstance(aapl, pd.Series) and isinstance(msft, pd.Series)
        return aapl.corr(msft)

    print(by_year.apply(corr_aapl_msft))


def explain_group_wise_linear_regression() -> None:
    """
    Problem: run an ordinary least squares regression within each group.
    Why: as long as the applied function returns a pandas object or scalar, apply
    can drive arbitrarily complex per-group analysis. Here `regress` fits an OLS
    model with statsmodels on each yearly chunk and returns its parameters.
    """
    print("== Group-wise linear regression (statsmodels OLS) ==")

    rng = np.random.default_rng(seed=12345)
    dates = pd.bdate_range("2003-01-01", periods=750)
    px = pd.DataFrame(
        {
            "AAPL": 100 * np.exp(np.cumsum(rng.standard_normal(750) * 0.02)),
            "SPX": 1000 * np.exp(np.cumsum(rng.standard_normal(750) * 0.012)),
        },
        index=dates,
    )
    rets = px.pct_change(fill_method=None).dropna()

    def regress(data: pd.DataFrame, yvar: str, xvars: list[str]) -> pd.Series:
        Y = data[yvar]
        X = data[xvars].copy()
        X["intercept"] = 1.0  # add the intercept column (Copy-on-Write safe copy)
        result = sm.OLS(Y, X).fit()
        return result.params

    def get_year(x: pd.Timestamp) -> int:
        return x.year

    by_year = rets.groupby(get_year)
    print(by_year.apply(regress, yvar="AAPL", xvars=["SPX"]))


def main() -> None:
    explain_apply_basics()
    explain_describe_via_apply()
    explain_suppressing_group_keys()
    explain_quantile_and_bucket_analysis()
    explain_filling_missing_with_group_values()
    explain_random_sampling_and_permutation()
    explain_group_weighted_average_and_correlation()
    explain_group_wise_linear_regression()


main()
