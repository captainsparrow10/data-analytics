"""
Array-Oriented Programming with Arrays (Section 4.4)

Using NumPy arrays lets you express many data-processing tasks as concise array
expressions that would otherwise need explicit loops. Replacing loops with array
expressions is called *vectorization*, and it is usually far faster than the pure
Python equivalent. This file covers the array-oriented toolkit:

  * Conditional logic with np.where (a vectorized ternary expression).
  * Mathematical and statistical methods (sum, mean, std, cumsum, ...).
  * Methods for Boolean arrays (counting, any, all).
  * Sorting (in place and copying).
  * Unique values and other set logic.

BASIC ARRAY STATISTICAL METHODS
sum            Sum of all elements, or along an axis (empty arrays sum to 0)
mean           Arithmetic mean (NaN on zero-length arrays)
std, var       Standard deviation and variance
min, max       Minimum and maximum
argmin, argmax Indices of the minimum and maximum elements
cumsum         Cumulative sum, starting from 0
cumprod        Cumulative product, starting from 1

ARRAY SET OPERATIONS
unique(x)          Sorted unique elements of x
intersect1d(x, y)  Sorted common elements of x and y
union1d(x, y)      Sorted union of elements
isin(x, y)         Boolean array: which elements of x are contained in y (NumPy < 2.0: in1d)
setdiff1d(x, y)    Set difference: elements in x that are not in y
setxor1d(x, y)     Symmetric difference: elements in either array but not both

Run:
    python3 cap_04_numpy/5-array-oriented.py
"""

import numpy as np


def explain_where() -> None:
    """
    Problem: choose values from one array or another based on a condition.
    Why: np.where(cond, x, y) is the vectorized form of `x if cond else y`. Its
    x and y can be arrays or scalars, so it is ideal for conditional replacement.
    """
    print("== Conditional logic with np.where ==")

    xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
    yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
    cond = np.array([True, False, True, True, False])
    # Take from xarr where cond is True, otherwise from yarr.
    print(np.where(cond, xarr, yarr))  # [1.1 2.2 1.3 1.4 2.5]

    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal((4, 4))
    print(arr)
    # The second/third arguments may be scalars: replace positives with 2,
    # negatives with -2.
    print(np.where(arr > 0, 2, -2))
    # Mix scalars and arrays: replace only the positives with 2, keep the rest.
    print(np.where(arr > 0, 2, arr))


def explain_math_and_stats() -> None:
    """
    Problem: compute aggregate statistics over an array or along an axis.
    Why: reductions like sum/mean/std summarize data; the axis argument controls
    the direction, and cumsum/cumprod produce running (non-reducing) results.
    """
    print("== Mathematical and statistical methods ==")

    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal((5, 4))
    print(arr.mean())      # mean of every element
    print(np.mean(arr))    # equivalent top-level function form
    print(arr.sum())

    # The axis argument reduces along one dimension, removing it from the result.
    print(arr.mean(axis=1))  # mean ACROSS the columns -> one value per row
    print(arr.sum(axis=0))   # sum DOWN the rows -> one value per column

    # cumsum/cumprod accumulate instead of reducing (same length output).
    arr = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    print(arr.cumsum())      # [ 0  1  3  6 10 15 21 28]

    arr = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    print(arr.cumsum(axis=0))  # cumulative sum down the rows
    print(arr.cumsum(axis=1))  # cumulative sum across the columns


def explain_boolean_array_methods() -> None:
    """
    Problem: count matches and test conditions over Boolean arrays.
    Why: True/False coerce to 1/0, so sum() counts True values; any() tests
    "at least one True" and all() tests "every value True".
    """
    print("== Methods for Boolean arrays ==")

    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal(100)
    # Parentheses are required so sum() is called on the Boolean result.
    print((arr > 0).sum())   # number of positive values
    print((arr <= 0).sum())  # number of non-positive values

    bools = np.array([False, False, True, False])
    print(bools.any())  # True  -> at least one True
    print(bools.all())  # False -> not every value is True


def explain_sorting() -> None:
    """
    Problem: order the values in an array.
    Why: the `sort` METHOD sorts in place; the top-level np.sort returns a sorted
    COPY. In multidimensional arrays, pass an axis to sort along it.
    """
    print("== Sorting ==")

    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal(6)
    arr.sort()            # in-place sort, ascending
    print(arr)

    arr = rng.standard_normal((5, 3))
    arr.sort(axis=0)      # sort within each column
    print(arr)
    arr.sort(axis=1)      # sort across each row
    print(arr)

    arr2 = np.array([5, -10, 7, 1, 0, -3])
    print(np.sort(arr2))  # returns a sorted copy; arr2 is unchanged
    print(arr2)


def explain_unique_and_set_logic() -> None:
    """
    Problem: find unique values and test membership.
    Why: np.unique returns the sorted unique elements (faster than sorted(set()))
    and np.isin reports, for each element of one array, whether it is in another.
    """
    print("== Unique and other set logic ==")

    names = np.array(["Bob", "Will", "Joe", "Bob", "Will", "Joe", "Joe"])
    print(np.unique(names))        # ['Bob' 'Joe' 'Will']

    ints = np.array([3, 3, 3, 2, 2, 1, 1, 4, 4])
    print(np.unique(ints))         # [1 2 3 4]

    # np.isin tests membership of each value of the first array in the second.
    # (In NumPy < 2.0 this function was named np.in1d.)
    values = np.array([6, 0, 0, 3, 2, 5, 6])
    print(np.isin(values, [2, 3, 6]))


def main() -> None:
    explain_where()
    explain_math_and_stats()
    explain_boolean_array_methods()
    explain_sorting()
    explain_unique_and_set_logic()


main()
