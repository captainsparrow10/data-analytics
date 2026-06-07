# Chapter 12 — Introduction to Modeling Libraries in Python

After data wrangling, the next step is usually fitting a model. This chapter is the
hand-off point: it shows how to cross back and forth between pandas data preparation and
the two most popular Python modeling toolkits, **statsmodels** (classical statistics) and
**scikit-learn** (machine learning), with **Patsy** in between as a formula language for
building design matrices. The point of contact between pandas and these libraries is the
NumPy array, so most of the work is converting frames to arrays, encoding categorical
columns, and reattaching feature names to the results.

Same format as the earlier chapters: every file is self-documenting and runnable — a
module docstring explains the topic (with a reference table), and each exercise is a
function documenting the problem, its purpose, and *why* the solution is written that way,
reproducing the book's `In [..]` examples faithfully.

## Index

The full chapter, in strict book order (12.1 → 12.4), one file per sub-section:

| File | Topic | Book section | Status |
|------|-------|--------------|--------|
| `1-pandas-model-interface.py` | pandas ↔ model code: `to_numpy`, column subsets, `get_dummies` design matrix | 12.1 | ✅ done |
| `2-patsy-formulas.py` | Patsy: `dmatrices`, no-intercept, `standardize`/`center`/`I()`, `build_design_matrices`, `C()` & interactions | 12.2 | ✅ done |
| `3-statsmodels.py` | statsmodels: OLS (array & formula APIs), `summary`/`params`/`tvalues`, AR time series (`AutoReg`) | 12.3 | ✅ done |
| `4-scikit-learn.py` | scikit-learn: impute, encode, `LogisticRegression`, `LogisticRegressionCV`, `cross_val_score` | 12.4 | ✅ done |
| `exercises.py` | Practice exercises: model matrices, `get_dummies`, scaling, OLS (array & formula), train/test split, `LinearRegression`/`LogisticRegression`, `cross_val_score` | — | ✅ done |

## Running

```bash
poetry run python cap_12_modeling/1-pandas-model-interface.py   # runs every exercise in the file
```

## Adaptations & library-version notes

The book targets older library versions and reads CSV files from disk; these files were
adapted to the installed stack (statsmodels **0.14.6**, scikit-learn **1.9.0**, patsy
**1.0.2**, pandas **3.0.3**, NumPy **2.4.6**) and kept fully self-contained:

- **No network / no data files.** The Titanic example (12.4) synthesizes a small
  Titanic-like train/test pair in code with `np.random.default_rng`, generating `Survived`
  from a logistic rule of `Pclass`, `Sex`, and `Age` so the classifier has real signal.
- **`pd.get_dummies` returns booleans by default** → file 1 passes `dtype=int` for a
  numeric design matrix.
- **`sm.tsa.AR` was removed** → file 3 uses `statsmodels.tsa.ar_model.AutoReg`, the modern
  equivalent.
- **scikit-learn `LogisticRegressionCV` defaults are changing** (`l1_ratios`, `scoring`,
  `use_legacy_attributes`) → file 4 sets them explicitly to silence `FutureWarning` while
  preserving the book's accuracy-based behavior.
- **Reproducible randomness** via `np.random.default_rng(seed=...)` throughout.

All four files run clean under `python -W error` (no Future/DeprecationWarning) and the
chapter type-checks at **0 errors** with pyright.

See the [project README](../README.md) for setup and conventions, and
[Chapter 5](../cap_05_pandas/README.md) for the established exercise pattern.
