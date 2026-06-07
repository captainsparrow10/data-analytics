# Chapter 8 — Data Wrangling: Join, Combine, and Reshape

In many applications data is spread across multiple files or arranged in a shape that is not
convenient to analyze. This chapter covers the tools to combine, join, and rearrange data:
*hierarchical indexing* (multiple index levels on an axis, the backbone of reshaping),
database-style joins and concatenation, combining overlapping datasets, and reshaping/pivoting
between "wide" and "long" layouts.

Same format as the earlier chapters: every file is self-documenting and runnable — a module
docstring explains the topic (with a reference table where the book has one), and each exercise
is a function documenting the problem, its purpose, and *why* the solution is written that way,
reproducing the book's `In [..]` examples faithfully with the book's own sample data.

## Index

The full chapter, in strict book order (8.1 → 8.3), one file per sub-section:

| File | Topic | Book section | Status |
|------|-------|--------------|--------|
| `1-hierarchical-indexing.py` | MultiIndex Series/DataFrame, partial indexing, `unstack`/`stack`, level names, `swaplevel`, `sort_index(level=)`, `groupby(level=)`, `set_index`/`reset_index` | 8.1 | ✅ done |
| `2-merge-and-join.py` | `pd.merge` (`on`, `left_on`/`right_on`, `how`, many-to-many, multiple keys, `suffixes`), merging on index, `DataFrame.join` | 8.2 | ✅ done |
| `3-concatenate-and-combine.py` | `np.concatenate` vs `pd.concat` (`axis`, `join`, `keys`, `ignore_index`), `np.where` + `combine_first` | 8.2 | ✅ done |
| `4-reshaping-pivoting.py` | `stack`/`unstack` in depth, `pivot` (long → wide), `melt` (wide → long) | 8.3 | ✅ done |
| `exercises.py` | Practice exercises | 8.1–8.3 | ✅ done |

## Running

```bash
poetry run python cap_08_wrangling/1-hierarchical-indexing.py   # runs every exercise in the file
```

## pandas 3.0 / NumPy 2.x notes

The book targets older pandas; these files were adapted to the installed pandas **3.0.3** and
NumPy **2.4.6**:

- `DataFrame.groupby(axis="columns")` was removed → aggregate columns by level with
  `frame.T.groupby(level=...).sum().T` (file 1).
- `swaplevel`'s pandas-stubs type only accepts axis positions, so we pass the level numbers
  `0`/`1` instead of the level names the book uses — they identify the same levels (file 1).
- `DataFrame.stack(dropna=...)` was removed: the new `stack` KEEPS the NA placeholders, so
  drop them explicitly with `.dropna()` (file 4).
- `pd.PeriodIndex(year=, quarter=)` was removed → use `pd.PeriodIndex.from_fields(...)` and
  `.rename("date")` (file 4).
- Random data uses `np.random.default_rng(seed=...)` (NumPy 2.x recommended generator).
- The book reads `examples/macrodata.csv`; to stay offline that frame is rebuilt inline (file 4).

pandas comes from the project's Poetry dependencies. See the [project README](../README.md)
for setup and conventions, and [Chapter 5](../cap_05_pandas/README.md) for the established
exercise pattern.
