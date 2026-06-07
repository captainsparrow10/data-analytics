# Chapter 11 — Time Series

Time series data — anything recorded repeatedly at many points in time — is a central form of
structured data in finance, economics, ecology, and beyond. This chapter builds up the pandas
time series toolkit from the ground: the standard-library `datetime`/`timedelta` types and their
pandas counterparts (`Timestamp`, `DatetimeIndex`), timestamp-indexed Series and their flexible
date-based selection, generating fixed-frequency ranges and shifting data through time, time zone
localization and conversion, `Period`/`PeriodIndex` arithmetic and frequency conversion,
resampling (down/upsampling, OHLC, grouped time resampling), and moving window functions
(`rolling`, `expanding`, `ewm`).

Same format as the earlier chapters: every file is self-documenting and runnable — a module
docstring explains the topic (with a reference table where the book has one), and each exercise is
a function documenting the problem, its purpose, and *why* the solution is written that way,
reproducing the book's `In [..]` examples faithfully.

## Index

The full chapter, in strict book order (11.1 → 11.7), one file per sub-section:

| File | Topic | Book section | Status |
|------|-------|--------------|--------|
| `1-date-time-types.py` | `datetime`/`timedelta`, `strftime`/`strptime`, `dateutil.parser.parse`, `pd.to_datetime`, `NaT` | 11.1 | ✅ done |
| `2-time-series-basics.py` | Timestamp-indexed Series, string/`datetime` selection & slicing, `truncate`, duplicate indices | 11.2 | ✅ done |
| `3-date-ranges-frequencies-shifting.py` | `date_range` (freq, `normalize`), offsets ("1h30min", "WOM-3FRI"), `shift`, `rollforward`/`rollback` | 11.3 | ✅ done |
| `4-time-zone-handling.py` | `tz_localize`/`tz_convert`, `zoneinfo`, tz-aware `Timestamp`, ops between zones | 11.4 | ✅ done |
| `5-periods.py` | `Period`/`period_range`, `PeriodIndex`, `asfreq`, quarterly frequencies, `to_period`/`to_timestamp` | 11.5 | ✅ done |
| `6-resampling.py` | `resample` API, downsampling (OHLC, `closed`/`label`), upsampling (`asfreq`/`ffill`), `pd.Grouper` | 11.6 | ✅ done |
| `7-moving-window-functions.py` | `rolling` (`min_periods`, offset window), `expanding`, `ewm`, rolling `corr`, `rolling().apply` | 11.7 | ✅ done |

## Running

```bash
poetry run python cap_11_timeseries/1-date-time-types.py   # runs every exercise in the file
```

## Self-contained data

The book's resampling and moving-window sections read `examples/stock_px.csv` / `volume.csv`. To
stay offline and deterministic, `7-moving-window-functions.py` synthesizes a daily price DataFrame
(columns `AAPL`, `MSFT`, `XOM`, `SPX`) with `pd.date_range` + a seeded
`np.random.default_rng` cumulative-sum random walk. Every file uses fixed RNG seeds, so output is
reproducible. Time zones come from the standard-library `zoneinfo` module (no `pytz` dependency).

## pandas 3.0 / NumPy 2.x notes

The book targets older pandas; these files were adapted to the installed pandas **3.0.3** and
NumPy **2.4.6**:

- Frequency aliases changed: lowercase `"h"`/`"min"`/`"s"` (uppercase `"H"`/`"T"`/`"S"` removed),
  and `"ME"`/`"BME"`/`"Y-DEC"`/`"Y-JUN"` replace `"M"`/`"BM"`/`"A-DEC"`/`"A-JUN"` (files 3, 5, 6).
- `Series.resample(..., kind="period")` was removed → resample to timestamps then `.to_period()`
  (file 6).
- `pd.PeriodIndex(year=..., quarter=...)` was removed → `pd.PeriodIndex.from_fields(...)` (file 5).
- `Period` with the business-day (`"B"`) frequency is deprecated → use calendar daily `"D"` for the
  quarterly fiscal-year computation (file 5).
- Copy-on-Write is the default → index reassignments go through `obj.index = ...`.
- Default timestamp resolution is **`us`** (microseconds) on pandas 3.0 — `DatetimeIndex` dtype
  is `datetime64[us]` (or `datetime64[us, tz]`) rather than the older `datetime64[ns]` (files 1, 2, 4).

pandas comes from the project's Poetry dependencies. See the [project README](../README.md) for
setup and conventions, and [Chapter 5](../cap_05_pandas/README.md) for the established exercise
pattern.
