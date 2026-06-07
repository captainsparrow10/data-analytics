"""
Date and Time Data Types and Tools (Section 11.1)

Time series data is an important form of structured data: anything recorded
repeatedly at many points in time forms a time series. The Python standard
library ships the building blocks for working with individual instants: the
`datetime`, `time`, and `calendar` modules. The `datetime.datetime` type (simply
`datetime`) stores both a date and a time down to the microsecond, and
`datetime.timedelta` represents the temporal difference between two `datetime`
values. pandas, in contrast, is oriented toward *arrays* of dates: `Timestamp`
(its scalar) and `DatetimeIndex` (its axis), built on NumPy's nanosecond-
resolution `datetime64` dtype.

This file covers `datetime`/`timedelta` arithmetic, formatting and parsing a
single instant (`str`/`strftime` and `strptime`), the looser parsing offered by
`dateutil.parser.parse`, the array-oriented `pd.to_datetime`, and `NaT`, the
pandas null value for timestamp data.

TYPES IN THE datetime MODULE
TYPE        DESCRIPTION
date        Store a calendar date (year, month, day) in the Gregorian calendar
time        Store a time of day as hours, minutes, seconds, microseconds
datetime    Store both date and time
timedelta   The difference between two datetime values (days, seconds, micros)
tzinfo      Base type for storing time zone information

Run:
    poetry run python cap_11_timeseries/1-date-time-types.py
"""

from datetime import datetime, timedelta

import pandas as pd
from dateutil.parser import parse


def explain_datetime_and_timedelta() -> None:
    """
    Problem: capture an instant in time and the span between two instants.
    Why: `datetime.now()` returns the current moment, exposing `.year`, `.month`,
    `.day`, etc. Subtracting two `datetime` objects yields a `timedelta`, whose
    `.days` and `.seconds` decompose the difference; adding/subtracting a
    `timedelta` (or a multiple of one) shifts a `datetime` to a new instant.
    """
    print("== datetime and timedelta ==")

    now = datetime.now()
    print(now)
    print(now.year, now.month, now.day)

    # The difference between two datetimes is a timedelta.
    delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15)
    print(delta)              # 926 days, 15:45:00
    print(delta.days)         # 926
    print(delta.seconds)      # 56700

    # Adding/subtracting a timedelta (or a multiple) yields a shifted datetime.
    start = datetime(2011, 1, 7)
    print(start + timedelta(12))      # 2011-01-19 00:00:00
    print(start - 2 * timedelta(12))  # 2010-12-14 00:00:00


def explain_string_to_datetime() -> None:
    """
    Problem: turn a `datetime` into a string and parse a string back into one.
    Why: `str(stamp)` or `stamp.strftime(fmt)` format a `datetime` with explicit
    format codes (e.g. "%Y-%m-%d"). The inverse, `datetime.strptime`, parses a
    string with a KNOWN format — ideal when the layout is fixed and uniform.
    """
    print("== Converting between string and datetime (strftime / strptime) ==")

    stamp = datetime(2011, 1, 3)
    print(str(stamp))                  # '2011-01-03 00:00:00'
    print(stamp.strftime("%Y-%m-%d"))  # '2011-01-03'

    # strptime parses a string with a known format specification.
    value = "2011-01-03"
    print(datetime.strptime(value, "%Y-%m-%d"))  # datetime(2011, 1, 3, 0, 0)

    datestrs = ["7/6/2011", "8/6/2011"]
    print([datetime.strptime(x, "%m/%d/%Y") for x in datestrs])


def explain_dateutil_parse() -> None:
    """
    Problem: parse dates whose exact format you do not want to spell out.
    Why: `dateutil.parser.parse` recognizes most human date representations
    without a format string. It is convenient but imperfect — it can read day-
    first layouts via `dayfirst=True`, and will happily interpret ambiguous
    strings (e.g. "42" becomes a year), so it is best for exploratory parsing.
    """
    print("== dateutil.parser.parse (flexible parsing) ==")

    print(parse("2011-01-03"))                  # datetime(2011, 1, 3, 0, 0)
    print(parse("Jan 31, 1997 10:45 PM"))       # natural-language date + time
    # In international locales the day often comes first; dayfirst handles it.
    print(parse("6/12/2011", dayfirst=True))    # datetime(2011, 12, 6, 0, 0)


def explain_pandas_to_datetime() -> None:
    """
    Problem: parse a whole ARRAY of date strings into a pandas index.
    Why: pandas is array-oriented — `pd.to_datetime` parses many standard formats
    (e.g. ISO 8601) quickly, returning a `DatetimeIndex`. It also handles values
    that should be considered missing (None, empty string), turning them into
    `NaT` (Not a Time), pandas's null value for timestamp data; `pd.isna` flags
    those entries.
    """
    print("== pd.to_datetime and NaT ==")

    datestrs = ["2011-07-06 12:00:00", "2011-08-06 00:00:00"]
    idx = pd.to_datetime(datestrs)
    print(idx)                       # DatetimeIndex([...], dtype='datetime64[ns]')

    # Missing-like values become NaT, the timestamp null.
    idx_with_na = pd.to_datetime(datestrs + [None])
    print(idx_with_na)
    print(idx_with_na[2])            # NaT
    print(pd.isna(idx_with_na))      # array([False, False,  True])


def main() -> None:
    explain_datetime_and_timedelta()
    explain_string_to_datetime()
    explain_dateutil_parse()
    explain_pandas_to_datetime()


main()
