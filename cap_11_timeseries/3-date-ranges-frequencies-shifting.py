"""
Date Ranges, Frequencies, and Shifting (Section 11.3)

Generic time series in pandas are assumed to be IRREGULAR — they have no fixed
frequency. For many applications, though, it is desirable to work relative to a
FIXED frequency (daily, monthly, every 15 minutes), even if that means
introducing missing values. pandas has a full suite of standard frequencies and
date offsets, plus tools to generate fixed-frequency ranges and to shift data
through time.

This file covers `pd.date_range` (start/end, `periods`, `normalize`), frequencies
and date offsets (combining `Hour`/`Minute`, string aliases like "1h30min",
week-of-month "WOM-3FRI"), shifting data with `shift` (leading and lagging,
shifting with a frequency, percent-change), and shifting dates with offset
objects (`MonthEnd`, `rollforward`/`rollback`).

KEY OPERATIONS IN THIS FILE
METHOD/CONCEPT       DESCRIPTION
date_range           Generate a DatetimeIndex of a given length/frequency
freq aliases         "D", "4h", "1h30min", "BME", "WOM-3FRI", ...
date offset objects  Hour(), Minute(), MonthEnd(); add to datetimes/Timestamps
shift(n)             Move values forward/backward, leaving the index unmodified
shift(n, freq=)      Advance the timestamps instead of the data
rollforward/back     Snap a date to the next/previous offset boundary

Run:
    poetry run python cap_11_timeseries/3-date-ranges-frequencies-shifting.py
"""

from datetime import datetime

import numpy as np
import pandas as pd
from pandas.tseries.offsets import Day, Hour, Minute, MonthEnd


def explain_generating_date_ranges() -> None:
    """
    Problem: generate a regular index of timestamps.
    Why: `pd.date_range` builds a `DatetimeIndex` of an indicated length at a
    given frequency. Pass start+end (daily by default), or one endpoint plus a
    `periods` count. A non-base frequency such as "BME" (business month end) only
    includes dates on or inside the interval that fall on the rule; the time of a
    start/end stamp is preserved unless `normalize=True` snaps it to midnight.
    """
    print("== Generating date ranges ==")

    # Start and end -> daily timestamps spanning the (inclusive) interval.
    index = pd.date_range("2012-04-01", "2012-06-01")
    print(index)

    # One endpoint + a periods count.
    print(pd.date_range(start="2012-04-01", periods=20))
    print(pd.date_range(end="2012-06-01", periods=20))

    # "BME" = business month end (pandas 3.0 renamed the old "BM" alias).
    print(pd.date_range("2000-01-01", "2000-12-01", freq="BME"))

    # By default the time of the start/end stamp is preserved...
    print(pd.date_range("2012-05-02 12:56:31", periods=5))
    # ...but normalize=True snaps each timestamp to midnight.
    print(pd.date_range("2012-05-02 12:56:31", periods=5, normalize=True))


def explain_frequencies_and_offsets() -> None:
    """
    Problem: express richer frequencies than the single-letter base aliases.
    Why: a frequency is a base frequency plus a multiplier. Date-offset objects
    (`Hour`, `Minute`, ...) can be multiplied by an integer and ADDED together,
    and the equivalent string aliases ("4h", "1h30min", "90min") are parsed to
    the same thing. The "week of month" class (WOM) yields dates like the third
    Friday of each month.
    """
    print("== Frequencies and date offsets ==")

    # Offset objects multiply and add. (pandas 3.0 uses lowercase 'h'/'min'.)
    print(Hour(4))                 # <4 * Hours>
    print(Hour(2) + Minute(30))    # <150 * Minutes>

    # The same expressed as string aliases passed to date_range.
    print(pd.date_range("2000-01-01", "2000-01-03 23:59", freq="4h"))
    print(pd.date_range("2000-01-01", periods=10, freq="1h30min"))

    # Week of month: the third Friday of each month.
    monthly_dates = pd.date_range("2012-01-01", "2012-09-01", freq="WOM-3FRI")
    print(list(monthly_dates))


def explain_shifting_data() -> None:
    """
    Problem: move data backward and forward through time.
    Why: `shift(n)` does a naive shift — values move, the index does NOT — which
    introduces NaN at one end and is the natural way to compute percent changes
    (`ts / ts.shift(1) - 1`). Passing a `freq` instead advances the TIMESTAMPS,
    keeping all the data; other frequencies (e.g. "90min") give flexible leads
    and lags.
    """
    print("== Shifting (leading and lagging) data ==")

    rng = np.random.default_rng(seed=12345)
    ts = pd.Series(
        rng.standard_normal(4),
        index=pd.date_range("2000-01-01", periods=4, freq="ME"),  # 3.0: "M"->"ME"
    )
    print(ts)

    # Naive shift: data moves, index unchanged -> NaN appears at one end.
    print(ts.shift(2))    # lag: NaN at the start
    print(ts.shift(-2))   # lead: NaN at the end

    # A common use: consecutive percent changes.
    print(ts / ts.shift(1) - 1)

    # Passing a freq advances the timestamps and keeps every value.
    print(ts.shift(2, freq="ME"))
    print(ts.shift(3, freq="D"))
    print(ts.shift(1, freq="90min"))  # T (minutes) was renamed to 'min' in 3.0


def explain_shifting_dates_with_offsets() -> None:
    """
    Problem: shift individual dates using offset objects, snapping to boundaries.
    Why: date offsets work directly with `datetime`/`Timestamp`. Adding a plain
    offset like `3 * Day()` is a simple shift; adding an ANCHORED offset like
    `MonthEnd` first "rolls forward" to the next boundary. The `rollforward` and
    `rollback` methods snap a date explicitly, which pairs nicely with `groupby`.
    """
    print("== Shifting dates with offsets ==")

    now = datetime(2011, 11, 17)
    print(now + 3 * Day())          # 2011-11-20 (plain shift)

    # An anchored offset rolls forward to the boundary first.
    print(now + MonthEnd())         # 2011-11-30
    print(now + MonthEnd(2))        # 2011-12-31

    # Explicit snapping with rollforward / rollback.
    offset = MonthEnd()
    print(offset.rollforward(now))  # 2011-11-30
    print(offset.rollback(now))     # 2011-10-31

    # A creative use: roll each date to its month end, then group.
    rng = np.random.default_rng(seed=12345)
    ts = pd.Series(
        rng.standard_normal(20),
        index=pd.date_range("2000-01-15", periods=20, freq="4D"),
    )
    print(ts.groupby(MonthEnd().rollforward).mean())
    # The easier, faster equivalent is resample (covered in file 6).
    print(ts.resample("ME").mean())


def main() -> None:
    explain_generating_date_ranges()
    explain_frequencies_and_offsets()
    explain_shifting_data()
    explain_shifting_dates_with_offsets()


main()
