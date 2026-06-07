# Chapter 10 — Data Aggregation and Group Operations

Categorizing a dataset and applying a function to each group — an aggregation or a
transformation — is a core part of any data analysis workflow. This chapter covers pandas'
`groupby` interface and the *split-apply-combine* paradigm: split a pandas object into groups
by one or more keys, apply a function to each group, and combine the results. It then builds
up from optimized aggregations to the fully general `apply`, group transforms, and finally
pivot tables and cross-tabulations.

Same format as the earlier chapters: every file is self-documenting and runnable — a module
docstring explains the topic (with a reference table where the book has one), and each
exercise is a function documenting the problem, its purpose, and *why* the solution is written
that way, reproducing the book's `In [..]` examples faithfully. All sample data (including a
small tips-like frame standing in for the book's `tips.csv`, and a synthetic stock-price
frame) is built in code with `numpy.random.default_rng`, so the files are self-contained and
need no network access.

## Index

The full chapter, in strict book order (10.1 → 10.5), one file per sub-section:

| File | Topic | Book section | Status |
|------|-------|--------------|--------|
| `1-groupby-mechanics.py` | split-apply-combine, group by keys/arrays/columns, iterate, select columns, dict/Series/function keys, group by index level | 10.1 | ✅ done |
| `2-data-aggregation.py` | optimized methods, custom `agg`, multiple/named functions (list/dict/tuples), `as_index=False` / `reset_index` | 10.2 | ✅ done |
| `3-apply-split-apply-combine.py` | general `apply`, `group_keys=False`, quantile/bucket (`cut`/`qcut`), fill NA per group, sampling, weighted average/correlation, group-wise OLS | 10.3 | ✅ done |
| `4-group-transforms.py` | `transform` (broadcast & same-shape), normalization, "unwrapped" group operations | 10.4 | ✅ done |
| `5-pivot-tables-crosstab.py` | `pivot_table` (`margins`, `aggfunc`, `fill_value`) and `pd.crosstab` | 10.5 | ✅ done |

## Running

```bash
poetry run python cap_10_groupby/1-groupby-mechanics.py   # runs every exercise in the file
```

Type-check the whole chapter (repo policy: 0 errors, 0 warnings):

```bash
poetry run pyright cap_10_groupby
```

## pandas 3.0 / NumPy 2.x notes

The book targets older pandas; these files were adapted to the installed pandas **3.0.3** and
NumPy **2.4.6**:

- `groupby(axis="columns")` was removed → to group COLUMNS we transpose, group the rows by the
  mapping/level, aggregate, and transpose back (files 1).
- Nuisance string columns are no longer silently dropped from numeric aggregations → pass
  `numeric_only=True` to `mean()` (file 1), and name the numeric `values` explicitly in
  `pivot_table` (file 5).
- `df.groupby(...).apply(func)` now operates on the grouping columns and warns → pass
  `include_groups=False` so the applied function receives only the non-key columns (file 3).
- `Series.pct_change()` requires an explicit `fill_method=None` (file 3).
- Grouping by a `Categorical` defaults to keeping unobserved categories with a warning → pass
  `observed=True` (file 3).
- `np.in1d` → `np.isin`; passing bare NumPy ufuncs (`np.std`, `np.var`, `np.max`) to `agg` is
  deprecated → use the string aliases (`"std"`, `"var"`, `"max"`) (files 2, 3).
- Copy-on-Write is the default → assignments go through `.loc` / `.iloc`, and the OLS helper
  copies its design matrix before adding the intercept column (file 3).

For pyright, a handful of method results (e.g. `groupby(...).mean()`, `pd.cut`/`pd.qcut`,
single-column indexing inside an applied function) are typed as broad unions by the pandas
stubs; these are narrowed with a small `assert isinstance(...)` and a comment rather than a
`cast`, preserving runtime behavior.

pandas comes from the project's Poetry dependencies. See the [project README](../README.md) for
setup and conventions, and [Chapter 3](../cap_05_pandas/README.md) for the established exercise
pattern.
