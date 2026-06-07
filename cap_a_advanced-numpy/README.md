# Appendix A — Advanced NumPy

A deeper pass over the NumPy library: the internals of the `ndarray`, more advanced
array manipulation, broadcasting, advanced `ufunc` usage, structured/record arrays,
and the full sorting toolkit. This appendix goes beyond the day-to-day NumPy of
Chapter 4 into the mechanics that make arrays fast and flexible.

Same format as the chapters: every file is self-documenting and runnable — a module
docstring explains the topic and its operations, and each exercise is a function
documenting the problem, its purpose, and *why* the solution is written that way.

## Index

The appendix in strict book order (A.1 → A.6), one file per sub-section:

| File | Topic | Book section | Status |
|------|-------|--------------|--------|
| `1-ndarray-internals.py` | Data pointer/dtype/shape/strides, `flags`, C vs Fortran contiguity, dtype hierarchy (`issubdtype`, `mro`) | A.1 | ✅ done |
| `2-advanced-array-manipulation.py` | `reshape`/`ravel`/`flatten`, C vs FORTRAN order, `concatenate`/`vstack`/`split`/`r_`/`c_`, `repeat`/`tile`, `take`/`put` | A.2 | ✅ done |
| `3-broadcasting.py` | The broadcasting rule, broadcasting over other axes, `reshape`/`newaxis`, setting values by broadcasting | A.3 | ✅ done |
| `4-advanced-ufuncs.py` | ufunc methods `reduce`/`accumulate`/`outer`/`reduceat`, writing ufuncs (`frompyfunc`, `vectorize`) | A.4 | ✅ done |
| `5-structured-arrays.py` | Structured dtypes, field access, nested & multidimensional fields, why use them | A.5 | ✅ done |
| `6-sorting.py` | In-place vs copy sorts, `argsort`/`lexsort`, stable `mergesort`, `partition`/`argpartition`, `searchsorted` | A.6 | ✅ done |
| `exercises.py` | Practice exercises | A.1–A.6 | ✅ done |

## Running

```bash
poetry run python cap_a_advanced-numpy/1-ndarray-internals.py   # runs every exercise in the file
```

All examples are self-contained and deterministic — sample data is built in code with
`np.random.default_rng(seed=...)`, so there is no network or external data dependency.

This folder is kept under **full pyright strict** (`reportUnknown*` re-enabled to error,
like `cap_04_numpy`), since NumPy ships complete type stubs:

```bash
poetry run pyright cap_a_advanced-numpy   # 0 errors, 0 warnings
```

See the [project README](../README.md) for setup and conventions, and
[Chapter 4](../cap_04_numpy/README.md) for the foundational NumPy material this
appendix builds on.
