# Challenges — your own complex exercises

A sandbox to **prove to yourself you learned this**. The chapter folders give you
worked examples (`explain_*`) and graded practice (`exercises.py`); here you design
your *own* harder, integrative problems that combine several chapters and solve
them.

This folder is intentionally separate from the book chapters and is **not** part of
the project-wide `poetry run pyright` check, so half-finished experiments never break
the repo. Type-check a challenge yourself when you want feedback (see below).

## Workflow

```bash
cp challenges/_template.py challenges/01-<topic>.py   # start from the template
poetry run python challenges/01-<topic>.py            # run it end to end
poetry run pyright challenges/01-<topic>.py           # optional: type-check it
```

Each file follows the repo shape: a module docstring, `challenge_NN() -> None`
functions (problem statement in the docstring + your solution), a `main()` runner,
and a bare `main()` call at the bottom. Build your own data with
`np.random.default_rng(seed=...)` so runs are reproducible; if you need files, use
`tempfile.TemporaryDirectory()` so nothing is left behind.

## Challenge ideas (design your own variations)

Pick a theme, write the exact problem yourself, then solve it:

1. **Sales rollup** — synthesize a daily transactions table (date, region, product,
   amount); compute monthly revenue per region with `groupby` + `resample`, find the
   top product per region, and save a headless bar chart (Agg → tempdir).
2. **Messy merge** — create two imperfect frames (duplicates, missing values,
   mismatched keys); clean both, merge them, and produce a `pivot_table` summary.
3. **Portfolio walk** — simulate many random-walk price series with NumPy, then in
   pandas compute rolling volatility, cumulative returns, and max drawdown.
4. **Vectorization race** — write a slow pure-Python loop and an equivalent NumPy
   broadcasting version; assert the results match with `np.allclose`.
5. **Mini model** — engineer features from a synthetic dataset, fit an OLS
   (statsmodels) and a `LinearRegression` (scikit-learn), and compare R² / coefficients.
6. **Time-zone report** — build a tz-aware time series, convert across zones, resample
   to business-day frequency, and flag the largest day-over-day change.

Make them progressively harder — the goal is to combine NumPy + pandas + plotting +
group ops + time series + modeling, not to repeat single-topic drills.
