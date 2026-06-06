# Chapter 2 — NumPy Basics: Arrays and Vectorized Computation

NumPy (Numerical Python) is the foundation of the scientific Python stack. Its core is
the `ndarray`, a fast, memory-efficient multidimensional array that enables *vectorized*
computation — expressing operations on whole arrays at once instead of writing Python
loops. This chapter covers arrays, indexing, universal functions, array-oriented
programming, linear algebra, and pseudorandom generation.

Same format as Chapter 1: every file is self-documenting and runnable — a module
docstring explains the topic and its operations, and each exercise is a function
documenting the problem, its purpose, the input, the expected output, and *why* the
solution is written that way.

## Index

> Files are added as the chapter progresses. Planned structure:

| File | Topic | Status |
|------|-------|--------|
| `1-ndarray-basics.py` | Creating arrays, dtypes, shape, arithmetic | ⏳ planned |
| `2-indexing-slicing.py` | Basic/boolean/fancy indexing, transposing axes | ⏳ planned |
| `3-universal-functions.py` | ufuncs: fast element-wise functions | ⏳ planned |
| `4-array-oriented.py` | `where`, stats, boolean methods, sorting, set logic | ⏳ planned |
| `5-linear-algebra.py` | `dot`, matrix ops, `numpy.linalg` | ⏳ planned |
| `6-random-and-walks.py` | Pseudorandom generation, the random-walk example | ⏳ planned |

## Running

```bash
python3 cap_02_numpy/1-ndarray-basics.py   # runs every exercise in the file
```

NumPy comes from the project's Poetry dependencies (installed automatically by the
devcontainer). See the [project README](../README.md) for setup and conventions, and
[Chapter 1](../cap_01_built-in/README.md) for the established exercise pattern.
