"""
Resampling and Frequency Conversion (Section 11.6)

*Resampling* is converting a time series from one frequency to another.
Aggregating higher-frequency data down to a lower frequency is DOWNSAMPLING;
going the other way is UPSAMPLING. (Not every conversion is one of these — W-WED
to W-FRI is neither.) The `resample` method is the workhorse for all frequency
conversion; its API mirrors `groupby`: you call `resample` to bin the data, then
an aggregation.

This file covers the `resample` API, downsampling (five-minute bars, `closed` /
`label`, shifting the result index with an offset, OHLC), upsampling and
interpolation (`asfreq`, `ffill` with a `limit`), resampling data indexed by
periods, and grouped time resampling with `pd.Grouper`.

resample METHOD ARGUMENTS (selected)
ARGUMENT      DESCRIPTION
rule          The target frequency ("ME", "5min", ...)
closed        Which end of each downsampling bin is inclusive ("left"/"right")
label         Whether to label a bin by its left or right edge
limit         Max number of periods to fill when forward/backward filling
origin        The base timestamp used to determine the bin edges

Run:
    poetry run python cap_11_timeseries/6-resampling.py
"""

import numpy as np
import pandas as pd
from pandas.tseries.frequencies import to_offset


def explain_resample_api() -> None:
    """
    Problem: aggregate a daily series down to monthly means two ways.
    Why: `resample(rule)` returns a lazy resampler (like a GroupBy); calling an
    aggregation such as `.mean()` produces the result. The book's
    `kind="period"` argument was removed in pandas 3.0, so to get a period-indexed
    result we resample to timestamps and then call `.to_period()`.
    """
    print("== The resample API ==")

    rng = np.random.default_rng(seed=12345)
    dates = pd.date_range("2000-01-01", periods=100)
    ts = pd.Series(rng.standard_normal(len(dates)), index=dates)

    print(ts.resample("ME").mean())             # 3.0: "M" -> "ME" (month end)
    # Period-indexed result: resample then convert (replaces kind="period").
    print(ts.resample("ME").mean().to_period("M"))


def explain_downsampling() -> None:
    """
    Problem: aggregate one-minute data into five-minute bars.
    Why: downsampling chops the series into half-open intervals; each point
    belongs to exactly one bin. `closed` chooses which edge is inclusive (default
    "left") and `label` chooses which edge names the bin (default "left"). You can
    also nudge the result index by adding an offset (e.g. subtract one second).
    """
    print("== Downsampling (closed, label, offset) ==")

    dates = pd.date_range("2000-01-01", periods=12, freq="min")  # 3.0: "T"->"min"
    ts = pd.Series(np.arange(len(dates)), index=dates)
    print(ts)

    # Default: left edge inclusive, bins labeled by their left edge.
    print(ts.resample("5min").sum())
    # Make the right edge inclusive instead.
    print(ts.resample("5min", closed="right").sum())
    # Right-closed AND right-labeled.
    print(ts.resample("5min", closed="right", label="right").sum())

    # Shift the result index by subtracting one second from each (right) label.
    result = ts.resample("5min", closed="right", label="right").sum()
    result.index = result.index + to_offset("-1s")
    print(result)


def explain_ohlc() -> None:
    """
    Problem: summarize each downsampling bin with four finance statistics.
    Why: open-high-low-close (OHLC) is the standard financial bar. The built-in
    `ohlc` aggregate computes the first, max, min, and last value of each bin in a
    single call, returning a DataFrame with those four columns.
    """
    print("== Open-high-low-close (OHLC) resampling ==")

    rng = np.random.default_rng(seed=12345)
    dates = pd.date_range("2000-01-01", periods=12, freq="min")
    ts = pd.Series(rng.permutation(np.arange(len(dates))), index=dates)
    print(ts.resample("5min").ohlc())


def explain_upsampling_and_interpolation() -> None:
    """
    Problem: convert lower-frequency data UP to a higher frequency.
    Why: upsampling introduces rows that have no data, so there is nothing to
    aggregate. `asfreq()` inserts the higher-frequency index leaving NaN in the
    gaps; the same fill methods as `fillna`/`reindex` apply — `ffill()` carries
    each value forward, and `limit=` caps how many periods to fill. The new index
    need not coincide with the old one at all.
    """
    print("== Upsampling and interpolation ==")

    rng = np.random.default_rng(seed=12345)
    frame = pd.DataFrame(
        rng.standard_normal((2, 4)),
        index=pd.date_range("2000-01-01", periods=2, freq="W-WED"),
        columns=["Colorado", "Texas", "New York", "Ohio"],
    )
    print(frame)

    # asfreq inserts the daily index with NaN where there was no observation.
    print(frame.resample("D").asfreq())
    # Forward-fill each weekly value onto the non-Wednesdays.
    print(frame.resample("D").ffill())
    # Limit how far an observed value is carried forward.
    print(frame.resample("D").ffill(limit=2))
    # The resampled index need not line up with the original one.
    print(frame.resample("W-THU").ffill())


def explain_resampling_with_periods() -> None:
    """
    Problem: resample data that is indexed by periods, not timestamps.
    Why: period resampling is similar to timestamps but more rigid — downsampling
    needs a SUBperiod target, upsampling a SUPERperiod. Upsampling must also pick
    which end of the span the values go to via `convention` ("start"/"end").
    """
    print("== Resampling with periods ==")

    rng = np.random.default_rng(seed=12345)
    frame = pd.DataFrame(
        rng.standard_normal((24, 4)),
        index=pd.period_range("2000-01", "2001-12", freq="M"),
        columns=["Colorado", "Texas", "New York", "Ohio"],
    )
    print(frame.head())

    # Downsample monthly -> annual (Y-DEC; was "A-DEC" before pandas 3.0).
    annual_frame = frame.resample("Y-DEC").mean()
    print(annual_frame)

    # Upsample annual -> quarterly. convention defaults to "start"; "end" places
    # the value at the end of the span (leaving leading quarters as NaN).
    print(annual_frame.resample("Q-DEC").ffill())
    print(annual_frame.resample("Q-DEC", convention="end").asfreq())


def explain_grouped_time_resampling() -> None:
    """
    Problem: resample each of several time series stored in one DataFrame.
    Why: `resample` is a group operation over a time intervalization. With a plain
    time index, `set_index("time").resample("5min")` works directly. When a second
    "key" column distinguishes multiple series, `pd.Grouper(freq=)` lets you
    combine the time binning with that key in a single `groupby`.
    """
    print("== Grouped time resampling (pd.Grouper) ==")

    n = 15
    times = pd.date_range("2017-05-20 00:00", freq="1min", periods=n)
    df = pd.DataFrame({"time": times, "value": np.arange(n)})
    # Single series: index by time, then resample.
    print(df.set_index("time").resample("5min").count())

    # Multiple series marked by a "key" column.
    df2 = pd.DataFrame(
        {
            "time": times.repeat(3),
            "key": np.tile(["a", "b", "c"], n),
            "value": np.arange(n * 3.0),
        }
    )
    print(df2.head(7))

    # Grouper bins the time index; combine it with the key in one groupby.
    time_key = pd.Grouper(freq="5min")
    # .sum() is typed broadly (it could be a scalar); narrow to a DataFrame so
    # the .reset_index() call resolves cleanly.
    resampled = df2.set_index("time").groupby(["key", time_key]).sum()
    assert isinstance(resampled, pd.DataFrame)
    print(resampled)
    print(resampled.reset_index())


def main() -> None:
    explain_resample_api()
    explain_downsampling()
    explain_ohlc()
    explain_upsampling_and_interpolation()
    explain_resampling_with_periods()
    explain_grouped_time_resampling()


main()
