# data-analytics

Study workspace for Python fundamentals and data analysis. Each topic is a single,
self-documenting, runnable Python file: a module docstring explains the type/topic and
its operators, and every exercise is a function with a docstring covering the problem,
its purpose, the given input, the expected output, and *why* the solution is written
that way.

The exercises are adapted from the [PYnative](https://pynative.com/) practice sets.

## Chapters

| # | Chapter | Index |
|---|---------|-------|
| 3 | Built-in Data Structures, Functions, and Files | [cap_03_built-in/](cap_03_built-in/README.md) |
| 4 | NumPy Basics: Arrays and Vectorized Computation | [cap_04_numpy/](cap_04_numpy/README.md) |
| 5 | Getting Started with pandas | [cap_05_pandas/](cap_05_pandas/README.md) |
| 6 | Data Loading, Storage, and File Formats | [cap_06_io/](cap_06_io/README.md) |
| 7 | Data Cleaning and Preparation | [cap_07_cleaning/](cap_07_cleaning/README.md) |
| 8 | Data Wrangling: Join, Combine, and Reshape | [cap_08_wrangling/](cap_08_wrangling/README.md) |
| 9 | Plotting and Visualization | [cap_09_plotting/](cap_09_plotting/README.md) |
| 10 | Data Aggregation and Group Operations | [cap_10_groupby/](cap_10_groupby/README.md) |
| 11 | Time Series | [cap_11_timeseries/](cap_11_timeseries/README.md) |
| 12 | Introduction to Modeling Libraries | [cap_12_modeling/](cap_12_modeling/README.md) |
| 13 | Data Analysis Examples | [cap_13_examples/](cap_13_examples/README.md) |
| A | Advanced NumPy (appendix) | [cap_a_advanced-numpy/](cap_a_advanced-numpy/README.md) |

## Chapter 3 — Built-ins (`cap_03_built-in/`)

```
cap_03_built-in/
├── data-structures/
│   ├── 1-tupple.py            # tuples            (25 exercises)
│   ├── 2-list.py              # lists             (45 exercises)
│   ├── 3-set.py               # sets              (31 exercises)
│   ├── 4-dictionary.py        # dictionaries      (40 exercises)
│   └── 5-string.py            # strings           (38 exercises)
├── control-flow/
│   └── 1-if-else-for-loop.py  # conditionals/loops (40 exercises)
├── functions/
│   ├── 1-functions.py         # functions          (18 exercises)
│   └── 2-iterators-generators.py  # iterators/generators (30 exercises)
├── files/
│   ├── 1-file-handling.py     # file I/O           (34 exercises)
│   └── 2-json.py              # JSON               (9 exercises)
├── io/
│   └── 1-input-output.py      # input & output     (23 exercises)
└── stdlib/
    ├── 1-regex.py             # regular expressions (30 exercises)
    └── 2-random.py            # random / secrets    (10 exercises)
```

## Chapter 5 — pandas (`cap_05_pandas/`)

```
cap_05_pandas/
├── 1-series.py                    # Series: creation, index, selection, dict interop, name   (5.1)
├── 2-dataframe.py                 # DataFrame: construction, loc/iloc, del, .T, to_numpy      (5.1)
├── 3-index-objects.py             # Index: immutability, set logic, duplicates, methods       (5.1)
├── 4-essential-functionality.py   # reindex, drop, indexing/filtering, arithmetic & alignment (5.2)
├── 5-function-sorting-ranking.py  # apply/map, sort_index/sort_values, rank, duplicate labels (5.2)
└── 6-descriptive-statistics.py    # reductions, describe, corr/cov/corrwith, unique/counts    (5.3)
```

## Chapter 6 — data loading (`cap_06_io/`)

```
cap_06_io/
├── 1-reading-writing-text.py  # read_csv options, nrows/chunksize, to_csv, csv module (6.1)
├── 2-json-xml-html.py         # JSON, read_html, read_xml                             (6.1)
├── 3-binary-formats.py        # pickle, Excel, HDF5                                   (6.2)
├── 4-web-apis.py              # GitHub-issues requests example (offline)             (6.3)
└── 5-databases.py             # SQLite via sqlite3, then SQLAlchemy + read_sql        (6.4)
```

## Chapter 7 — data cleaning (`cap_07_cleaning/`)

```
cap_07_cleaning/
├── 1-handling-missing-data.py                       # isna/notna, dropna, fillna/ffill   (7.1)
├── 2-data-transformation.py                         # duplicates, map, replace, rename   (7.2)
├── 3-discretization-outliers-sampling-dummies.py    # cut/qcut, outliers, sample, dummies(7.2)
├── 4-extension-data-types.py                        # Int64/string/boolean, pd.NA, Arrow (7.3)
├── 5-string-manipulation.py                         # built-ins, re module, .str accessor (7.4)
└── 6-categorical-data.py                            # Categorical, codes/categories, .cat (7.5)
```

## Chapter 8 — data wrangling (`cap_08_wrangling/`)

```
cap_08_wrangling/
├── 1-hierarchical-indexing.py     # MultiIndex, unstack/stack, swaplevel, set_index/reset_index (8.1)
├── 2-merge-and-join.py            # pd.merge (on/how/keys/suffixes), merge on index, join        (8.2)
├── 3-concatenate-and-combine.py   # np.concatenate vs pd.concat, combine_first                   (8.2)
└── 4-reshaping-pivoting.py        # stack/unstack, pivot (long→wide), melt (wide→long)           (8.3)
```

## Chapter 9 — plotting (`cap_09_plotting/`)

```
cap_09_plotting/
├── 1-matplotlib-primer.py   # figures/subplots, spacing, colors/markers/styles, ticks/labels/legends, annotations & patches, savefig, plt.rc (9.1)
└── 2-pandas-seaborn.py      # line/bar (grouped, stacked, seaborn.barplot), hist/density/histplot, regplot/pairplot, catplot facet grids        (9.2)
```

> Headless: figures are saved into a temp dir (never shown), and nothing is left in the repo.

## Chapter 10 — group operations (`cap_10_groupby/`)

```
cap_10_groupby/
├── 1-groupby-mechanics.py            # split-apply-combine, keys/arrays/columns, iterate, select, dict/Series/function keys, level (10.1)
├── 2-data-aggregation.py             # optimized methods, custom/multiple/named agg (list/dict/tuples), as_index=False/reset_index    (10.2)
├── 3-apply-split-apply-combine.py    # general apply, group_keys=False, cut/qcut buckets, fill NA, sampling, wavg/corr, group-wise OLS (10.3)
├── 4-group-transforms.py             # transform (broadcast & same-shape), normalization, "unwrapped" group operations                (10.4)
└── 5-pivot-tables-crosstab.py        # pivot_table (margins, aggfunc, fill_value) and pd.crosstab                                      (10.5)
```

## Chapter 11 — time series (`cap_11_timeseries/`)

```
cap_11_timeseries/
├── 1-date-time-types.py                    # datetime/timedelta, strftime/strptime, dateutil.parse, to_datetime, NaT          (11.1)
├── 2-time-series-basics.py                 # timestamp-indexed Series, string/datetime selection & slicing, truncate, dups    (11.2)
├── 3-date-ranges-frequencies-shifting.py   # date_range, offsets (1h30min, WOM-3FRI), shift, rollforward/rollback            (11.3)
├── 4-time-zone-handling.py                 # tz_localize/tz_convert, zoneinfo, tz-aware Timestamp, ops between zones          (11.4)
├── 5-periods.py                            # Period/period_range, asfreq, quarterly freqs, to_period/to_timestamp            (11.5)
├── 6-resampling.py                         # resample, downsampling (OHLC, closed/label), upsampling (ffill), pd.Grouper     (11.6)
└── 7-moving-window-functions.py            # rolling (min_periods, offset), expanding, ewm, rolling corr, rolling().apply    (11.7)
```

## Chapter 12 — modeling libraries (`cap_12_modeling/`)

```
cap_12_modeling/
├── 1-pandas-model-interface.py  # pandas <-> models: to_numpy, column subsets, get_dummies design matrix          (12.1)
├── 2-patsy-formulas.py          # Patsy: dmatrices, no-intercept, standardize/center/I(), C() & interactions       (12.2)
├── 3-statsmodels.py             # statsmodels: OLS (array & formula APIs), summary/params/tvalues, AR via AutoReg   (12.3)
└── 4-scikit-learn.py            # scikit-learn: impute, encode, LogisticRegression(CV), cross_val_score (Titanic)  (12.4)
```

> Self-contained: the Titanic example synthesizes a Titanic-like frame in code (no CSV/network).

## Chapter 13 — data analysis examples (`cap_13_examples/`)

```
cap_13_examples/
├── 1-bitly-usagov.py   # count time zones (pure Python + pandas), agent field, Windows split   (13.1)
├── 2-movielens.py      # merge three tables, mean rating by gender, rating disagreement         (13.2)
├── 3-baby-names.py     # concat per-year files, prop, top-1000, diversity, last-letter, Lesley  (13.3)
├── 4-usda-food.py      # normalize nested nutrient JSON, median by food group, max per nutrient  (13.4)
└── 5-fec-campaign.py   # party mapping, donations by occupation/state, cut buckets (large CSV)   (13.5)
```

> Unlike the other chapters, Chapter 13 analyzes the book's **real datasets**. Each file
> downloads what it needs on first run into `cap_13_examples/datasets/` (git-ignored); the
> large FEC CSV is streamed with a size cap. Offline, every analysis prints a download hint
> and the file still exits 0.

## Running an exercise file

Each file runs end to end and prints the result of every exercise:

```bash
poetry run python cap_03_built-in/data-structures/3-set.py
```

## Conventions (read this before editing)

These conventions keep every file runnable unattended and verifiable.

1. **Non-interactive by design.** Exercises that originally used `input()` (file
   handling, input/output) instead use a fixed value, with the real call shown in a
   comment next to it (e.g. `name = "Alice"  # name = input(...)`). This lets the whole
   file run without blocking for keyboard input.

2. **Self-contained file I/O.** File and JSON exercises never touch the working
   directory. They create a `tempfile.TemporaryDirectory()`, do their work inside it,
   and clean up automatically — so running them leaves no stray files.

3. **Reproducible vs. cryptographic randomness.** In `stdlib/2-random.py`, exercises
   built on the `random` module call `random.seed()` so their output is stable on every
   run. Exercises built on the `secrets` module (OTPs, tokens) are cryptographically
   random *by design* and therefore produce different output each run — this is noted in
   their docstrings.

## Local setup (Poetry)

Dependencies are managed with [Poetry](https://python-poetry.org/). The full data stack
(numpy, pandas, matplotlib, IPython, Jupyter, SciPy, scikit-learn, statsmodels, plus
openpyxl, lxml, tables, SQLAlchemy, pyarrow, seaborn, patsy) is declared in
`pyproject.toml` using the modern PEP 621 `[project]` table; `pyright` is a dev-only
dependency. The virtualenv lives **inside the repo** at
`.venv/` (git-ignored) and is built on the single Homebrew Python — no extra Python
versions are installed.

First-time setup on macOS:

```bash
brew install python poetry                          # if not already installed
poetry config virtualenvs.in-project true           # keep the venv at ./.venv
poetry env use "$(brew --prefix)/bin/python3"       # create .venv with Homebrew Python
poetry install                                      # runtime + dev dependencies
```

Everyday use — run anything inside the environment with `poetry run`:

```bash
poetry run python cap_04_numpy/1-ndarray-basics.py  # run an exercise file
poetry shell                                        # or drop into the venv
```

Add or remove packages (updates `pyproject.toml` + `poetry.lock`):

```bash
poetry add <package>
poetry add --group dev <package>                    # dev-only tool
```

> **Heads-up if you also use the devcontainer.** It builds its own *Linux* `.venv`
> (Python under `/usr/local/bin`). That venv is invalid on a macOS host and makes every
> `poetry` command fail with `[Errno 2] No such file or directory: 'python'`. Fix: remove
> it and recreate locally — `rm -rf .venv && poetry env use "$(brew --prefix)/bin/python3"`.

## Type checking

Checked with [pyright](https://github.com/microsoft/pyright) in **strict** mode
(configured in `pyproject.toml` under `[tool.pyright]`; `venvPath`/`venv` point it at the
in-project `.venv` so third-party types resolve). Every file is kept at **0 errors**.

```bash
poetry run pyright                # whole project
poetry run pyright cap_04_numpy   # a single chapter
```
