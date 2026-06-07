# Chapter 7 — Data Cleaning and Preparation

A significant amount of an analyst's time goes into data preparation: loading,
cleaning, transforming, and rearranging. This chapter collects pandas' high-level
tools for that work — handling missing data, removing duplicates, transforming and
replacing values, discretizing and binning, detecting outliers, sampling, building
indicator/dummy variables, nullable extension data types, string manipulation
(built-in methods, regular expressions, and the vectorized `.str` accessor), and
the `Categorical` extension type.

Same format as the earlier chapters: every file is self-documenting and runnable — a
module docstring explains the topic (with a reference table where the book has one), and
each exercise is a function documenting the problem, its purpose, and *why* the solution is
written that way, reproducing the book's `In [..]` examples faithfully.

## Index

The full chapter, in strict book order (7.1 → 7.5), one file per sub-section:

| File | Topic | Book section | Status |
|------|-------|--------------|--------|
| `1-handling-missing-data.py` | Detecting NA (`isna`/`notna`), filtering (`dropna`, `how`, `axis`, `thresh`), filling (`fillna`, dict, `ffill`/`limit`, mean) | 7.1 | ✅ done |
| `2-data-transformation.py` | Duplicates (`duplicated`/`drop_duplicates`, `subset`/`keep`), `map`, `replace`, renaming (`index.map`, `rename`) | 7.2 | ✅ done |
| `3-discretization-outliers-sampling-dummies.py` | `cut`/`qcut`, outlier detect & cap, permutation/`take`/`sample`, `get_dummies` & genres `str.get_dummies` | 7.2 | ✅ done |
| `4-extension-data-types.py` | Nullable `Int64`/`boolean`/`string`, `pd.NA`, `astype`, Arrow-backed dtypes | 7.3 | ✅ done |
| `5-string-manipulation.py` | Built-in string methods, `re` (split/findall/match/sub/groups), pandas `.str` accessor | 7.4 | ✅ done |
| `6-categorical-data.py` | Dimension tables, `Categorical`/`from_codes`, computations (`qcut`/groupby), `.cat` methods | 7.5 | ✅ done |

## Running

```bash
poetry run python cap_07_cleaning/1-handling-missing-data.py   # runs every exercise in the file
```

## pandas 3.0 / NumPy 2.x notes

The book targets older pandas; these files were adapted to the installed pandas **3.0.3**
and NumPy **2.4.6**:

- `pd.value_counts` (top-level function) was removed → use the `Series`/`DataFrame`
  `.value_counts()` method (files 1, 3, 6).
- `fillna(method="ffill")` was removed → use the dedicated `ffill()` method (file 1).
- `pd.get_dummies` now returns boolean columns by default → pass `dtype=int` for 0/1
  integers as the book shows (files 3, 6).
- Legacy global random functions (`np.random.randn`, `np.random.permutation`) are replaced
  by `np.random.default_rng(seed=...)` generators (files 1, 3, 6).
- Copy-on-Write is the default → assignments go through `.loc[...] = ...` where needed.

pandas comes from the project's Poetry dependencies. See the [project README](../README.md)
for setup and conventions, and [Chapter 5](../cap_05_pandas/README.md) for the established
exercise pattern.
