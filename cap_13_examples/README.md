# Chapter 13 — Data Analysis Examples

The final chapter is different from chapters 6–12: instead of synthesizing data in
code, it analyzes the book's **real datasets** end to end, applying the techniques
from the whole book. Each file reproduces one of the chapter's worked examples
faithfully, in English, self-documenting and runnable.

> **This chapter downloads the book's real datasets on first run.** Each file
> fetches what it needs (one time) from the book's GitHub repo
> (`wesm/pydata-book`, 3rd edition) into a local `datasets/` cache that is
> **git-ignored** — downloaded data is never committed. If a dataset can't be
> downloaded (offline, or a file that is intentionally too large), the affected
> analysis prints a clear "download manually from …" hint and returns, so **every
> file still exits 0** in a guarded "prints a hint" mode.

Same format as the earlier chapters: a module docstring explains the topic (with a
technique table), and each exercise is an `explain_<topic>()` function documenting
the problem, its purpose, and *why* the solution is written that way — but here the
inputs are the actual book datasets rather than inline synthetic stand-ins.

## Index

The full chapter, in strict book order (13.1 → 13.5), one file per section:

| File | Topic | Book section | Status |
|------|-------|--------------|--------|
| `1-bitly-usagov.py` | Counting time zones (pure Python + pandas), agent field, Windows split | 13.1 | ✅ done |
| `2-movielens.py` | Merge three tables, mean rating by gender, rating disagreement | 13.2 | ✅ done |
| `3-baby-names.py` | Concat per-year files, births/prop, top-1000, diversity, last-letter, Lesley | 13.3 | ✅ done |
| `4-usda-food.py` | Normalize nested nutrient JSON, median by food group, max food per nutrient | 13.4 | ✅ done |
| `5-fec-campaign.py` | Party mapping, donations by occupation/state, `cut` buckets (large CSV) | 13.5 | ✅ done |

## Running

```bash
poetry run python cap_13_examples/1-bitly-usagov.py   # runs every exercise in the file
```

On the first run a file downloads its dataset into `cap_13_examples/datasets/`
(git-ignored); later runs reuse the cache. All plotting is **headless**
(`matplotlib.use("Agg")`): figures are written into a temporary directory and never
displayed, so the files run cleanly on a server.

## Datasets

| File | Dataset | Approx. size | Notes |
|------|---------|--------------|-------|
| `1-bitly-usagov.py` | `bitly_usagov/example.txt` | small | JSON lines |
| `2-movielens.py` | `movielens/{users,ratings,movies}.dat` | a few MB | `::`-separated |
| `3-baby-names.py` | `babynames/yob1880.txt … yob2010.txt` | ~25 MB total | 131 files; proceeds with whatever downloads |
| `4-usda-food.py` | `usda_food/database.json` | a few MB | nested JSON |
| `5-fec-campaign.py` | `fec/P00000001-ALL.csv` | **~150 MB** | streamed with a size cap; skipped (guarded) if it fails |

The FEC file is large, so its loader streams the download with a size cap and
**skips** (printing a hint, returning `None`) if the download fails or would exceed
the cap. The analysis is fully implemented and stays guarded either way.

## pandas 3.0 / NumPy 2.x notes

These files target the installed pandas **3.0.3** / NumPy **2.4.6**:

- `Series.value_counts()` is a method (the top-level `pd.value_counts` was removed).
- `groupby(...).apply(...)` is called with `include_groups=False` to exclude the
  grouping columns from the applied frame (pandas 3.0 behavior).
- Copy-on-Write is the default → assignments go through `.loc[...] = ...`.
- `pd.read_table(sep="::", engine="python")` is required for the multi-character
  MovieLens separator.

See the [project README](../README.md) for setup and conventions, and
[Chapter 5](../cap_05_pandas/README.md) for the established exercise pattern.
