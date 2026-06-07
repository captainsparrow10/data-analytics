"""
Advanced NumPy: Practice Exercises

A set of original, self-contained drills covering the advanced corners of NumPy:
the strided memory model and contiguity flags, reshaping under C vs Fortran
order, broadcasting (row/column demeaning, assigning by broadcast), the ufunc
instance methods (reduce, accumulate, outer, reduceat), wrapping Python callables
as array functions (frompyfunc, vectorize), structured and record arrays with
nested dtypes, and the full indirect-sorting and searching toolkit (argsort,
lexsort, partition, argpartition, searchsorted).

Every exercise states the PROBLEM and its expected result in the docstring, then
solves it in the body with inline comments and printed output. All data is built
in code with a seeded generator, so results are deterministic.

Run:
    poetry run python cap_a_advanced-numpy/exercises.py
"""

import numpy as np
from numpy.typing import NDArray


def exercise_01() -> None:
    """
    PROBLEM: Take a C-contiguous 4x6 int64 array and report its byte strides,
    then transpose it and report the new strides and contiguity flags.
    EXPECTED: original strides (48, 8) and C_CONTIGUOUS True; the transpose has
    strides (8, 48), is F_CONTIGUOUS True and C_CONTIGUOUS False (zero-copy view).
    """
    print("== Exercise 01: strides and contiguity of a transpose ==")

    arr = np.arange(24, dtype=np.int64).reshape((4, 6))
    # int64 is 8 bytes; a C-order row of 6 elements spans 6 * 8 = 48 bytes.
    print(arr.strides)                    # (48, 8)
    print(arr.flags["C_CONTIGUOUS"])      # True

    # Transposing only swaps shape and strides metadata -- no data is moved.
    transposed = arr.T
    print(transposed.strides)                  # (8, 48)
    print(transposed.flags["F_CONTIGUOUS"])    # True
    print(transposed.flags["C_CONTIGUOUS"])    # False


def exercise_02() -> None:
    """
    PROBLEM: Take one C-contiguous 2x6 matrix, make a Fortran-contiguous COPY of
    it with np.asfortranarray, and flatten each with ravel(order="K") to expose
    the physical memory order.
    EXPECTED: the two arrays are elementwise equal, but the K-order ravel (which
    walks memory as stored) differs: the C copy yields 0..11 in row order, while
    the F copy yields column order [0, 6, 1, 7, 2, 8, 3, 9, 4, 10, 5, 11].
    """
    print("== Exercise 02: C vs F memory layout exposed by ravel('K') ==")

    # A plain reshape only relabels shape/strides over the SAME buffer, so it
    # would not change physical order; asfortranarray makes a real F-order copy.
    arr_c: NDArray[np.int64] = np.arange(12, dtype=np.int64).reshape((2, 6))
    arr_f: NDArray[np.int64] = np.asfortranarray(arr_c)

    # ravel(order="K") reads elements in the order they physically sit in memory.
    print(arr_c.ravel(order="K"))   # [ 0  1  2  3  4  5  6  7  8  9 10 11]
    print(arr_f.ravel(order="K"))   # [ 0  6  1  7  2  8  3  9  4 10  5 11]

    # The two arrays are equal elementwise despite different memory layouts.
    print(np.array_equal(arr_c, arr_f))  # True


def exercise_03() -> None:
    """
    PROBLEM: Reshape arange(8) into a 2x4 block in C order and in F order, and
    show the resulting 2D arrays differ.
    EXPECTED: C order gives [[0 1 2 3] [4 5 6 7]]; F order gives
    [[0 2 4 6] [1 3 5 7]].
    """
    print("== Exercise 03: reshape with explicit order ==")

    flat = np.arange(8, dtype=np.int64)
    # C order: walk the last axis (columns) fastest.
    print(flat.reshape((2, 4), order="C"))
    # F order: walk the first axis (rows) fastest.
    print(flat.reshape((2, 4), order="F"))


def exercise_04() -> None:
    """
    PROBLEM: Given a 3x4 float matrix, subtract each ROW's mean from that row,
    then subtract each COLUMN's mean from that column, using broadcasting with
    np.newaxis instead of any loop.
    EXPECTED: every row of the row-demeaned matrix sums to ~0; every column of
    the column-demeaned matrix sums to ~0 (verified by near-zero max abs sums).
    """
    print("== Exercise 04: demean rows vs columns with np.newaxis ==")

    rng = np.random.default_rng(seed=7)
    matrix: NDArray[np.float64] = rng.normal(size=(3, 4))

    # Row means have shape (3,); reshape to (3, 1) so they broadcast across cols.
    row_means: NDArray[np.float64] = matrix.mean(axis=1)
    row_demeaned: NDArray[np.float64] = matrix - row_means[:, np.newaxis]
    print(np.abs(row_demeaned.sum(axis=1)).max() < 1e-12)  # True

    # Column means have shape (4,); a (1, 4) view broadcasts down the rows.
    col_means: NDArray[np.float64] = matrix.mean(axis=0)
    col_demeaned: NDArray[np.float64] = matrix - col_means[np.newaxis, :]
    print(np.abs(col_demeaned.sum(axis=0)).max() < 1e-12)  # True


def exercise_05() -> None:
    """
    PROBLEM: Start from a 4x4 zero matrix and, using broadcasting assignment
    only, set every element on or below the main diagonal to its row index + 1.
    EXPECTED: a lower-triangular matrix where row i (on/below diagonal) holds
    i + 1 -- e.g. last row is [4 4 4 4], top row is [1 0 0 0].
    """
    print("== Exercise 05: set values by broadcasting ==")

    grid: NDArray[np.int64] = np.zeros((4, 4), dtype=np.int64)
    # A boolean mask of the lower triangle (including the diagonal).
    lower_mask: NDArray[np.bool_] = np.tril(np.ones((4, 4), dtype=np.bool_))

    # Column vector of row labels broadcasts across all columns on assignment.
    row_labels: NDArray[np.int64] = np.arange(1, 5, dtype=np.int64)[:, np.newaxis]
    # np.where selects the broadcast label where the mask is True, else the zero.
    grid = np.where(lower_mask, row_labels, grid)
    print(grid)


def exercise_06() -> None:
    """
    PROBLEM: Use ufunc reduce and accumulate on arange(1, 6) to get the product
    and the running product.
    EXPECTED: np.multiply.reduce gives 120; np.multiply.accumulate gives
    [1 2 6 24 120].
    """
    print("== Exercise 06: ufunc reduce and accumulate ==")

    arr = np.arange(1, 6, dtype=np.int64)
    # reduce collapses the array to a single value via repeated multiplication.
    print(np.multiply.reduce(arr))      # 120 -- this is 5!
    # accumulate keeps every partial product (a running factorial here).
    print(np.multiply.accumulate(arr))  # [  1   2   6  24 120]


def exercise_07() -> None:
    """
    PROBLEM: Build a 3x3 multiplication table with np.multiply.outer over
    [1, 2, 3], then collapse a 9-element array into 3 group sums for the index
    edges [0, 4, 7] using np.add.reduceat.
    EXPECTED: outer product table [[1 2 3] [2 4 6] [3 6 9]]; reduceat groups
    arange(1, 10) into [10, 18, 17] (1..4, 5..7, 8..9).
    """
    print("== Exercise 07: ufunc outer and reduceat ==")

    factors = np.array([1, 2, 3], dtype=np.int64)
    # outer applies multiply to every pair; result shape is (3,) + (3,).
    print(np.multiply.outer(factors, factors))

    grouped = np.arange(1, 10, dtype=np.int64)
    # reduceat sums each slice [0:4], [4:7], [7:end] given the edge list.
    print(np.add.reduceat(grouped, [0, 4, 7]))  # [10 18 17]


def exercise_08() -> None:
    """
    PROBLEM: Wrap a two-argument Python function (clamped subtraction, never
    below zero) as an array function with np.frompyfunc, and wrap a one-argument
    function (integer square) with np.vectorize giving an explicit otypes.
    EXPECTED: frompyfunc on [5, 2, 9] minus [3, 4, 1] yields [2 0 8] after
    casting object output to int64; vectorize squares [1, 2, 3, 4] to [1 4 9 16].
    """
    print("== Exercise 08: frompyfunc and vectorize ==")

    def clamped_sub(left: int, right: int) -> int:
        # Plain Python scalar logic; frompyfunc will broadcast it elementwise.
        return max(left - right, 0)

    # frompyfunc(func, n_in, n_out) always returns object dtype, so we asarray it
    # as NDArray[np.object_] then cast to the concrete numeric dtype we want.
    sub_ufunc = np.frompyfunc(clamped_sub, 2, 1)
    raw: NDArray[np.object_] = np.asarray(
        sub_ufunc(np.array([5, 2, 9]), np.array([3, 4, 1]))
    )
    print(raw.astype(np.int64))  # [2 0 8]

    def square(value: int) -> int:
        return value * value

    # vectorize lets us declare otypes, so the result has a real numeric dtype.
    square_v = np.vectorize(square, otypes=[np.int64])
    squared: NDArray[np.int64] = square_v(np.array([1, 2, 3, 4]))
    print(squared)  # [ 1  4  9 16]


def exercise_09() -> None:
    """
    PROBLEM: Define a structured dtype with named fields name (string), age
    (int) and a nested 2-float "coords" field, build three records, and query
    everyone older than 30 by their coords.
    EXPECTED: three records; selecting age > 30 returns the rows for the two
    older people and their (x, y) coordinate pairs.
    """
    print("== Exercise 09: structured array with a nested field ==")

    # A nested dtype: "coords" is itself a length-2 float64 sub-array per record.
    person_dtype = np.dtype(
        [("name", "U10"), ("age", np.int64), ("coords", np.float64, (2,))]
    )
    people: NDArray[np.void] = np.array(
        [
            ("Ana", 41, (1.0, 2.0)),
            ("Beto", 29, (3.0, 4.0)),
            ("Cira", 35, (5.0, 6.0)),
        ],
        dtype=person_dtype,
    )

    # Field access by name returns a view of just that column.
    print(people["name"])  # ['Ana' 'Beto' 'Cira']

    # Boolean mask over the age field selects matching whole records.
    older: NDArray[np.void] = people[people["age"] > 30]
    print(older["name"])    # ['Ana' 'Cira']
    print(older["coords"])  # [[1. 2.] [5. 6.]]


def exercise_10() -> None:
    """
    PROBLEM: Given scores for five players, use argsort to produce the ranking
    order (highest score first) and reorder a parallel names array accordingly.
    EXPECTED: with scores [50, 90, 70, 90, 60], descending argsort puts the two
    90s first (stable order keeps the earlier index first), giving names ordered
    high-to-low.
    """
    print("== Exercise 10: argsort for indirect ranking ==")

    names = np.array(["p0", "p1", "p2", "p3", "p4"])
    scores = np.array([50, 90, 70, 90, 60], dtype=np.int64)

    # argsort returns the index permutation that sorts ascending; negating the
    # scores (with a stable kind) gives a descending, tie-stable ranking.
    order: NDArray[np.intp] = np.argsort(-scores, kind="stable")
    print(order)          # [1 3 2 4 0]
    print(names[order])   # ['p1' 'p3' 'p2' 'p4' 'p0']
    print(scores[order])  # [90 90 70 60 50]


def exercise_11() -> None:
    """
    PROBLEM: Sort records by two keys with lexsort: primary key last_name
    ascending, secondary key first_name ascending.
    EXPECTED: lexsort orders by the LAST key passed first, so passing
    (first_name, last_name) sorts by last_name then first_name, putting the two
    "Diaz" rows together ordered Ana then Cira.
    """
    print("== Exercise 11: lexsort multi-key sort ==")

    first_name = np.array(["Cira", "Ana", "Beto", "Ana"])
    last_name = np.array(["Diaz", "Diaz", "Soto", "Ruiz"])

    # The LAST array passed to lexsort is the primary sort key.
    sorter: NDArray[np.intp] = np.lexsort((first_name, last_name))
    print(sorter)               # [1 0 3 2]
    print(last_name[sorter])    # ['Diaz' 'Diaz' 'Ruiz' 'Soto']
    print(first_name[sorter])   # ['Ana' 'Cira' 'Ana' 'Beto']


def exercise_12() -> None:
    """
    PROBLEM: From a shuffled array, get the 3 smallest values (unsorted) with
    np.partition, and recover the index of the single smallest with
    np.argpartition.
    EXPECTED: partition(arr, 3)[:3] holds the three smallest values {3, 7, 12}
    in some order; argpartition(arr, 0)[0] is the index of the global minimum 3.
    """
    print("== Exercise 12: partition and argpartition for k-th smallest ==")

    arr = np.array([42, 7, 19, 3, 25, 12, 88], dtype=np.int64)
    # partition guarantees the k smallest sit in the first k slots (unordered),
    # which is cheaper than a full sort when you only need the smallest few.
    part: NDArray[np.int64] = np.partition(arr, 3)
    print(np.sort(part[:3]))  # [ 3  7 12] (sorted only for a stable printout)

    # argpartition returns indices; index 0 after partitioning at 0 is the min.
    idx: NDArray[np.intp] = np.argpartition(arr, 0)
    print(arr[idx[0]])  # 3 -- the global minimum value


def exercise_13() -> None:
    """
    PROBLEM: Use np.searchsorted to bucket measurements into labeled bins with
    edges [0, 10, 20, 30].
    EXPECTED: data [5, 10, 22, 35, 0] maps to bin labels via searchsorted with
    side="right" -> [1 2 3 4 1], so values land in the bin whose upper edge they
    fall under.
    """
    print("== Exercise 13: searchsorted for binning ==")

    bins = np.array([0, 10, 20, 30], dtype=np.int64)
    data = np.array([5, 10, 22, 35, 0], dtype=np.int64)

    # searchsorted finds each value's insertion point in the sorted bin edges;
    # side="right" sends a value equal to an edge into the higher bin.
    labels: NDArray[np.intp] = bins.searchsorted(data, side="right")
    print(labels)  # [1 2 3 4 1]


def main() -> None:
    print("##### STRIDES, FLAGS & RESHAPE ORDER #####")
    exercise_01()
    exercise_02()
    exercise_03()

    print("\n##### BROADCASTING #####")
    exercise_04()
    exercise_05()

    print("\n##### ADVANCED UFUNCS #####")
    exercise_06()
    exercise_07()
    exercise_08()

    print("\n##### STRUCTURED ARRAYS #####")
    exercise_09()

    print("\n##### SORTING & SEARCHING #####")
    exercise_10()
    exercise_11()
    exercise_12()
    exercise_13()


main()
