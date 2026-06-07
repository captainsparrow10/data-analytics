"""
More About Sorting (Appendix A.6)

Like Python's built-in list, the ndarray `sort` method is an IN-PLACE sort that
rearranges the array's contents without producing a new array; np.sort instead
returns a sorted COPY. This file covers the rest of NumPy's sorting toolkit:

  * In-place versus copy sorts (and sorting along an axis).
  * Indirect sorts: argsort and lexsort (sort by one or more keys).
  * Alternative sort algorithms (kind="mergesort" for stability).
  * Partially sorting arrays (np.partition, np.argpartition).
  * np.searchsorted: finding insertion points in a sorted array.

ARRAY SORTING METHODS (relative speed; lower is faster)
KIND         SPEED  STABLE  WORK SPACE  WORST CASE
quicksort    1      No      0           O(n^2)
mergesort    2      Yes     n / 2       O(n log n)
heapsort     3      No      0           O(n log n)

Run:
    poetry run python cap_a_advanced-numpy/6-sorting.py
"""

import numpy as np


def explain_inplace_vs_copy() -> None:
    """
    Problem: order an array, choosing whether to mutate it or get a sorted copy.
    Why: the `sort` METHOD sorts in place (and mutates the underlying data even
    through a view); np.sort returns a new sorted array. Both take an axis.
    """
    print("== In-place versus copy sorts ==")

    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal(6)
    arr.sort()  # in-place, ascending
    print(arr)

    # Sorting a VIEW mutates the original array's underlying data.
    arr = rng.standard_normal((3, 5))
    arr[:, 0].sort()  # sort just the first column, in place
    print(arr)

    # np.sort returns a sorted COPY; the input is unchanged.
    arr = rng.standard_normal(5)
    print(np.sort(arr))
    print(arr)

    # All sort methods take an axis to sort each section independently.
    arr = rng.standard_normal((3, 5))
    arr.sort(axis=1)  # sort within each row
    print(arr)

    # There is no "descending" flag; slice the sorted result in reverse (a view).
    print(arr[:, ::-1])


def explain_indirect_sorts() -> None:
    """
    Problem: reorder data by one or more KEYS without sorting the keys in place.
    Why: argsort returns the integer indices that would sort an array (an
    "indexer"); lexsort does the same for multiple keys, ordered by the LAST key
    passed first.
    """
    print("== Indirect sorts: argsort and lexsort ==")

    values = np.array([5, 0, 1, 3, 2])
    indexer = values.argsort()
    print(indexer)            # [1 2 4 3 0]
    print(values[indexer])    # [0 1 2 3 5]

    # Reorder a 2D array by its first row using that row's argsort.
    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal((3, 5))
    arr[0] = values
    print(arr[:, arr[0].argsort()])

    # lexsort sorts by multiple keys; the LAST key passed is the primary sort.
    first_name = np.array(["Bob", "Jane", "Steve", "Bill", "Barbara"])
    last_name = np.array(["Jones", "Arnold", "Arnold", "Jones", "Walters"])
    sorter = np.lexsort((first_name, last_name))  # sort by last, then first
    print(sorter)
    print(list(zip(last_name[sorter], first_name[sorter])))


def explain_stable_sort() -> None:
    """
    Problem: keep the relative order of equal elements during a sort.
    Why: a STABLE algorithm preserves the input order of ties, which matters for
    indirect sorts. mergesort is the stable option (kind="mergesort").
    """
    print("== Alternative (stable) sort algorithms ==")

    values = np.array(["2:first", "2:second", "1:first", "1:second", "1:third"])
    key = np.array([2, 2, 1, 1, 1])
    # mergesort is stable: the three "1:" items keep their original relative order.
    indexer = key.argsort(kind="mergesort")
    print(indexer)              # [2 3 4 0 1]
    print(values.take(indexer))


def explain_partition() -> None:
    """
    Problem: find the k smallest (or largest) elements without a full sort.
    Why: np.partition rearranges so the first k entries are the k smallest (in no
    particular order) -- cheaper than sorting; np.argpartition returns the
    indices that produce that arrangement.
    """
    print("== Partially sorting arrays ==")

    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal(20)
    print(arr)

    # The first 3 entries are the 3 smallest values (unordered among themselves).
    print(np.partition(arr, 3))

    # argpartition returns the indices that yield that same arrangement.
    indices = np.argpartition(arr, 3)
    print(indices)
    print(arr.take(indices))


def explain_searchsorted() -> None:
    """
    Problem: find where a value would be inserted to keep a sorted array sorted,
    and bin data into buckets.
    Why: searchsorted runs a binary search on a sorted array. With an array of
    bin edges it labels each value with the bucket it falls into.
    """
    print("== np.searchsorted: finding elements in a sorted array ==")

    arr = np.array([0, 1, 7, 12, 15])
    print(arr.searchsorted(9))            # 3 -- insertion point for 9
    print(arr.searchsorted([0, 8, 11, 16]))  # [0 3 3 5]

    # With ties, side controls left/right insertion among equal values.
    arr = np.array([0, 0, 0, 1, 1, 1, 1])
    print(arr.searchsorted([0, 1]))                 # [0 3] (left, default)
    print(arr.searchsorted([0, 1], side="right"))   # [3 7]

    # Binning: label each value with the bucket whose edges bracket it.
    rng = np.random.default_rng(seed=12345)
    data = np.floor(rng.uniform(0, 10000, size=50))
    bins = np.array([0, 100, 1000, 5000, 10000])
    labels = bins.searchsorted(data)
    print(labels)


def main() -> None:
    explain_inplace_vs_copy()
    explain_indirect_sorts()
    explain_stable_sort()
    explain_partition()
    explain_searchsorted()


main()
