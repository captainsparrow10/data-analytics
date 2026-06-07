"""
Indexing, Slicing, and Transposing (Section 4.1, continued)

NumPy array indexing is a rich topic: there are many ways to select a subset of
your data or individual elements. This file covers the four building blocks:

  * Basic indexing and slicing — like Python lists, but slices are VIEWS
    (they share memory with the original array; mutating a slice mutates the source).
  * Boolean indexing — select rows/elements using a Boolean mask.
  * Fancy indexing — select rows/elements using integer arrays.
  * Transposing and swapping axes — reorient an array without copying data.

A key distinction from Python lists: basic slices return *views*, not copies.
Boolean and fancy indexing, by contrast, always *copy* the selected data.

Run:
    python3 cap_02_numpy/2-indexing-slicing.py
"""

import numpy as np


def explain_basic_indexing_and_slicing() -> None:
    """
    Problem: select elements and ranges from 1D and multidimensional arrays.
    Why: 1D arrays behave like Python lists; in 2D+ arrays each top-level index
    returns a lower-dimensional array, and slices keep the same dimensionality.
    """
    print("== Basic indexing and slicing ==")

    arr = np.arange(10)
    print(arr[5])     # a single element -> 5
    print(arr[5:8])   # a slice -> [5 6 7]

    # Assigning a scalar to a slice broadcasts it across the whole selection.
    arr[5:8] = 12
    print(arr)        # [ 0  1  2  3  4 12 12 12  8  9]

    # IMPORTANT: a slice is a VIEW onto the original data, not a copy.
    arr_slice = arr[5:8]
    arr_slice[1] = 12345
    print(arr)        # the change is reflected in the source array
    arr_slice[:] = 64  # the bare slice [:] assigns to every element of the view
    print(arr)
    # To get an independent copy instead of a view, use arr[5:8].copy().

    # In a 2D array, a single index selects a whole row (a 1D array).
    arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(arr2d[2])       # [7 8 9]
    # These two forms are equivalent ways to reach a single element.
    print(arr2d[0][2])    # 3
    print(arr2d[0, 2])    # 3 (axis 0 = rows, axis 1 = columns)

    # Omitting later indices returns a lower-dimensional view.
    arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
    print(arr3d[0])       # a 2x3 array
    print(arr3d[1, 0])    # [7 8 9]

    # Slicing a 2D array slices along axis 0 first ("the first two rows").
    print(arr2d[:2])
    # Multiple slices select a rectangular block.
    print(arr2d[:2, 1:])
    # Mixing an integer index with a slice yields a lower-dimensional result.
    lower_dim_slice = arr2d[1, :2]
    print(lower_dim_slice.shape)  # (2,)
    # A lone colon means "the whole axis", so you can slice only later axes.
    print(arr2d[:, :1])


def explain_boolean_indexing() -> None:
    """
    Problem: select rows/elements that satisfy a condition.
    Why: comparing an array produces a Boolean mask; indexing with that mask
    keeps only the True positions. Masks can combine with & (and) and | (or).
    """
    print("== Boolean indexing ==")

    names = np.array(["Bob", "Joe", "Will", "Bob", "Will", "Joe", "Joe"])
    data = np.array([[4, 7], [0, 2], [-5, 6], [0, 0], [1, 2], [-12, -4], [3, 4]])

    # Comparing names to a string yields a Boolean array, one flag per element.
    print(names == "Bob")        # [ True False False  True False False False]

    # The mask must match the length of the axis it indexes. Here it picks rows.
    print(data[names == "Bob"])  # rows 0 and 3

    # You can index rows with a mask AND slice columns at the same time.
    print(data[names == "Bob", 1:])

    # Negate a condition with != or with ~ (useful for a mask stored in a name).
    print(data[~(names == "Bob")])
    cond = names == "Bob"
    print(data[~cond])

    # Combine multiple conditions with & (and) / | (or).
    # NOTE: the Python keywords `and`/`or` do NOT work on Boolean arrays.
    mask = (names == "Bob") | (names == "Will")
    print(data[mask])

    # Setting values through a Boolean mask assigns into the True positions.
    data[data < 0] = 0          # clamp all negatives to 0
    print(data)
    data[names != "Joe"] = 7    # set whole rows via a 1D mask
    print(data)


def explain_fancy_indexing() -> None:
    """
    Problem: select rows/elements in an arbitrary order using integer arrays.
    Why: passing a list of integers picks exactly those rows (in that order);
    passing multiple integer arrays picks the elements at each (row, col) pair.
    Unlike slicing, fancy indexing always copies the data into a new array.
    """
    print("== Fancy indexing ==")

    arr = np.zeros((8, 4))
    for i in range(8):
        arr[i] = i
    # Pass a list of integers to select rows in a chosen order.
    print(arr[[4, 3, 0, 6]])
    # Negative indices count from the end.
    print(arr[[-3, -5, -7]])

    arr = np.arange(32).reshape((8, 4))
    # Passing MULTIPLE index arrays selects one element per (row, col) pair:
    # here the elements at (1,0), (5,3), (7,1), (2,2) -> a 1D array.
    print(arr[[1, 5, 7, 2], [0, 3, 1, 2]])  # [ 4 23 29 10]
    # To select the rectangular region of those rows and columns, index twice.
    print(arr[[1, 5, 7, 2]][:, [0, 3, 1, 2]])

    # Assigning with fancy indexing modifies the selected elements in place.
    arr[[1, 5, 7, 2], [0, 3, 1, 2]] = 0
    print(arr)


def explain_transposing_and_swapping_axes() -> None:
    """
    Problem: reorient an array (e.g., turn rows into columns).
    Why: transposing is a special form of reshaping that returns a VIEW. It is
    common in matrix math, such as computing X.T @ X.
    """
    print("== Transposing arrays and swapping axes ==")

    arr = np.arange(15).reshape((3, 5))
    print(arr.T)  # the .T attribute transposes (rows <-> columns)

    # A typical use: the inner matrix product np.dot(arr.T, arr) (== arr.T @ arr).
    arr = np.array([[0, 1, 0], [1, 2, -2], [6, 3, 2], [-1, 0, -1], [1, 0, 1]])
    print(np.dot(arr.T, arr))
    print(arr.T @ arr)  # the @ operator is another way to do matrix multiplication

    # swapaxes returns a view with the two named axes interchanged.
    print(arr.swapaxes(0, 1))


def main() -> None:
    explain_basic_indexing_and_slicing()
    explain_boolean_indexing()
    explain_fancy_indexing()
    explain_transposing_and_swapping_axes()


main()
