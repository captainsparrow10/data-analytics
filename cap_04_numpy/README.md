# Chapter 4 — NumPy Basics: Arrays and Vectorized Computation

NumPy (Numerical Python) is the foundation of the scientific Python stack. Its core is
the `ndarray`, a fast, memory-efficient multidimensional array that enables *vectorized*
computation — expressing operations on whole arrays at once instead of writing Python
loops. This chapter covers arrays, indexing, universal functions, array-oriented
programming, linear algebra, and pseudorandom generation.

Same format as Chapter 3: every file is self-documenting and runnable — a module
docstring explains the topic and its operations, and each exercise is a function
documenting the problem, its purpose, the input, the expected output, and *why* the
solution is written that way.

## Index

The full chapter, in strict book order (4.1 → 4.7), one file per sub-section:

| File | Topic | Book section | Status |
|------|-------|--------------|--------|
| `1-ndarray-basics.py` | Creating arrays, dtypes, shape, arithmetic | 4.1 | ✅ done |
| `2-indexing-slicing.py` | Basic/boolean/fancy indexing, transposing axes | 4.1 | ✅ done |
| `3-pseudorandom-number-generation.py` | The numpy.random generator, distributions | 4.2 | ✅ done |
| `4-universal-functions.py` | ufuncs: fast element-wise functions | 4.3 | ✅ done |
| `5-array-oriented.py` | `where`, stats, boolean methods, sorting, set logic | 4.4 | ✅ done |
| `6-file-io.py` | Saving/loading arrays (`save`, `load`, `savez`) | 4.5 | ✅ done |
| `7-linear-algebra.py` | `dot`, `@`, matrix ops, `numpy.linalg` | 4.6 | ✅ done |
| `8-random-walks.py` | The random-walk example (single + many) | 4.7 | ✅ done |

## Running

```bash
poetry run python cap_04_numpy/1-ndarray-basics.py   # runs every exercise in the file
```

NumPy comes from the project's Poetry dependencies (installed automatically by the
devcontainer). See the [project README](../README.md) for setup and conventions, and
[Chapter 3](../cap_03_built-in/README.md) for the established exercise pattern.
