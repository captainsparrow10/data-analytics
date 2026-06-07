"""
Moving Window Functions (Section 11.7)

An important class of array transformations for time series are statistics
evaluated over a sliding WINDOW or with exponentially decaying weights — useful
for smoothing noisy or gappy data. pandas calls these *moving window functions*.
Like other statistical functions, they automatically exclude missing data. The
`rolling` operator behaves like `resample`/`groupby`: it groups over a window
(a number of periods, or a time offset like "20D") and you then aggregate.

This file covers `rolling` (fixed window, `min_periods`, and a time-offset
window), `expanding` (an ever-growing window), exponentially weighted statistics
(`ewm(span=)`), binary moving window functions (rolling `corr` between two
series), and user-defined window functions (`rolling().apply`).

The book loads `examples/stock_px.csv` / `volume.csv`; to stay self-contained and
offline, this file synthesizes a deterministic daily price DataFrame (AAPL, MSFT,
XOM, SPX) via a cumulative-sum random walk seeded with `np.random.default_rng`.

KEY OPERATIONS IN THIS FILE
METHOD/CONCEPT       DESCRIPTION
rolling(window)      Sliding fixed-length window; aggregate with mean/std/...
rolling(min_periods=) Allow fewer than `window` points (fewer NaN at the start)
rolling("20D")       A time-offset window for irregular series
expanding()          A window that grows from the start to the whole series
ewm(span=)           Exponentially weighted moving statistics (decay factor)
rolling().corr(other) Binary window function over two aligned series
rolling().apply(f)   Apply a user-defined reduction over each window

Run:
    poetry run python cap_11_timeseries/7-moving-window-functions.py
"""

import numpy as np
import pandas as pd
from scipy.stats import percentileofscore


def _make_close_px() -> pd.DataFrame:
    """
    Build a deterministic daily closing-price DataFrame standing in for the book's
    examples/stock_px.csv (columns AAPL, MSFT, XOM, SPX). Each column is a
    positive cumulative-sum random walk over business days, so the moving-window
    statistics below behave like the real data without any network access.
    """
    rng = np.random.default_rng(seed=12345)
    dates = pd.date_range("2003-01-01", "2011-10-14", freq="B")  # business days
    n = len(dates)
    columns = ["AAPL", "MSFT", "XOM", "SPX"]
    starts = {"AAPL": 7.0, "MSFT": 21.0, "XOM": 29.0, "SPX": 900.0}
    scales = {"AAPL": 0.6, "MSFT": 0.25, "XOM": 0.4, "SPX": 6.0}
    data = {}
    for col in columns:
        steps = rng.standard_normal(n) * scales[col]
        walk = starts[col] + np.cumsum(steps)
        # Keep prices strictly positive (a real price series never goes negative).
        data[col] = np.abs(walk) + 1.0
    return pd.DataFrame(data, index=dates)


def explain_rolling() -> None:
    """
    Problem: compute a moving average and a moving standard deviation.
    Why: `rolling(window)` creates an object that groups over a sliding window of
    `window` periods; `.mean()` then gives the moving average. By default a window
    needs every value present, so the first `window-1` results are NaN;
    `min_periods=` relaxes that so partial windows still produce a value.
    """
    print("== rolling (window, min_periods) ==")

    close_px_all = _make_close_px()
    close_px = close_px_all[["AAPL", "MSFT", "XOM"]]
    # Resample to business day frequency and forward-fill (mirrors the book).
    close_px = close_px.resample("B").ffill()

    # 250-day moving average of Apple's price (tail keeps the output compact).
    print(close_px["AAPL"].rolling(250).mean().tail())

    # Rolling std of daily returns, allowing windows with as few as 10 points.
    std250 = close_px["AAPL"].pct_change().rolling(250, min_periods=10).std()
    print(std250[5:12])


def explain_expanding() -> None:
    """
    Problem: compute a statistic over an ever-growing window.
    Why: `expanding()` starts the window at the same point as `rolling` but keeps
    GROWING it until it spans the whole series — so each value is the statistic of
    all data up to that point (an expanding-window mean here).
    """
    print("== expanding (growing window) ==")

    close_px = _make_close_px()
    std250 = close_px["AAPL"].pct_change().rolling(250, min_periods=10).std()
    expanding_mean = std250.expanding().mean()
    print(expanding_mean.tail())


def explain_time_offset_window() -> None:
    """
    Problem: define a window by a time span rather than a fixed count of rows.
    Why: `rolling` also accepts a fixed-size TIME OFFSET (e.g. "20D"), which is
    handy for irregular series — each window covers the last 20 calendar days
    regardless of how many observations that is. The strings match those of
    `resample`.
    """
    print("== rolling with a time-offset window ==")

    close_px = _make_close_px()
    # .mean() on a rolling DataFrame is typed broadly; narrow to a DataFrame so
    # the .tail() call resolves cleanly.
    rolled = close_px.rolling("20D").mean()
    assert isinstance(rolled, pd.DataFrame)
    print(rolled.tail())


def explain_ewm() -> None:
    """
    Problem: weight recent observations more heavily than older ones.
    Why: instead of an equally weighted fixed window, exponentially weighted
    statistics apply a decay factor. `ewm(span=)` (a common parameterization,
    comparable to a simple window of that span) "adapts" faster to changes than
    the equal-weighted version. Here a 30-day simple average is compared with an
    EW average of the same span.
    """
    print("== Exponentially weighted (ewm) ==")

    close_px = _make_close_px()
    # String-slicing a Series is typed broadly (could be an ndarray); narrow to
    # Series so the rolling / ewm methods resolve.
    aapl_px = close_px["AAPL"]["2006":"2007"]
    assert isinstance(aapl_px, pd.Series)
    # Both .mean() results are typed broadly; narrow to Series for .tail().
    ma30 = aapl_px.rolling(30, min_periods=20).mean()
    ewma30 = aapl_px.ewm(span=30).mean()
    assert isinstance(ma30, pd.Series)
    assert isinstance(ewma30, pd.Series)
    print(ma30.tail())
    print(ewma30.tail())


def explain_binary_window() -> None:
    """
    Problem: compute a rolling statistic between TWO time series.
    Why: operators like correlation need two series. After `rolling`, the `corr`
    aggregation computes the rolling correlation of one series with another (e.g.
    a stock's returns vs. a benchmark index). Calling it on a whole DataFrame
    computes every column's rolling correlation against the benchmark at once.
    """
    print("== Binary moving window functions (rolling corr) ==")

    close_px_all = _make_close_px()
    close_px = close_px_all[["AAPL", "MSFT", "XOM"]].resample("B").ffill()
    spx_rets = close_px_all["SPX"].pct_change()
    returns = close_px.pct_change()

    # Six-month (125-day) rolling correlation of AAPL returns with the S&P 500.
    corr = returns["AAPL"].rolling(125, min_periods=100).corr(spx_rets)
    print(corr.tail())

    # Every column's rolling correlation against the benchmark in one shot.
    corr_all = returns.rolling(125, min_periods=100).corr(spx_rets)
    print(corr_all.tail())


def explain_user_defined_window() -> None:
    """
    Problem: apply a custom reduction over each rolling window.
    Why: `rolling(...).apply(f)` runs an array function of your own over each
    window; `f` must reduce each window to a single value. Here
    `scipy.stats.percentileofscore` gives the percentile rank of a 2% return
    within each one-year (250-day) window.
    """
    print("== User-defined moving window functions (rolling().apply) ==")

    close_px_all = _make_close_px()
    close_px = close_px_all[["AAPL", "MSFT", "XOM"]].resample("B").ffill()
    returns = close_px.pct_change()

    def score_at_2percent(x: np.ndarray) -> float:
        # percentileofscore is typed as returning an ndarray; wrap in float() to
        # satisfy rolling.apply's single-value (reduction) contract.
        return float(percentileofscore(x, 0.02))

    result = returns["AAPL"].rolling(250).apply(score_at_2percent)
    print(result.tail())


def main() -> None:
    explain_rolling()
    explain_expanding()
    explain_time_offset_window()
    explain_ewm()
    explain_binary_window()
    explain_user_defined_window()


main()
