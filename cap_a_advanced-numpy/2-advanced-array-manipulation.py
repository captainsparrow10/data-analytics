"""
Advanced Array Manipulation (Appendix A.2)

Beyond fancy indexing, slicing, and Boolean subsetting there are many ways to
reshape, combine, and rearrange arrays. While pandas handles most heavy lifting
for data analysis, you may eventually need to write an array algorithm that no
existing library provides. This file covers:

  * Reshaping arrays (reshape, the -1 placeholder, ravel/flatten).
  * C versus FORTRAN (row-major versus column-major) order.
  * Concatenating and splitting (concatenate, vstack/hstack, split, r_/c_).
  * Repeating elements (repeat, tile).
  * Fancy-indexing equivalents (take/put, and take along an axis).

ARRAY CONCATENATION FUNCTIONS
FUNCTION           DESCRIPTION
concatenate        Most general: join a collection of arrays along one axis
vstack, row_stack  Stack arrays by rows (along axis 0)
hstack             Stack arrays by columns (along axis 1)
column_stack       Like hstack, but convert 1D arrays to 2D column vectors first
dstack             Stack arrays by "depth" (along axis 2)
split              Split an array at the passed locations along an axis
hsplit, vsplit     Convenience functions for splitting on axis 0 and 1

Run:
    poetry run python cap_a_advanced-numpy/2-advanced-array-manipulation.py
"""

import numpy as np


def explain_reshaping() -> None:
    """
    Problem: convert an array from one shape to another without copying data.
    Why: reshape returns a view with new shape metadata. The -1 placeholder lets
    NumPy infer one dimension; an existing array's .shape tuple can be reused.
    """
    print("== Reshaping arrays ==")

    # Pass a tuple for the new shape. The data is shared, not copied.
    arr = np.arange(8)
    print(arr)                  # [0 1 2 3 4 5 6 7]
    print(arr.reshape((4, 2)))  # 4 rows x 2 columns

    # reshape can chain; a multidimensional array can be reshaped again.
    print(arr.reshape((4, 2)).reshape((2, 4)))

    # One dimension can be -1: its size is inferred from the total element count.
    arr = np.arange(15)
    print(arr.reshape((5, -1)))  # 5 rows; columns inferred as 3

    # Since shape is a tuple, another array's shape can be passed directly.
    other_arr = np.ones((3, 5))
    print(other_arr.shape)              # (3, 5)
    print(arr.reshape(other_arr.shape)) # reshaped to 3 x 5

    # The opposite of reshape (to 1D) is "raveling"/"flattening".
    arr = np.arange(15).reshape((5, 3))
    # ravel does NOT copy if the result was contiguous in the original.
    print(arr.ravel())
    # flatten behaves like ravel but ALWAYS returns a copy.
    print(arr.flatten())


def explain_c_vs_fortran_order() -> None:
    """
    Problem: control the order in which array data is walked when reshaping or
    raveling.
    Why: C/row-major (the default) traverses higher dimensions first; FORTRAN/
    column-major traverses them last. The order argument ('C' or 'F') selects it.
    """
    print("== C versus FORTRAN order ==")

    arr = np.arange(12).reshape((3, 4))
    print(arr)

    # 'C' (default) walks the last axis fastest -> rows read left to right.
    print(arr.ravel())       # [ 0  1  2 ... 11]
    # 'F' walks the first axis fastest -> values read down each column.
    print(arr.ravel("F"))    # [ 0  4  8  1  5  9  2  6 10  3  7 11]


def explain_concatenate_and_split() -> None:
    """
    Problem: join several arrays into one, or slice one array into several.
    Why: np.concatenate is the general tool (pick the axis); vstack/hstack are
    convenient shortcuts; np.split cuts an array at the given index positions.
    """
    print("== Concatenating and splitting arrays ==")

    arr1 = np.array([[1, 2, 3], [4, 5, 6]])
    arr2 = np.array([[7, 8, 9], [10, 11, 12]])

    # concatenate joins along the chosen axis.
    print(np.concatenate([arr1, arr2], axis=0))  # stack rows -> 4 x 3
    print(np.concatenate([arr1, arr2], axis=1))  # stack columns -> 2 x 6

    # vstack/hstack are shortcuts for the two common cases above.
    print(np.vstack((arr1, arr2)))  # same as concatenate axis=0
    print(np.hstack((arr1, arr2)))  # same as concatenate axis=1

    # split slices an array into pieces at the given index positions.
    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal((5, 2))
    first, second, third = np.split(arr, [1, 3])
    # [1, 3] means: rows [0:1], rows [1:3], rows [3:].
    print(first)
    print(second)
    print(third)


def explain_r_and_c_helpers() -> None:
    """
    Problem: stack arrays (and slice ranges) with a terse syntax.
    Why: the special objects np.r_ and np.c_ make row/column stacking concise and
    can even translate slice objects into arrays.
    """
    print("== Stacking helpers: r_ and c_ ==")

    rng = np.random.default_rng(seed=12345)
    arr = np.arange(6)
    arr1 = arr.reshape((3, 2))
    arr2 = rng.standard_normal((3, 2))

    # r_ stacks along axis 0 (rows), like vstack.
    stacked = np.r_[arr1, arr2]
    print(stacked)
    # c_ stacks along axis 1 (columns); here it appends arr as a final column.
    print(np.c_[stacked, arr])

    # c_ and r_ also translate slices directly into arrays.
    print(np.c_[1:6, -10:-5])


def explain_repeat_and_tile() -> None:
    """
    Problem: build a larger array by replicating elements or whole blocks.
    Why: repeat copies each element in place (optionally a different count per
    element, optionally along an axis); tile lays whole copies of the array side
    by side, like laying down floor tiles.
    """
    print("== Repeating elements: repeat and tile ==")

    # repeat with a scalar copies every element that many times.
    arr = np.arange(3)
    print(arr.repeat(3))  # [0 0 0 1 1 1 2 2 2]

    # An array of counts repeats each element a different number of times.
    print(arr.repeat([2, 3, 4]))  # [0 0 1 1 1 2 2 2 2]

    # For multidimensional arrays, pass an axis (otherwise the array is flattened).
    rng = np.random.default_rng(seed=12345)
    arr2 = rng.standard_normal((2, 2))
    print(arr2)
    print(arr2.repeat(2, axis=0))         # duplicate each row
    print(arr2.repeat([2, 3], axis=0))    # row 0 twice, row 1 three times
    print(arr2.repeat([2, 3], axis=1))    # col 0 twice, col 1 three times

    # tile stacks whole copies of the array. A scalar tiles row by row.
    print(np.tile(arr2, 2))       # two copies side by side
    print(np.tile(arr2, (2, 1)))  # a 2x1 tuple: stack copies vertically
    print(np.tile(arr2, (3, 2)))  # 3 rows by 2 columns of copies


def explain_take_and_put() -> None:
    """
    Problem: select or assign elements using an integer index array on a single
    axis -- the fancy-indexing operation made explicit.
    Why: take/put are the method form of fancy indexing for one axis. take also
    accepts an axis keyword; put only works on the flattened (C-order) array.
    """
    print("== Fancy indexing equivalents: take and put ==")

    arr = np.arange(10) * 100
    inds = [7, 1, 2, 6]
    # Fancy indexing and take are equivalent for a single axis.
    print(arr[inds])        # [700 100 200 600]
    print(arr.take(inds))   # [700 100 200 600]

    # put assigns into those positions IN PLACE (flattened indices only).
    arr.put(inds, 42)
    print(arr)
    arr.put(inds, [40, 41, 42, 43])  # a value per index
    print(arr)

    # take along another axis: pass axis. Here we pick columns of a 2D array.
    inds = [2, 0, 2, 1]
    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal((2, 4))
    print(arr)
    print(arr.take(inds, axis=1))  # reorder/duplicate columns
    # put has no axis argument, so use []-based indexing for other axes.


def main() -> None:
    explain_reshaping()
    explain_c_vs_fortran_order()
    explain_concatenate_and_split()
    explain_r_and_c_helpers()
    explain_repeat_and_tile()
    explain_take_and_put()


main()
