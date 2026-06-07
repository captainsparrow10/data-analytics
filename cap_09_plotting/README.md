# Chapter 9 — Plotting and Visualization

Making informative visualizations (*plots*) is one of the most important tasks in data
analysis. This chapter builds up from the low-level **matplotlib** API — where you assemble
a figure from its base components (subplots, ticks, legends, annotations, shapes) — to the
high-level convenience methods that **pandas** adds on top, and finally to **seaborn**, a
statistical-graphics library that handles aggregation, confidence intervals, and faceting
for you.

Same format as the earlier chapters: every file is self-documenting and runnable — a module
docstring explains the topic (with a reference table where the book has one), and each
exercise is a function documenting the problem, its purpose, and *why* the solution is
written that way, reproducing the book's `In [..]` examples faithfully.

> **Headless by design.** These files never open a window. Each selects the non-interactive
> `Agg` backend *before* importing pyplot and never calls `plt.show()`. Instead every figure
> is **saved into a `tempfile.TemporaryDirectory()`** (with a printed confirmation of the
> filename and `os.path.exists`), and `plt.close("all")` runs between examples so figures do
> not accumulate. Running a file prints what it saved and then leaves **nothing** behind in
> the repo.

## Index

The full chapter, in strict book order (9.1 → 9.2), one file per section:

| File | Topic | Book section | Status |
|------|-------|--------------|--------|
| `1-matplotlib-primer.py` | Figures & subplots, `subplots_adjust`, colors/markers/line styles, ticks/labels/legends, annotations & patches, `savefig`, `plt.rc` | 9.1 | ✅ done |
| `2-pandas-seaborn.py` | Line plots, bar plots (grouped/stacked/`seaborn.barplot`), histograms & density (`plot.hist`/`plot.density`/`histplot`), scatter/point (`regplot`/`pairplot`), facet grids (`catplot`) | 9.2 | ✅ done |

## Running

```bash
poetry run python cap_09_plotting/1-matplotlib-primer.py   # runs every exercise in the file
poetry run python cap_09_plotting/2-pandas-seaborn.py
```

## Self-contained data (no network, no CSVs)

The book reads `examples/spx.csv`, `examples/tips.csv`, and `examples/macrodata.csv`. These
files rebuild small **inline synthetic equivalents** with a seeded `np.random.default_rng`,
so the examples read like the originals but require no downloads:

- **spx** → a positive, drifting random walk indexed by business days (file 1, annotations).
- **tips** → a tiny tips-like DataFrame (`total_bill`, `tip`, `smoker`, `day`, `time`,
  `size`) built by `_make_tips()` (file 2, seaborn bar/scatter/catplot examples).
- **macrodata** → a synthetic macro-style frame (`cpi`, `m1`, `tbilrate`, `unemp`) with the
  same log-difference transform (file 2, `regplot`/`pairplot`).

## matplotlib 3.10 / seaborn 0.13 / pandas 3.0 notes

The book targets older versions; these files were adapted to the installed
matplotlib **3.10.9**, seaborn **0.13.2**, pandas **3.0.3**, and NumPy **2.4.6**:

- `seaborn.distplot` was **removed** → use `seaborn.histplot` (file 2).
- seaborn uses the keyword API `x=` / `y=` / `data=` (file 2).
- `np.random.standard_normal`/`uniform` legacy calls → the seedable
  `np.random.default_rng(...)` Generator.
- Shapes (`Rectangle`, `Circle`, `Polygon`) are imported from `matplotlib.patches` (the
  `plt.*` re-exports are hidden by the type stubs).
- Dates passed to `annotate`/`text`/`set_xlim` are converted with `matplotlib.dates.date2num`
  (matplotlib's internal float date scale) — behavior-identical, and it satisfies the
  float-typed APIs.

See the [project README](../README.md) for setup and conventions, and
[Chapter 3](../cap_05_pandas/README.md) for the established exercise pattern.
