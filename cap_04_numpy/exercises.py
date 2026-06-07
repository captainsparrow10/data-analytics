"""
NumPy: Practice Exercises

A hands-on practice set for NumPy fundamentals, progressing from basic array
creation to intermediate array-oriented programming. Each exercise states a
clear problem in its docstring and shows an original, self-contained, and
deterministic solution. Topics covered include array creation, dtypes and
astype, shape manipulation, indexing and slicing, boolean masking, fancy
indexing, broadcasting, axis-aware aggregations, np.where, sorting, np.unique,
a small linear-algebra task, and reproducible random data.

Run:
    poetry run python cap_04_numpy/exercises.py
"""

import numpy as np
from numpy.typing import NDArray


def exercise_01() -> None:
    """
    Exercise 1: Build arrays with the creation helpers.

    Problem: Using arange, linspace, zeros, full, and eye, build:
      - a vector of the even numbers from 0 up to (but not including) 10,
      - 5 equally spaced points from 0.0 to 1.0 inclusive,
      - a length-4 vector of zeros,
      - a length-3 vector filled with the value 7,
      - a 3x3 identity matrix.

    Expected result:
      evens     -> [0 2 4 6 8]
      spaced    -> [0.   0.25 0.5  0.75 1.  ]
      zeros     -> [0. 0. 0. 0.]
      sevens    -> [7 7 7]
      identity  -> 3x3 matrix with 1.0 on the diagonal, 0.0 elsewhere
    """
    evens: NDArray[np.int64] = np.arange(0, 10, 2, dtype=np.int64)
    spaced: NDArray[np.float64] = np.linspace(0.0, 1.0, 5, dtype=np.float64)
    zeros: NDArray[np.float64] = np.zeros(4, dtype=np.float64)
    sevens: NDArray[np.int64] = np.full(3, 7, dtype=np.int64)
    identity: NDArray[np.float64] = np.eye(3, dtype=np.float64)

    print("evens:", evens)
    print("spaced:", spaced)
    print("zeros:", zeros)
    print("sevens:", sevens)
    print("identity:\n", identity)


def exercise_02() -> None:
    """
    Exercise 2: Inspect and convert dtypes with astype.

    Problem: Start from a float array of measurements. Report its dtype, then
    create a truncated integer copy with astype, and report the new dtype.
    Note that astype toward int truncates toward zero (it does not round).

    Given input: [1.9, 2.1, 3.5, 4.99]
    Expected result:
      original dtype -> float64
      as integers    -> [1 2 3 4]
      integer dtype  -> int64
    """
    measurements: NDArray[np.float64] = np.array(
        [1.9, 2.1, 3.5, 4.99], dtype=np.float64
    )
    as_ints: NDArray[np.int64] = measurements.astype(np.int64)  # truncates

    print("original dtype:", measurements.dtype)
    print("as integers:", as_ints)
    print("integer dtype:", as_ints.dtype)


def exercise_03() -> None:
    """
    Exercise 3: Reshape and flatten.

    Problem: Take the integers 1..12, reshape them into a 3x4 matrix, then flatten
    the matrix back into a 1-D view with ravel. Report shapes along the way.

    Expected result:
      vector shape -> (12,)
      matrix shape -> (3, 4)
      raveled      -> [ 1  2  3  4  5  6  7  8  9 10 11 12]
    """
    vector: NDArray[np.int64] = np.arange(1, 13, dtype=np.int64)
    matrix: NDArray[np.int64] = vector.reshape(3, 4)  # 3 rows, 4 cols
    raveled: NDArray[np.int64] = matrix.ravel()  # flatten back to 1-D

    print("vector shape:", vector.shape)
    print("matrix shape:", matrix.shape)
    print("matrix:\n", matrix)
    print("raveled:", raveled)


def exercise_04() -> None:
    """
    Exercise 4: Use -1 to infer a dimension in reshape.

    Problem: Reshape the integers 0..11 into a matrix with exactly 2 columns,
    letting NumPy infer the number of rows by passing -1.

    Expected result:
      shape -> (6, 2)
      a 6x2 matrix with rows [0 1], [2 3], ..., [10 11]
    """
    data: NDArray[np.int64] = np.arange(12, dtype=np.int64)
    reshaped: NDArray[np.int64] = data.reshape(-1, 2)  # rows inferred -> 6

    print("shape:", reshaped.shape)
    print("reshaped:\n", reshaped)


def exercise_05() -> None:
    """
    Exercise 5: Basic indexing and slicing on a 1-D array.

    Problem: From the tens 10..100, extract the first element, the last element,
    a slice of the middle (indices 3..6), and every second element.

    Given input: [ 10  20  30  40  50  60  70  80  90 100]
    Expected result:
      first    -> 10
      last     -> 100
      middle   -> [40 50 60 70]
      every 2  -> [ 10  30  50  70  90]
    """
    tens: NDArray[np.int64] = np.arange(10, 101, 10, dtype=np.int64)

    print("first:", tens[0])
    print("last:", tens[-1])
    print("middle:", tens[3:7])  # indices 3,4,5,6
    print("every 2:", tens[::2])  # step of two


def exercise_06() -> None:
    """
    Exercise 6: Index and slice a 2-D array.

    Problem: Given a 3x4 matrix of 1..12, extract a single element (row 1, col 2),
    an entire row (row 0), an entire column (column 3), and a 2x2 sub-block from
    the bottom-right corner.

    Expected result:
      element    -> 7
      first row  -> [1 2 3 4]
      last col   -> [ 4  8 12]
      sub-block  -> [[ 7  8]
                     [11 12]]
    """
    matrix: NDArray[np.int64] = np.arange(1, 13, dtype=np.int64).reshape(3, 4)

    print("element [1,2]:", matrix[1, 2])
    print("first row:", matrix[0])
    print("last col:", matrix[:, 3])
    print("sub-block:\n", matrix[1:, 2:])  # rows 1..2, cols 2..3


def exercise_07() -> None:
    """
    Exercise 7: Boolean masking to filter values.

    Problem: From a vector of integers, build a boolean mask selecting values
    greater than 25, then use it to keep only those values. Also count how many
    pass the test.

    Given input: [12 40 7 33 25 60 18]
    Expected result:
      mask    -> [False  True False  True False  True False]
      kept    -> [40 33 60]
      count   -> 3
    """
    values: NDArray[np.int64] = np.array(
        [12, 40, 7, 33, 25, 60, 18], dtype=np.int64
    )
    mask: NDArray[np.bool_] = values > 25  # element-wise comparison
    kept: NDArray[np.int64] = values[mask]  # select where True

    print("mask:", mask)
    print("kept:", kept)
    print("count:", int(mask.sum()))


def exercise_08() -> None:
    """
    Exercise 8: Conditional in-place assignment via masking.

    Problem: Given a vector that mixes positive and negative numbers, clamp all
    negative values to 0 using boolean-mask assignment (a "rectify" operation).

    Given input: [ 3 -5  8 -1  0 -9  4]
    Expected result: [3 0 8 0 0 0 4]
    """
    data: NDArray[np.int64] = np.array(
        [3, -5, 8, -1, 0, -9, 4], dtype=np.int64
    )
    data[data < 0] = 0  # write 0 wherever the mask is True

    print("rectified:", data)


def exercise_09() -> None:
    """
    Exercise 9: Fancy indexing with an array of positions.

    Problem: Given a vector of labels-as-numbers, select elements at the explicit
    positions [0, 2, 4] in that order, and then select them in a custom order
    [4, 4, 0] (note repetition is allowed).

    Given input: [100 200 300 400 500]
    Expected result:
      picked      -> [100 300 500]
      reordered   -> [500 500 100]
    """
    data: NDArray[np.int64] = np.array(
        [100, 200, 300, 400, 500], dtype=np.int64
    )
    positions: NDArray[np.int64] = np.array([0, 2, 4], dtype=np.int64)
    custom: NDArray[np.int64] = np.array([4, 4, 0], dtype=np.int64)

    print("picked:", data[positions])
    print("reordered:", data[custom])


def exercise_10() -> None:
    """
    Exercise 10: Fancy indexing rows of a matrix.

    Problem: Given a 4x3 matrix, select rows 2 and 0 (in that order) to produce a
    new 2x3 matrix.

    Expected result:
      a 2x3 matrix whose first row is the original row 2 ([6 7 8])
      and whose second row is the original row 0 ([0 1 2])
    """
    matrix: NDArray[np.int64] = np.arange(12, dtype=np.int64).reshape(4, 3)
    selected: NDArray[np.int64] = matrix[np.array([2, 0], dtype=np.int64)]

    print("matrix:\n", matrix)
    print("selected rows [2, 0]:\n", selected)


def exercise_11() -> None:
    """
    Exercise 11: Element-wise arithmetic and a vectorized formula.

    Problem: Given parallel vectors of prices and quantities, compute the line
    total for each item (price * quantity) without a Python loop, then the grand
    total.

    Given input:
      prices     = [2.5 1.0 4.0]
      quantities = [4   10  2  ]
    Expected result:
      line totals -> [10. 10.  8.]
      grand total -> 28.0
    """
    prices: NDArray[np.float64] = np.array([2.5, 1.0, 4.0], dtype=np.float64)
    quantities: NDArray[np.int64] = np.array([4, 10, 2], dtype=np.int64)
    line_totals: NDArray[np.float64] = prices * quantities  # element-wise

    print("line totals:", line_totals)
    print("grand total:", float(line_totals.sum()))


def exercise_12() -> None:
    """
    Exercise 12: Broadcasting a row vector across a matrix.

    Problem: Given a 3x3 matrix of ones and a row vector [10, 20, 30], add the
    row vector to every row of the matrix using broadcasting (no loop).

    Expected result:
      a 3x3 matrix where every row is [11. 21. 31.]
    """
    matrix: NDArray[np.float64] = np.ones((3, 3), dtype=np.float64)
    row: NDArray[np.float64] = np.array([10.0, 20.0, 30.0], dtype=np.float64)
    result: NDArray[np.float64] = matrix + row  # row broadcast over each row

    print("result:\n", result)


def exercise_13() -> None:
    """
    Exercise 13: Axis-aware aggregations on a matrix.

    Problem: Given a 3x4 matrix of 1..12, compute the overall sum, the sum down
    each column (axis 0), the mean across each row (axis 1), and the population
    standard deviation of all elements.

    Expected result:
      total      -> 78
      col sums   -> [15 18 21 24]
      row means  -> [ 2.5  6.5 10.5]
      std (all)  -> ~3.452
    """
    matrix: NDArray[np.int64] = np.arange(1, 13, dtype=np.int64).reshape(3, 4)

    print("total:", int(matrix.sum()))
    print("col sums:", matrix.sum(axis=0))  # collapse rows
    print("row means:", matrix.mean(axis=1))  # collapse cols
    print("std (all):", round(float(matrix.std()), 3))


def exercise_14() -> None:
    """
    Exercise 14: Locate extremes with min, max, and argmax.

    Problem: Given a vector of scores, report the minimum, the maximum, and the
    index of the maximum (argmax). This pattern is how you find "which item won".

    Given input: [42 17 88 63 88 5]
    Expected result:
      min    -> 5
      max    -> 88
      argmax -> 2  (the FIRST position holding the maximum)
    """
    scores: NDArray[np.int64] = np.array(
        [42, 17, 88, 63, 88, 5], dtype=np.int64
    )

    print("min:", int(scores.min()))
    print("max:", int(scores.max()))
    print("argmax:", int(scores.argmax()))  # first occurrence wins


def exercise_15() -> None:
    """
    Exercise 15: Select values conditionally with np.where.

    Problem: Given a vector of temperatures in Celsius, build a parallel array of
    labels: "warm" where the temperature is at least 20, otherwise "cold". Then,
    in a second pass, use np.where to replace sub-zero readings with 0 while
    leaving the rest untouched.

    Given input: [ -3  15  22  19  30  -8]
    Expected result:
      labels  -> ['cold' 'cold' 'warm' 'cold' 'warm' 'cold']
      clamped -> [ 0 15 22 19 30  0]
    """
    temps: NDArray[np.int64] = np.array(
        [-3, 15, 22, 19, 30, -8], dtype=np.int64
    )
    labels: NDArray[np.str_] = np.where(temps >= 20, "warm", "cold")
    clamped: NDArray[np.int64] = np.where(temps < 0, 0, temps)

    print("labels:", labels)
    print("clamped:", clamped)


def exercise_16() -> None:
    """
    Exercise 16: Sort values and find unique entries.

    Problem: Given a vector with duplicates, produce a sorted copy (leaving the
    original untouched), then the sorted unique values via np.unique.

    Given input: [4 1 7 1 4 9 7 4]
    Expected result:
      sorted -> [1 1 4 4 4 7 7 9]
      unique -> [1 4 7 9]
    """
    data: NDArray[np.int64] = np.array(
        [4, 1, 7, 1, 4, 9, 7, 4], dtype=np.int64
    )
    ordered: NDArray[np.int64] = np.sort(data)  # returns a new sorted array
    unique: NDArray[np.int64] = np.unique(data)  # sorted distinct values

    print("sorted:", ordered)
    print("unique:", unique)


def exercise_17() -> None:
    """
    Exercise 17: Count occurrences with np.unique(return_counts=True).

    Problem: Given a vector of categorical codes, report each distinct code
    alongside how many times it appears.

    Given input: [2 2 3 1 3 3 1 2]
    Expected result:
      values -> [1 2 3]
      counts -> [2 3 3]
    """
    codes: NDArray[np.int64] = np.array(
        [2, 2, 3, 1, 3, 3, 1, 2], dtype=np.int64
    )
    values, counts = np.unique(codes, return_counts=True)

    print("values:", values)
    print("counts:", counts)


def exercise_18() -> None:
    """
    Exercise 18: A small linear-algebra task with dot and @.

    Problem: Given a 2x3 matrix A and a 3x2 matrix B, compute the matrix product
    A @ B (a 2x2 matrix). Separately, compute the dot product of two vectors and
    confirm np.dot agrees with the @ operator.

    Expected result:
      A @ B  -> [[ 28  31]
                 [100 112]]
      v . w  -> 32  (1*4 + 2*5 + 3*6)
      operators agree -> True
    """
    a: NDArray[np.int64] = np.arange(6, dtype=np.int64).reshape(2, 3)
    b: NDArray[np.int64] = np.arange(6, 12, dtype=np.int64).reshape(3, 2)
    product: NDArray[np.int64] = a @ b  # 2x3 @ 3x2 -> 2x2

    v: NDArray[np.int64] = np.array([1, 2, 3], dtype=np.int64)
    w: NDArray[np.int64] = np.array([4, 5, 6], dtype=np.int64)
    dot_value: int = int(np.dot(v, w))

    print("A @ B:\n", product)
    print("v . w:", dot_value)
    print("operators agree:", dot_value == int(v @ w))


def exercise_19() -> None:
    """
    Exercise 19: Verify an inverse against the identity matrix.

    Problem: Given an invertible 2x2 matrix M, compute its inverse with
    numpy.linalg.inv, then verify that M @ M_inv equals the 2x2 identity. Because
    floating-point math is inexact, use np.allclose (not ==) for the check.

    Given input: M = [[4. 7.]
                      [2. 6.]]
    Expected result:
      product is identity (within tolerance) -> True
    """
    m: NDArray[np.float64] = np.array(
        [[4.0, 7.0], [2.0, 6.0]], dtype=np.float64
    )
    # inv returns a generic float array; pin it back to float64 explicitly
    m_inv: NDArray[np.float64] = np.linalg.inv(m).astype(np.float64)
    product: NDArray[np.float64] = m @ m_inv
    identity: NDArray[np.float64] = np.eye(2, dtype=np.float64)

    print("M @ inv(M):\n", np.round(product, 6))
    print("is identity:", bool(np.allclose(product, identity)))


def exercise_20() -> None:
    """
    Exercise 20: Reproducible random data with default_rng.

    Problem: Create a seeded generator (seed=42) and draw a 2x3 matrix of
    integers in [0, 100). Because the seed is fixed, the output is deterministic
    and identical on every run. Then report the column means.

    Expected result (deterministic for seed=42):
      samples    -> [[ 8 77 65]
                     [43 43 85]]
      col means  -> [25.5 60.  75. ]
    """
    rng: np.random.Generator = np.random.default_rng(seed=42)
    samples: NDArray[np.int64] = rng.integers(0, 100, size=(2, 3))
    # mean of an int array yields float; keep dtype explicit with astype
    col_means: NDArray[np.float64] = samples.mean(axis=0).astype(np.float64)

    print("samples:\n", samples)
    print("col means:", col_means)


def main() -> None:
    print("=== Exercise 1: Array creation helpers ===")
    exercise_01()

    print("\n=== Exercise 2: dtype and astype ===")
    exercise_02()

    print("\n=== Exercise 3: Reshape and ravel ===")
    exercise_03()

    print("\n=== Exercise 4: Inferring a dimension with -1 ===")
    exercise_04()

    print("\n=== Exercise 5: 1-D indexing and slicing ===")
    exercise_05()

    print("\n=== Exercise 6: 2-D indexing and slicing ===")
    exercise_06()

    print("\n=== Exercise 7: Boolean masking ===")
    exercise_07()

    print("\n=== Exercise 8: Conditional assignment via masking ===")
    exercise_08()

    print("\n=== Exercise 9: Fancy indexing by position ===")
    exercise_09()

    print("\n=== Exercise 10: Fancy indexing matrix rows ===")
    exercise_10()

    print("\n=== Exercise 11: Element-wise arithmetic ===")
    exercise_11()

    print("\n=== Exercise 12: Broadcasting a row vector ===")
    exercise_12()

    print("\n=== Exercise 13: Axis-aware aggregations ===")
    exercise_13()

    print("\n=== Exercise 14: min, max, and argmax ===")
    exercise_14()

    print("\n=== Exercise 15: np.where ===")
    exercise_15()

    print("\n=== Exercise 16: Sorting and np.unique ===")
    exercise_16()

    print("\n=== Exercise 17: Counting with np.unique ===")
    exercise_17()

    print("\n=== Exercise 18: dot and @ ===")
    exercise_18()

    print("\n=== Exercise 19: Inverse vs. identity ===")
    exercise_19()

    print("\n=== Exercise 20: Reproducible random data ===")
    exercise_20()


main()
