# Chapter 5 — Getting Started with pandas

pandas is the workhorse library for tabular and heterogeneous data in Python. Built on
top of NumPy, it adds two labeled data structures — the one-dimensional `Series` and the
two-dimensional `DataFrame` — whose defining feature is the *index*: every value carries a
label, so selection, filtering, arithmetic, and function application all align on those
labels automatically. This chapter covers the two data structures, Index objects, the
essential mechanics (reindexing, dropping, selecting with `loc`/`iloc`, alignment),
function application, sorting and ranking, and descriptive statistics.

Same format as the earlier chapters: every file is self-documenting and runnable — a
module docstring explains the topic (with a reference table where the book has one), and
each exercise is a function documenting the problem, its purpose, and *why* the solution is
written that way, reproducing the book's `In [..]` examples faithfully.

## Index

The full chapter, in strict book order (5.1 → 5.3), one file per sub-section:

| File | Topic | Book section | Status |
|------|-------|--------------|--------|
| `1-series.py` | Series: creation, index, selection, dict interop, alignment, name | 5.1 | ✅ done |
| `2-dataframe.py` | DataFrame: construction, columns/rows, `loc`/`iloc`, `del`, `.T`, `to_numpy` | 5.1 | ✅ done |
| `3-index-objects.py` | Index objects: immutability, set logic, duplicates, methods | 5.1 | ✅ done |
| `4-essential-functionality.py` | Reindex, drop, indexing/filtering, arithmetic & alignment | 5.2 | ✅ done |
| `5-function-sorting-ranking.py` | `apply`/`map`, `sort_index`/`sort_values`, `rank`, duplicate labels | 5.2 | ✅ done |
| `6-descriptive-statistics.py` | Reductions, `describe`, `corr`/`cov`/`corrwith`, unique/counts/membership | 5.3 | ✅ done |
| `exercises.py` | Practice exercises | — | ✅ done |

## Running

```bash
poetry run python cap_05_pandas/1-series.py   # runs every exercise in the file
```

## pandas 3.0 / NumPy 2.x notes

The book targets older pandas; these files were adapted to the installed pandas **3.0.3**
and NumPy **2.4.6**:

- `DataFrame.applymap` was removed → use `DataFrame.map` (file 5).
- `pd.value_counts` (top-level function) was removed → use the `Series`/`DataFrame`
  `.value_counts()` method (file 6).
- Copy-on-Write is the default → assignments go through `.loc[...] = ...`.

pandas comes from the project's Poetry dependencies. See the [project README](../README.md)
for setup and conventions, and [Chapter 4](../cap_04_numpy/README.md) for the established
exercise pattern.
