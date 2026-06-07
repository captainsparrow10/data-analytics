"""
Periods and Period Arithmetic (Section 11.5)

A *period* represents a time SPAN — days, months, quarters, years — rather than a
single instant. The `pd.Period` class stores one, requiring a string/integer plus
a supported frequency; `pd.period_range` builds ranges of them and `PeriodIndex`
serves as an axis index. Adding integers to periods shifts them by their own
frequency, and the difference of two same-frequency periods is the number of units
between them.

This file covers `Period`/`period_range` arithmetic, `PeriodIndex` (including
building one from string arrays), frequency conversion with `asfreq`, quarterly
period frequencies and a fiscal-year computation, converting timestamps to periods
and back (`to_period`/`to_timestamp`), and building a `PeriodIndex` from separate
year/quarter arrays.

KEY OPERATIONS IN THIS FILE
METHOD/CONCEPT       DESCRIPTION
Period(s, freq=)     A single time span; integer add/subtract shifts it
period_range         A regular range of periods -> PeriodIndex
PeriodIndex(arr,...) Build a period axis from an array of period strings
asfreq(freq, how=)   Convert a period to a sub/super-frequency (start or end)
to_period / to_timestamp  Move between a DatetimeIndex and a PeriodIndex
PeriodIndex.from_fields(year=, quarter=)  Combine separate arrays into a period axis

Run:
    poetry run python cap_11_timeseries/5-periods.py
"""

import numpy as np
import pandas as pd


def explain_periods_and_arithmetic() -> None:
    """
    Problem: represent a time span and shift it arithmetically.
    Why: `pd.Period("2011", freq="Y-DEC")` is the full span Jan 1 - Dec 31, 2011.
    Adding/subtracting an integer shifts the period by its own frequency; the
    DIFFERENCE of two same-frequency periods is the count of units between them.
    (pandas 3.0 renamed the annual alias "A-DEC" to "Y-DEC".)
    """
    print("== Periods and period arithmetic ==")

    # pd.Period is typed as Period | NaTType in the stubs; assert the concrete
    # Period so the arithmetic/asfreq operations below type-check cleanly.
    p = pd.Period("2011", freq="Y-DEC")   # was "A-DEC" before pandas 3.0
    assert isinstance(p, pd.Period)
    print(p)                              # Period('2011', 'Y-DEC')
    print(p + 5)                          # Period('2016', 'Y-DEC')
    print(p - 2)                          # Period('2009', 'Y-DEC')

    # Same-frequency difference -> number of units between them (a date offset).
    p2014 = pd.Period("2014", freq="Y-DEC")
    assert isinstance(p2014, pd.Period)
    print(p2014 - p)


def explain_period_range_and_index() -> None:
    """
    Problem: build regular ranges of periods and use them as an axis index.
    Why: `period_range` constructs a `PeriodIndex`; it can index any pandas object.
    If you already have an array of period strings, `PeriodIndex(values, freq=)`
    turns them straight into a period axis.
    """
    print("== period_range and PeriodIndex ==")

    periods = pd.period_range("2000-01-01", "2000-06-30", freq="M")
    print(periods)

    rng = np.random.default_rng(seed=12345)
    print(pd.Series(rng.standard_normal(6), index=periods))

    # Build a PeriodIndex directly from an array of period strings.
    values = ["2001Q3", "2002Q2", "2003Q1"]
    index = pd.PeriodIndex(values, freq="Q-DEC")
    print(index)


def explain_frequency_conversion() -> None:
    """
    Problem: convert periods (and period-indexed series) to another frequency.
    Why: `asfreq` reinterprets a period at a sub- or super-frequency, with
    `how="start"`/`"end"` choosing which end of the span. An annual "Y-DEC" period
    spans Jan-Dec, so its monthly start/end are 2011-01 / 2011-12; for a fiscal
    year ending in June ("Y-JUN") the subperiods are shifted accordingly. Whole
    period-indexed series convert with the same semantics.
    """
    print("== Period frequency conversion (asfreq) ==")

    p = pd.Period("2011", freq="Y-DEC")
    assert isinstance(p, pd.Period)
    print(p.asfreq("M", how="start"))   # Period('2011-01', 'M')
    print(p.asfreq("M", how="end"))     # Period('2011-12', 'M')

    # A fiscal year ending in June: the monthly subperiods are shifted.
    p = pd.Period("2011", freq="Y-JUN")  # was "A-JUN" before pandas 3.0
    assert isinstance(p, pd.Period)
    print(p.asfreq("M", how="start"))   # Period('2010-07', 'M')
    print(p.asfreq("M", how="end"))     # Period('2011-06', 'M')
    # Aug-2011 belongs to the 2012 fiscal year under Y-JUN.
    p_aug = pd.Period("Aug-2011", "M")
    assert isinstance(p_aug, pd.Period)
    print(p_aug.asfreq("Y-JUN"))

    # Whole series convert the same way.
    rng = np.random.default_rng(seed=12345)
    periods = pd.period_range("2006", "2009", freq="Y-DEC")
    ts = pd.Series(rng.standard_normal(len(periods)), index=periods)
    print(ts)
    print(ts.asfreq("M", how="start"))


def explain_quarterly_frequencies() -> None:
    """
    Problem: work with quarterly periods anchored to a fiscal-year end.
    Why: quarterly data is reported relative to a fiscal year end, so "2012Q4"
    means different calendar months depending on the anchor. pandas supports all
    twelve (Q-JAN..Q-DEC). Chaining `asfreq` calls plus integer/offset arithmetic
    lets you pinpoint, say, 4 P.M. on the second-to-last day of the quarter; the
    `period_range` arithmetic is identical.
    """
    print("== Quarterly period frequencies ==")

    p = pd.Period("2012Q4", freq="Q-JAN")
    assert isinstance(p, pd.Period)
    print(p)
    # For a fiscal year ending in January, 2012Q4 runs Nov 2011 - Jan 2012.
    print(p.asfreq("D", how="start"))   # Period('2011-11-01', 'D')
    print(p.asfreq("D", how="end"))     # Period('2012-01-31', 'D')

    # 4 P.M. on the second-to-last day of the quarter. The book uses the "B"
    # (business-day) period frequency, but Period-with-BDay is deprecated in
    # pandas 3.0, so we use calendar daily "D" here (same chaining technique).
    # Period - int is typed ambiguously in the stubs; narrow the intermediate
    # second-to-last day back to a Period before chaining the next asfreq.
    second_to_last = p.asfreq("D", how="end") - 1
    assert isinstance(second_to_last, pd.Period)
    p4pm = second_to_last.asfreq("min", how="start") + 16 * 60
    print(p4pm)                          # Period('2012-01-30 16:00', 'min')
    print(p4pm.to_timestamp())           # to_timestamp -> start of the period

    # period_range arithmetic is identical; converting the index to timestamps.
    periods = pd.period_range("2011Q3", "2012Q4", freq="Q-JAN")
    ts = pd.Series(np.arange(len(periods)), index=periods)
    print(ts)
    new_periods = (periods.asfreq("D", "end") - 1).asfreq("h", "start") + 16
    ts.index = new_periods.to_timestamp()
    print(ts)


def explain_timestamps_to_periods() -> None:
    """
    Problem: move between a timestamp index and a period index.
    Why: `to_period` converts a timestamp-indexed object to periods (frequency
    inferred or specified), and `to_timestamp` reverses it. Since periods are
    nonoverlapping spans, distinct timestamps within one span map to the same
    period — duplicates are fine. `to_timestamp(how="end")` lands at the span end.
    """
    print("== Converting timestamps to periods (and back) ==")

    rng = np.random.default_rng(seed=12345)
    dates = pd.date_range("2000-01-01", periods=3, freq="ME")  # 3.0: "M"->"ME"
    ts = pd.Series(rng.standard_normal(3), index=dates)
    print(ts)
    pts = ts.to_period()
    print(pts)                           # monthly periods

    # Daily timestamps spanning a month boundary -> duplicate monthly periods.
    dates = pd.date_range("2000-01-29", periods=6)
    ts2 = pd.Series(rng.standard_normal(6), index=dates)
    print(ts2.to_period("M"))

    # to_timestamp reverses it; how="end" lands at the end of each span.
    pts = ts2.to_period()
    print(pts.to_timestamp(how="end"))


def explain_periodindex_from_arrays() -> None:
    """
    Problem: build a PeriodIndex when the span is split across columns.
    Why: fixed-frequency data is sometimes stored with the time pieces in separate
    columns (e.g. a `year` column and a `quarter` column). Passing them to
    `PeriodIndex.from_fields(year=..., quarter=..., freq=...)` combines them into
    one index (pandas 3.0 replaced the old `PeriodIndex(year=...)` constructor).
    """
    print("== Creating a PeriodIndex from arrays ==")

    # The book reads examples/macrodata.csv; here we build the year/quarter
    # columns synthetically (deterministically) to stay self-contained.
    rng = np.random.default_rng(seed=12345)
    years = np.repeat(np.arange(1959, 1964), 4)        # 1959Q1 .. 1963Q4
    quarters = np.tile(np.arange(1, 5), 5)
    data = pd.DataFrame(
        {"year": years, "quarter": quarters, "infl": rng.standard_normal(20)}
    )
    print(data.head())

    # pandas 3.0 moved the year=/quarter= constructor to PeriodIndex.from_fields.
    index = pd.PeriodIndex.from_fields(
        year=data["year"], quarter=data["quarter"], freq="Q-DEC"
    )
    data.index = index
    print(data["infl"])


def main() -> None:
    explain_periods_and_arithmetic()
    explain_period_range_and_index()
    explain_frequency_conversion()
    explain_quarterly_frequencies()
    explain_timestamps_to_periods()
    explain_periodindex_from_arrays()


main()
