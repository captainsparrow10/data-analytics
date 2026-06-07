"""
Advanced ufunc Usage (Appendix A.4)

Most NumPy users only ever need the fast element-wise behavior of universal
functions (ufuncs). But each binary ufunc also carries special instance methods
for less-common vectorized operations, and you can wrap your own Python function
as a (slow) ufunc-like callable. This file covers:

  * ufunc instance methods: reduce, accumulate, outer, reduceat.
  * Writing new ufuncs in Python with np.frompyfunc and np.vectorize.

UFUNC INSTANCE METHODS
METHOD              DESCRIPTION
reduce(x)          Aggregate values by successive applications of the operation
accumulate(x)      Aggregate values, preserving all partial (running) aggregates
outer(x, y)        Apply to all pairs of x and y; result shape is x.shape + y.shape
reduceat(x, bins)  "Local" reduce / group-by over contiguous slices given bin edges
at(x, idx, b)      Perform the operation in place at the given indices

Run:
    poetry run python cap_a_advanced-numpy/4-advanced-ufuncs.py
"""

import numpy as np
from numpy.typing import NDArray


def explain_reduce() -> None:
    """
    Problem: aggregate an array down to a single value (or along an axis) using a
    binary ufunc.
    Why: reduce applies the operation pairwise across the array. np.add.reduce is
    the same as sum; np.logical_and.reduce is the same as all.
    """
    print("== ufunc reduce ==")

    arr = np.arange(10)
    print(np.add.reduce(arr))  # 45 -- same as arr.sum()
    print(arr.sum())           # 45

    # logical_and.reduce checks "are all True". Use it to test sortedness.
    my_rng = np.random.default_rng(12346)  # for reproducibility
    arr = my_rng.standard_normal((5, 5))
    arr[::2].sort(1)  # sort a few rows so some rows are ascending
    # Within each row, is every element < its right neighbor?
    print(arr[:, :-1] < arr[:, 1:])
    print(np.logical_and.reduce(arr[:, :-1] < arr[:, 1:], axis=1))


def explain_accumulate() -> None:
    """
    Problem: keep the running (partial) aggregates instead of one final value.
    Why: accumulate is to reduce as cumsum is to sum -- it returns an array of
    the same size holding every intermediate result.
    """
    print("== ufunc accumulate ==")

    arr = np.arange(15).reshape((3, 5))
    # Running sum across each row (axis=1).
    print(np.add.accumulate(arr, axis=1))


def explain_outer() -> None:
    """
    Problem: apply a binary operation to every pair of elements from two arrays.
    Why: outer forms a "cross product"; the result shape is the concatenation of
    the two input shapes (x.shape + y.shape).
    """
    print("== ufunc outer ==")

    arr = np.arange(3).repeat([1, 2, 2])
    print(arr)  # [0 1 1 2 2]
    # Every element of arr times every element of np.arange(5).
    print(np.multiply.outer(arr, np.arange(5)))

    # The output dimension is the concatenation of the input dimensions.
    rng = np.random.default_rng(seed=12345)
    x = rng.standard_normal((3, 4))
    y = rng.standard_normal(5)
    result = np.subtract.outer(x, y)
    print(result.shape)  # (3, 4, 5)


def explain_reduceat() -> None:
    """
    Problem: reduce contiguous slices of an array independently -- an array-level
    "group by".
    Why: reduceat takes a sequence of bin edges and reduces each slice between
    consecutive edges (and from the last edge to the end).
    """
    print("== ufunc reduceat ==")

    arr = np.arange(10)
    # Bins [0, 5, 8] -> reduce arr[0:5], arr[5:8], arr[8:].
    print(np.add.reduceat(arr, [0, 5, 8]))  # [10 18 17]

    # reduceat also accepts an axis for multidimensional arrays.
    arr = np.multiply.outer(np.arange(4), np.arange(5))
    print(arr)
    print(np.add.reduceat(arr, [0, 2, 4], axis=1))


def explain_writing_ufuncs() -> None:
    """
    Problem: turn an arbitrary Python function into something that works on whole
    arrays element by element.
    Why: np.frompyfunc and np.vectorize wrap a scalar Python function. They are
    convenient but SLOW (a Python call per element), far slower than C-based
    ufuncs -- use a real vectorized expression when one exists.
    """
    print("== Writing new ufuncs in Python ==")

    def add_elements(x: float, y: float) -> float:
        return x + y

    # frompyfunc(func, n_in, n_out) returns object-dtype results, which can be
    # inconvenient. The stubs type the call loosely, so wrap the result with
    # np.asarray to recover a typed ndarray, then narrow it with astype.
    add_them = np.frompyfunc(add_elements, 2, 1)
    result_obj: NDArray[np.object_] = np.asarray(add_them(np.arange(8), np.arange(8)))
    print(result_obj)              # dtype=object
    print(result_obj.astype(np.float64))

    # vectorize is slightly less general but lets you declare the output type.
    add_them_v = np.vectorize(add_elements, otypes=[np.float64])
    result: NDArray[np.float64] = add_them_v(np.arange(8), np.arange(8))
    print(result)  # float64 array

    # Both are much slower than the native vectorized form (np.add / "+"), which
    # should always be preferred when it exists.
    print(np.add(np.arange(8), np.arange(8)))


def main() -> None:
    explain_reduce()
    explain_accumulate()
    explain_outer()
    explain_reduceat()
    explain_writing_ufuncs()


main()
