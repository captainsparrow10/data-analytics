"""
Time Series: Practice Exercises

A set of original, self-contained drills over the pandas time series toolkit:
parsing strings to timestamps, building fixed-frequency date ranges and
timestamp-indexed Series, date-based selection and slicing, resampling
(down/upsampling, OHLC), rolling and exponentially-weighted windows, shifting
for period-over-period change, time zone localization/conversion, and Period
arithmetic. Every series is generated in-code with `pd.date_range` and a seeded
`np.random.default_rng`, so output is fully reproducible and offline. Targets
pandas 3.0 (lowercase freq aliases like "h"/"min"/"s", "ME"/"YE" for
month/year-end, default `datetime64[us]` resolution) and stdlib `zoneinfo`.

Run:
    poetry run python cap_11_timeseries/exercises.py
"""

from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd


def exercise_01() -> None:
    """
    Exercise 1: Parse mixed date strings to timestamps

    Problem: Given a list of human-written date strings in different formats,
    convert them into a pandas DatetimeIndex.

    Purpose: With `format="mixed"`, `pd.to_datetime` infers the format of each
    element independently and returns a DatetimeIndex, the foundation for any
    timestamp-based work. (pandas 3.0 no longer guesses per-element by default.)

    Given Input: ["2026-01-05", "Feb 14, 2026", "2026/03/30"]
    Expected Output: DatetimeIndex of 2026-01-05, 2026-02-14, 2026-03-30
    """
    raw = ["2026-01-05", "Feb 14, 2026", "2026/03/30"]
    parsed = pd.to_datetime(raw, format="mixed")  # infer each element's format
    print(parsed)


def exercise_02() -> None:
    """
    Exercise 2: Coerce an invalid date to NaT

    Problem: Parse a list containing one unparseable entry without raising.

    Purpose: `errors="coerce"` turns anything unparseable into NaT (the
    time series "missing" marker) instead of throwing, which is essential when
    cleaning messy real-world inputs.

    Given Input: ["2026-01-01", "not-a-date", "2026-01-03"]
    Expected Output: middle value is NaT
    """
    raw = ["2026-01-01", "not-a-date", "2026-01-03"]
    parsed = pd.to_datetime(raw, errors="coerce")  # bad entry -> NaT
    print(parsed)
    print(f"Any missing: {parsed.isna().any()}")


def exercise_03() -> None:
    """
    Exercise 3: Build a daily date range and a timestamp-indexed Series

    Problem: Create 10 consecutive daily timestamps starting 2026-01-01 and
    attach seeded random values to form a Series.

    Purpose: `pd.date_range(..., periods=, freq="D")` is the canonical way to
    generate a fixed-frequency index; pairing it with data yields the
    timestamp-indexed Series that the rest of the chapter operates on.

    Given Input: start="2026-01-01", periods=10, freq="D"
    Expected Output: a length-10 Series indexed by daily timestamps
    """
    idx = pd.date_range(start="2026-01-01", periods=10, freq="D")
    rng = np.random.default_rng(seed=42)
    series = pd.Series(rng.integers(0, 100, size=10), index=idx)  # daily series
    print(series)
    print(f"Index dtype: {series.index.dtype}")  # datetime64[us] on pandas 3.0


def exercise_04() -> None:
    """
    Exercise 4: Select all observations within a single year

    Problem: From a daily series spanning two years, pull out only the rows
    that fall in 2026.

    Purpose: pandas lets you index a timestamp series with a partial date
    string ("2026"); it resolves to every timestamp in that year, a far more
    readable selection than building explicit boundaries.

    Given Input: daily series 2025-12-28 .. 2026-01-06
    Expected Output: only the 2026 rows
    """
    idx = pd.date_range(start="2025-12-28", periods=10, freq="D")
    rng = np.random.default_rng(seed=7)
    series = pd.Series(rng.integers(0, 50, size=10), index=idx)
    only_2026 = series.loc["2026"]  # partial-string indexing by year
    print(only_2026)


def exercise_05() -> None:
    """
    Exercise 5: Select a single month with partial-string indexing

    Problem: From a daily series covering several months, extract just the
    March 2026 rows.

    Purpose: Partial-string indexing also resolves at month granularity
    ("2026-03"), avoiding manual start/end timestamp construction.

    Given Input: daily series 2026-01-01 for 90 days
    Expected Output: the 31 rows in March 2026
    """
    idx = pd.date_range(start="2026-01-01", periods=90, freq="D")
    rng = np.random.default_rng(seed=11)
    series = pd.Series(rng.normal(size=90).round(2), index=idx)
    march = series.loc["2026-03"]  # all timestamps in March 2026
    print(f"March count: {len(march)}")
    print(march.head())


def exercise_06() -> None:
    """
    Exercise 6: Slice a series by an explicit date range

    Problem: Return the rows between 2026-02-10 and 2026-02-15 inclusive.

    Purpose: Slicing a timestamp index with a string range is inclusive of
    both endpoints (unlike positional slicing), which suits calendar windows.

    Given Input: daily series 2026-02-01 for 28 days
    Expected Output: the 6 rows from Feb 10 through Feb 15
    """
    idx = pd.date_range(start="2026-02-01", periods=28, freq="D")
    rng = np.random.default_rng(seed=3)
    series = pd.Series(rng.integers(100, 200, size=28), index=idx)
    window = series.loc["2026-02-10":"2026-02-15"]  # inclusive both ends
    print(window)


def exercise_07() -> None:
    """
    Exercise 7: Downsample to a monthly mean

    Problem: Aggregate a daily series into one mean value per calendar month.

    Purpose: `resample("ME")` bins by month-end and behaves like a GroupBy;
    chaining `.mean()` produces the standard downsample. "ME" replaces the old
    "M" alias removed in pandas 3.0.

    Given Input: daily series 2026-01-01 for 120 days
    Expected Output: 4 monthly mean values (Jan..Apr)
    """
    idx = pd.date_range(start="2026-01-01", periods=120, freq="D")
    rng = np.random.default_rng(seed=21)
    series = pd.Series(rng.normal(loc=50, scale=5, size=120), index=idx)
    monthly = series.resample("ME").mean().round(2)  # month-end means
    print(monthly)


def exercise_08() -> None:
    """
    Exercise 8: Downsample to OHLC bars

    Problem: Convert an hourly "price" series into daily open-high-low-close
    bars.

    Purpose: `resample(...).ohlc()` is a specialized aggregation that returns
    four columns per bin, the standard financial summary of a period.

    Given Input: hourly series 2026-01-01 for 72 hours
    Expected Output: a 3-row DataFrame with open/high/low/close per day
    """
    idx = pd.date_range(start="2026-01-01", periods=72, freq="h")
    rng = np.random.default_rng(seed=99)
    # random walk so values look price-like
    price = pd.Series(100 + rng.normal(size=72).cumsum(), index=idx)
    bars = price.resample("D").ohlc().round(2)  # open/high/low/close per day
    print(bars)


def exercise_09() -> None:
    """
    Exercise 9: Upsample with asfreq and forward-fill

    Problem: Take a 3-point monthly series and expand it to a daily index,
    first showing the gaps, then filling them.

    Purpose: Upsampling creates rows that did not exist; `asfreq()` leaves them
    as NaN, while `ffill()` propagates the last known value forward — a common
    way to carry a low-frequency signal onto a high-frequency grid.

    Given Input: monthly series at 2026-01-31, 2026-02-28, 2026-03-31
    Expected Output: a daily series; NaNs from asfreq, then forward-filled
    """
    idx = pd.date_range(start="2026-01-31", periods=3, freq="ME")
    monthly = pd.Series([10.0, 20.0, 30.0], index=idx)
    daily_raw = monthly.resample("D").asfreq()  # introduces NaN rows
    daily_filled = monthly.resample("D").ffill()  # carry last value forward
    assert isinstance(daily_filled, pd.Series)  # narrow for the type checker
    print(f"NaNs after asfreq: {int(daily_raw.isna().sum())}")
    print(daily_filled.head())


def exercise_10() -> None:
    """
    Exercise 10: Rolling window mean

    Problem: Compute a 7-day trailing average of a daily series.

    Purpose: `rolling(window).mean()` smooths noise by averaging each point
    with its predecessors; the first `window-1` results are NaN because the
    window is not yet full.

    Given Input: daily series 2026-01-01 for 30 days
    Expected Output: a 7-day moving average (first 6 entries NaN)
    """
    idx = pd.date_range(start="2026-01-01", periods=30, freq="D")
    rng = np.random.default_rng(seed=5)
    series = pd.Series(rng.normal(loc=20, scale=3, size=30), index=idx)
    smoothed = series.rolling(window=7).mean().round(2)  # 7-day trailing mean
    assert isinstance(smoothed, pd.Series)  # narrow for the type checker
    print(smoothed.head(10))


def exercise_11() -> None:
    """
    Exercise 11: Exponentially weighted moving average

    Problem: Smooth the same kind of daily series with an EWMA of span 7.

    Purpose: Unlike a flat rolling mean, `ewm(span=...)` weights recent points
    more heavily and yields a value from the very first row, reacting faster to
    changes.

    Given Input: daily series 2026-01-01 for 15 days
    Expected Output: an EWMA series with no leading NaNs
    """
    idx = pd.date_range(start="2026-01-01", periods=15, freq="D")
    rng = np.random.default_rng(seed=8)
    series = pd.Series(rng.normal(loc=0, scale=1, size=15).cumsum(), index=idx)
    ewma = series.ewm(span=7).mean().round(3)  # recent points weighted more
    print(ewma)


def exercise_12() -> None:
    """
    Exercise 12: Period-over-period change with shift

    Problem: Compute the day-over-day percentage change of a price series.

    Purpose: `shift(1)` moves values forward one step so each row can be
    compared with the previous one; dividing the difference by the shifted value
    gives the relative change. The first row is NaN (no prior day).

    Given Input: daily series 2026-01-01 for 6 days
    Expected Output: a percent-change series, first value NaN
    """
    idx = pd.date_range(start="2026-01-01", periods=6, freq="D")
    price = pd.Series([100.0, 102.0, 101.0, 105.0, 104.0, 110.0], index=idx)
    prev = price.shift(1)  # align each row with the previous day
    pct_change = ((price - prev) / prev * 100).round(2)  # day-over-day %
    print(pct_change)


def exercise_13() -> None:
    """
    Exercise 13: Localize then convert time zones

    Problem: Stamp a naive hourly series as UTC, then view it in New York time.

    Purpose: `tz_localize` attaches a zone to naive timestamps (no shift of the
    clock), while `tz_convert` translates already-aware timestamps to another
    zone (shifting the displayed clock). Zones come from stdlib `zoneinfo`.

    Given Input: naive hourly series 2026-06-01 00:00 for 3 hours
    Expected Output: same instants shown as UTC, then as US/Eastern (UTC-4)
    """
    idx = pd.date_range(start="2026-06-01 00:00", periods=3, freq="h")
    rng = np.random.default_rng(seed=2)
    series = pd.Series(rng.integers(0, 10, size=3), index=idx)
    utc = series.tz_localize(ZoneInfo("UTC"))  # attach UTC, no clock shift
    eastern = utc.tz_convert(ZoneInfo("America/New_York"))  # shift the clock
    print("UTC:")
    print(utc)
    print("\nUS/Eastern:")
    print(eastern)


def exercise_14() -> None:
    """
    Exercise 14: Period arithmetic and frequency conversion

    Problem: Build a range of monthly Periods, shift them forward, and convert
    the index to a quarterly frequency.

    Purpose: A `Period` represents a span of time (not an instant); `period_range`
    builds a PeriodIndex, integer addition advances whole periods, and `asfreq`
    re-expresses each period at a coarser frequency.

    Given Input: monthly periods 2026-01 .. 2026-06
    Expected Output: shifted-by-2 periods, plus their quarterly mapping
    """
    months = pd.period_range(start="2026-01", periods=6, freq="M")
    shifted = months + 2  # advance every period by two months
    quarterly = months.asfreq("Q", how="end")  # map each month to its quarter
    print("Months:", list(months.astype(str)))
    print("Shifted +2:", list(shifted.astype(str)))
    print("As quarters:", list(quarterly.astype(str)))


def exercise_15() -> None:
    """
    Exercise 15: Convert a timestamp index to periods with to_period

    Problem: Turn a daily timestamp-indexed series into a monthly-period index
    and count observations per month.

    Purpose: `to_period("M")` converts instant-based timestamps into span-based
    monthly periods, after which a groupby-style aggregation buckets the rows
    naturally by period.

    Given Input: daily series 2026-01-01 for 70 days
    Expected Output: per-month observation counts as a PeriodIndex
    """
    idx = pd.date_range(start="2026-01-01", periods=70, freq="D")
    rng = np.random.default_rng(seed=13)
    series = pd.Series(rng.normal(size=70), index=idx)
    by_month = series.to_period("M")  # timestamps -> monthly periods
    counts = by_month.groupby(level=0).count()  # rows per month
    print(counts)


def main() -> None:
    print("=== Exercise 1: Parse mixed date strings to timestamps ===")
    exercise_01()

    print("\n=== Exercise 2: Coerce an invalid date to NaT ===")
    exercise_02()

    print("\n=== Exercise 3: Build a daily date range and Series ===")
    exercise_03()

    print("\n=== Exercise 4: Select all observations within a single year ===")
    exercise_04()

    print("\n=== Exercise 5: Select a single month with partial-string indexing ===")
    exercise_05()

    print("\n=== Exercise 6: Slice a series by an explicit date range ===")
    exercise_06()

    print("\n=== Exercise 7: Downsample to a monthly mean ===")
    exercise_07()

    print("\n=== Exercise 8: Downsample to OHLC bars ===")
    exercise_08()

    print("\n=== Exercise 9: Upsample with asfreq and forward-fill ===")
    exercise_09()

    print("\n=== Exercise 10: Rolling window mean ===")
    exercise_10()

    print("\n=== Exercise 11: Exponentially weighted moving average ===")
    exercise_11()

    print("\n=== Exercise 12: Period-over-period change with shift ===")
    exercise_12()

    print("\n=== Exercise 13: Localize then convert time zones ===")
    exercise_13()

    print("\n=== Exercise 14: Period arithmetic and frequency conversion ===")
    exercise_14()

    print("\n=== Exercise 15: Convert a timestamp index to periods with to_period ===")
    exercise_15()


main()
