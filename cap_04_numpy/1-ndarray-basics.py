"""
The NumPy ndarray: A Multidimensional Array Object (Section 4.1)

NumPy, short for Numerical Python, is one of the most important foundational
packages for numerical computing in Python. Its core feature is the ndarray, an
N-dimensional array object: a fast, flexible container for large datasets that
lets you perform *vectorized* arithmetic on whole blocks of data using a syntax
as concise as the equivalent operation on scalars — no Python loops required.

An ndarray is a generic multidimensional container for homogeneous data: every
element must be of the same type. Each array carries a `shape` tuple (the size of
each dimension) and a `dtype` object (the data type of its elements).

This file covers creating arrays, their data types, and array arithmetic.

ARRAY-CREATION FUNCTIONS
FUNCTION      DESCRIPTION
array         Convert input data (list, tuple, array, or other sequence) to an ndarray, inferring a dtype or using an explicit one; copies the input by default
asarray       Convert input to an ndarray, but do not copy if the input is already an ndarray
arange        Like the built-in range, but returns an ndarray instead of a list
ones          Produce an array of all 1s with the given shape and dtype
ones_like     Take another array and produce a ones array of the same shape and dtype
zeros         Produce an array of all 0s with the given shape and dtype
zeros_like    Take another array and produce a zeros array of the same shape and dtype
empty         Allocate new memory for an array, but do not populate it with values
empty_like    Like empty, but takes another array to determine shape and dtype
full          Produce an array of the given shape and dtype, with all values set to a fill value
full_like     Take another array and produce a filled array of the same shape and dtype
eye, identity Create a square N x N identity matrix (1s on the diagonal, 0s elsewhere)

Run:
    python3 cap_04_numpy/1-ndarray-basics.py
"""

import numpy as np


def explain_ndarray() -> None:
    """
    Problem: show what makes an ndarray special compared to a Python list.
    Why: the ndarray enables vectorized (batch) operations — a single expression
    applies element-wise to every value, which is both concise and fast.
    """
    print("== The NumPy ndarray ==")

    # Create a 2D array from a nested list. Because the values include floats,
    # NumPy infers a floating-point dtype for the whole array.
    data = np.array([[1.5, -0.1, 3.0], [0.0, -3.0, 6.5]])
    print(data)

    # Vectorized arithmetic: every element is multiplied by 10 — no for loop.
    print(data * 10)

    # Element-wise addition of the array with itself.
    print(data + data)

    # .shape reports the size of each dimension: (2 rows, 3 columns).
    print(data.shape)

    # .dtype reports the element type that all values share (here, float64).
    print(data.dtype)


def explain_creating_ndarrays() -> None:
    """
    Problem: build arrays from existing data and from scratch.
    Why: np.array converts any sequence-like object; zeros/ones/empty/arange
    create arrays of a known shape without needing the data up front.
    """
    print("== Creating ndarrays ==")

    # The easiest way to create an array is np.array on a sequence.
    data1 = [6, 7.5, 8, 0, 1]
    arr1 = np.array(data1)
    print(arr1)

    # Nested sequences become a multidimensional array.
    data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
    arr2 = np.array(data2)
    print(arr2)
    print(arr2.ndim)   # number of dimensions -> 2
    print(arr2.shape)  # shape -> (2, 4)

    # Unless told otherwise, np.array infers a good dtype from the data.
    print(arr1.dtype)  # float64
    print(arr2.dtype)  # int64 (platform dependent)

    # zeros / ones create arrays filled with 0s or 1s of a given shape.
    print(np.zeros(10))         # 1D array of ten 0.0s
    print(np.zeros((3, 6)))     # 3x6 array of 0.0s
    print(np.ones((2, 3)))      # 2x3 array of 1.0s

    # empty allocates memory WITHOUT initializing it — values are arbitrary.
    # It is not safe to assume empty returns zeros.
    print(np.empty((2, 3, 2)).shape)  # show only the shape; contents are garbage

    # arange is the array-valued version of the built-in range.
    print(np.arange(15))  # [0 1 2 ... 14]


def explain_dtype() -> None:
    """
    Problem: understand and convert the dtype of an array.
    Why: the dtype tells NumPy how to interpret the bytes in memory. Casting with
    astype lets you change representation (e.g., int -> float, string -> number).
    """
    print("== Data types for ndarrays ==")

    # The dtype is named after a type plus its size in bits, e.g. float64.
    arr1 = np.array([1, 2, 3], dtype=np.float64)
    arr2 = np.array([1, 2, 3], dtype=np.int32)
    print(arr1.dtype)  # float64
    print(arr2.dtype)  # int32

    # astype explicitly casts an array to another dtype, always making a copy.
    arr = np.array([1, 2, 3, 4, 5])
    print(arr.dtype)               # int64
    float_arr = arr.astype(np.float64)
    print(float_arr.dtype)         # float64

    # Casting floats to an integer dtype TRUNCATES the decimal part (no rounding).
    arr = np.array([3.7, -1.2, -2.6, 0.5, 12.9, 10.1])
    print(arr.astype(np.int32))    # [ 3 -1 -2  0 12 10]

    # Strings that represent numbers can be cast to a numeric dtype.
    numeric_strings = np.array(["1.25", "-9.6", "42"], dtype=np.bytes_)
    print(numeric_strings.astype(float))  # [ 1.25 -9.6  42.  ]

    # You can also reuse another array's dtype via its .dtype attribute.
    int_array = np.arange(10)
    calibers = np.array([0.22, 0.270, 0.357, 0.380, 0.44, 0.50], dtype=np.float64)
    print(int_array.astype(calibers.dtype))  # ints become floats

    # Shorthand type-code strings work too ("u4" == uint32).
    zeros_uint32 = np.zeros(8, dtype="u4")
    print(zeros_uint32)


def explain_arithmetic() -> None:
    """
    Problem: operate on whole arrays at once.
    Why: equal-size arrays combine element-wise; scalars broadcast to every
    element; comparisons yield Boolean arrays. This is "vectorization".
    """
    print("== Arithmetic with NumPy arrays ==")

    arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    print(arr)

    # Element-wise operations between equal-size arrays.
    print(arr * arr)   # squares each element
    print(arr - arr)   # all zeros

    # Operations with a scalar propagate (broadcast) the scalar to each element.
    print(1 / arr)
    print(arr ** 2)

    # Comparisons between same-size arrays produce a Boolean array.
    arr2 = np.array([[0.0, 4.0, 1.0], [7.0, 2.0, 12.0]])
    print(arr2 > arr)


def main() -> None:
    explain_ndarray()
    explain_creating_ndarrays()
    explain_dtype()
    explain_arithmetic()


main()
