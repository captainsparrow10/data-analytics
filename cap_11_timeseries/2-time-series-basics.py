"""
Time Series Basics (Section 11.2)

The basic kind of time series object in pandas is a `Series` indexed by
timestamps — often represented outside pandas as Python strings or `datetime`
objects. Once those `datetime` values are placed in a `DatetimeIndex`, the Series
behaves like any other Series: arithmetic between two differently indexed series
automatically aligns on the dates, scalar elements come back as `Timestamp`
objects, and the index stores the data as NumPy's nanosecond `datetime64`.

This file covers building a timestamp-indexed Series, label-based indexing and
selection (including passing date strings), slicing longer series by year /
year-month / `datetime` objects, range queries with `truncate`, indexing a
DataFrame on its datetime rows, and time series with DUPLICATE indices
(`is_unique`, aggregating by the index level).

KEY OPERATIONS IN THIS FILE
METHOD/ATTRIBUTE      DESCRIPTION
DatetimeIndex         Axis index built from datetimes (datetime64[ns] dtype)
ts["2001"]            String selection by year / year-month / exact date
ts[start:end]         Range slice using dates not necessarily in the series
truncate(after=)      Instance method slicing a Series between two dates
index.is_unique       Whether the timestamp index has no duplicate labels
groupby(level=0)      Aggregate observations sharing the same timestamp

Run:
    poetry run python cap_11_timeseries/2-time-series-basics.py
"""

from datetime import datetime

import numpy as np
import pandas as pd


def explain_creating_a_time_series() -> None:
    """
    Problem: build a Series whose index is a sequence of timestamps and see how
    pandas stores it.
    Why: passing a list of `datetime` objects as the index produces a
    `DatetimeIndex` under the hood (dtype `datetime64[ns]`). Arithmetic between
    two time series aligns on the dates, so non-overlapping labels yield NaN;
    scalar values pulled from the index come back as `Timestamp` objects.
    """
    print("== Creating a timestamp-indexed Series ==")

    # The book uses np.random.standard_normal; default_rng is the modern API.
    rng = np.random.default_rng(seed=12345)
    dates = [
        datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7),
        datetime(2011, 1, 8), datetime(2011, 1, 10), datetime(2011, 1, 12),
    ]
    ts = pd.Series(rng.standard_normal(6), index=dates)
    print(ts)
    print(ts.index)            # DatetimeIndex([...], dtype='datetime64[ns]')

    # Arithmetic aligns on the dates; ts[::2] keeps every second row -> NaN gaps.
    print(ts + ts[::2])

    # The index dtype is NumPy's nanosecond datetime64; scalars are Timestamps.
    print(ts.index.dtype)      # datetime64[ns]
    stamp = ts.index[0]
    print(stamp)               # Timestamp('2011-01-02 00:00:00')


def explain_indexing_selection_subsetting() -> None:
    """
    Problem: select single observations and slices from a time series.
    Why: a time series indexes like any Series — by a `Timestamp`, or, as a
    convenience, by a STRING interpretable as a date. For longer series, passing
    just a year ("2001") or a year-month ("2001-05") selects that whole span.
    Slicing also works with `datetime` objects and with date strings, and because
    the data is ordered chronologically you can slice with timestamps NOT present
    in the series to perform a range query. `truncate` is the equivalent method.
    """
    print("== Indexing, selection, subsetting ==")

    rng = np.random.default_rng(seed=12345)
    dates = [
        datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7),
        datetime(2011, 1, 8), datetime(2011, 1, 10), datetime(2011, 1, 12),
    ]
    ts = pd.Series(rng.standard_normal(6), index=dates)

    # Select by a Timestamp pulled from the index, or by a date string.
    stamp = ts.index[2]
    print(ts[stamp])
    print(ts["2011-01-10"])

    # A longer series: selecting by year, or year and month, slices that span.
    longer_ts = pd.Series(
        rng.standard_normal(1000),
        index=pd.date_range("2000-01-01", periods=1000),
    )
    print(longer_ts["2001"])       # the whole year 2001
    print(longer_ts["2001-05"])    # just May 2001

    # Slicing with datetime objects and with date strings (range query).
    print(ts[datetime(2011, 1, 7):])
    print(ts[datetime(2011, 1, 7):datetime(2011, 1, 10)])
    # "2011-01-06" is not in the index, but the slice still resolves a range.
    print(ts["2011-01-06":"2011-01-11"])

    # truncate is the instance-method equivalent of a one-sided slice.
    print(ts.truncate(after="2011-01-09"))


def explain_dataframe_datetime_index() -> None:
    """
    Problem: index a DataFrame on its rows with timestamps.
    Why: everything that works for a Series holds for a DataFrame indexing on its
    rows. `pd.date_range` builds the index here (covered fully in file 3); passing
    a date-string year-month to `.loc` selects all rows in that span.
    """
    print("== DataFrame indexed on datetime rows ==")

    rng = np.random.default_rng(seed=12345)
    # W-WED = weekly on Wednesday.
    dates = pd.date_range("2000-01-01", periods=100, freq="W-WED")
    long_df = pd.DataFrame(
        rng.standard_normal((100, 4)),
        index=dates,
        columns=["Colorado", "Texas", "New York", "Ohio"],
    )
    print(long_df.loc["2001-05"])  # all Wednesdays in May 2001


def explain_duplicate_indices() -> None:
    """
    Problem: handle a time series with multiple observations on one timestamp.
    Why: some applications record several data points for the same instant. The
    `index.is_unique` property reports whether duplicates exist. Indexing a
    duplicated timestamp yields a slice (Series), a unique one yields a scalar.
    To collapse the duplicates, `groupby(level=0)` aggregates over the (only)
    index level — `mean`, `count`, etc.
    """
    print("== Time series with duplicate indices ==")

    dates = pd.DatetimeIndex(
        ["2000-01-01", "2000-01-02", "2000-01-02", "2000-01-02", "2000-01-03"]
    )
    dup_ts = pd.Series(np.arange(5), index=dates)
    print(dup_ts)
    print(dup_ts.index.is_unique)   # False

    # Non-duplicated timestamp -> scalar; duplicated timestamp -> a Series slice.
    print(dup_ts["2000-01-03"])     # 4 (not duplicated)
    print(dup_ts["2000-01-02"])     # three rows (duplicated)

    # Aggregate the non-unique timestamps by grouping on the single index level.
    grouped = dup_ts.groupby(level=0)
    print(grouped.mean())
    print(grouped.count())


def main() -> None:
    explain_creating_a_time_series()
    explain_indexing_selection_subsetting()
    explain_dataframe_datetime_index()
    explain_duplicate_indices()


main()
