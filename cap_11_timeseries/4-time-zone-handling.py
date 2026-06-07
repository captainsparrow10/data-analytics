"""
Time Zone Handling (Section 11.4)

Working with time zones is one of the most unpleasant parts of time series
manipulation. Many users work in coordinated universal time (UTC), the geography-
independent standard; other zones are expressed as offsets from UTC (e.g. New
York is four hours behind during daylight saving time, five hours behind the rest
of the year). The book uses the third-party `pytz` library, but this file uses
the Python 3.9+ standard-library `zoneinfo.ZoneInfo`, which exposes the same IANA
(Olson) time zone database that pandas understands — no extra dependency needed.

This file covers time zone localization and conversion (`tz_localize` /
`tz_convert`, generating a tz-aware range), operations with tz-aware `Timestamp`
objects (localizing, converting, the internal UTC `value`, DST-aware arithmetic),
and operations between two different time zones (the result is UTC).

KEY OPERATIONS IN THIS FILE
METHOD/CONCEPT       DESCRIPTION
ZoneInfo("...")      Standard-library tz object from the IANA database
tz_localize(tz)      Reinterpret naive timestamps as observed in a time zone
tz_convert(tz)       Convert an already-localized series to another time zone
Timestamp(..., tz=)  Build a tz-aware scalar; .value is nanoseconds since epoch
DateOffset arithmetic Respects DST transitions where possible

Run:
    poetry run python cap_11_timeseries/4-time-zone-handling.py
"""

from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from pandas.tseries.offsets import Hour


def explain_localization_and_conversion() -> None:
    """
    Problem: attach a time zone to naive timestamps and convert between zones.
    Why: by default pandas time series are time-zone NAIVE (`index.tz` is None).
    `tz_localize` REINTERPRETS naive stamps as having been observed in a given
    zone (without moving the wall-clock time); `tz_convert` then translates an
    already-localized series into another zone (changing the wall-clock display
    but not the instant). A range can also be born tz-aware via `date_range(tz=)`.
    """
    print("== Time zone localization and conversion ==")

    rng = np.random.default_rng(seed=12345)
    dates = pd.date_range("2012-03-09 09:30", periods=6)
    ts = pd.Series(rng.standard_normal(len(dates)), index=dates)
    print(ts)
    # Series.index is typed as a generic Index in the stubs; narrow to the
    # DatetimeIndex it really is so the tz / tz_localize attributes resolve.
    assert isinstance(ts.index, pd.DatetimeIndex)
    print(ts.index.tz)         # None -> naive

    # A range can be generated already localized.
    print(pd.date_range("2012-03-09 09:30", periods=10, tz="UTC"))

    # Localize the naive series to UTC, then convert to US Eastern.
    ts_utc = ts.tz_localize("UTC")
    print(ts_utc)
    print(ts_utc.index)        # dtype datetime64[ns, UTC]
    print(ts_utc.tz_convert("America/New_York"))

    # localize/convert also exist directly on a DatetimeIndex. A ZoneInfo object
    # works anywhere a zone name does (the stdlib equivalent of pytz.timezone).
    tz = ZoneInfo("Asia/Shanghai")
    print(ts.index.tz_localize(tz))


def explain_tz_aware_timestamps() -> None:
    """
    Problem: localize and convert individual `Timestamp` scalars, and observe how
    DST-aware arithmetic behaves.
    Why: like a whole series, a single `Timestamp` can be localized and converted.
    A tz-aware `Timestamp` stores a UTC value as nanoseconds since the Unix epoch,
    so `.value` is identical before and after conversion. When you add a
    `DateOffset` like `Hour()`, pandas respects DST transitions where possible.
    """
    print("== Operations with time zone-aware Timestamp objects ==")

    # Localize a naive Timestamp, then convert it.
    stamp = pd.Timestamp("2011-03-12 04:00")
    stamp_utc = stamp.tz_localize("utc")
    print(stamp_utc.tz_convert("America/New_York"))

    # A time zone can also be supplied at construction time.
    stamp_moscow = pd.Timestamp("2011-03-12 04:00", tz="Europe/Moscow")
    print(stamp_moscow)

    # The internal UTC value (ns since epoch) is unchanged by conversion.
    print(stamp_utc.value)
    print(stamp_utc.tz_convert("America/New_York").value)

    # DST-aware arithmetic: 30 minutes before springing forward (gap appears)...
    stamp = pd.Timestamp("2012-03-11 01:30", tz="US/Eastern")
    print(stamp)
    print(stamp + Hour())            # offset -0500 jumps to 03:30 -0400
    # ...and 90 minutes before falling back out of DST.
    stamp = pd.Timestamp("2012-11-04 00:30", tz="US/Eastern")
    print(stamp)
    print(stamp + 2 * Hour())        # offset -0400 changes to -0500


def explain_operations_between_time_zones() -> None:
    """
    Problem: combine two time series localized in different zones.
    Why: because timestamps are stored under the hood in UTC, combining two
    differently-localized series is a straightforward UTC operation requiring no
    conversion — the resulting index is in UTC. (Mixing tz-naive and tz-aware
    data, by contrast, raises an exception.)
    """
    print("== Operations between different time zones ==")

    rng = np.random.default_rng(seed=12345)
    dates = pd.date_range("2012-03-07 09:30", periods=10, freq="B")
    ts = pd.Series(rng.standard_normal(len(dates)), index=dates)

    # A slice of a Series is typed broadly (could be an ndarray) in the stubs;
    # narrow to Series so the tz_localize / tz_convert methods resolve.
    ts_head = ts[:7]
    assert isinstance(ts_head, pd.Series)
    ts1 = ts_head.tz_localize("Europe/London")
    ts1_tail = ts1[2:]
    assert isinstance(ts1_tail, pd.Series)
    ts2 = ts1_tail.tz_convert("Europe/Moscow")
    result = ts1 + ts2
    print(result.index)              # the combined index is in UTC


def main() -> None:
    explain_localization_and_conversion()
    explain_tz_aware_timestamps()
    explain_operations_between_time_zones()


main()
