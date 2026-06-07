"""
Series: A One-Dimensional Labeled Array (Section 5.1)

A Series is a one-dimensional array-like object containing a sequence of values
(of similar types to NumPy types) of the same type and an associated array of
data labels, called its *index*. Think of it as a fixed-length, ordered
dictionary: a mapping of index values to data values. Unlike a NumPy array, a
Series carries its labels along with the data, so arithmetic, filtering, and
function application all preserve the index-value link, and operations between
two Series automatically align on the index.

This file covers creating a Series, its `array`/`index` attributes, label-based
selection and assignment, vectorized operations that preserve the index, dict
interop (`in`, building from a dict, `to_dict`), missing-data detection
(`isna`/`notna`), automatic index alignment, and the `name` attribute.

SERIES ESSENTIALS
ATTRIBUTE/METHOD   DESCRIPTION
array              The underlying values as a PandasArray (wraps a NumPy array)
index              The Index object holding the labels
isna / notna       Boolean Series flagging missing (NaN) / present values
to_dict            Convert the Series back into a plain Python dictionary
name               Optional name for the Series; index.name names the labels

Run:
    poetry run python cap_05_pandas/1-series.py
"""

import numpy as np
import pandas as pd


def explain_creating_series() -> None:
    """
    Problem: build a Series and inspect how it stores values and labels.
    Why: a Series pairs every value with an index label. With no index given,
    pandas creates a default RangeIndex 0..N-1. The `array` and `index`
    attributes expose the two halves the Series is made of.
    """
    print("== Creating a Series ==")

    # The simplest Series is formed from just an array of data.
    obj = pd.Series([4, 7, -5, 3])
    print(obj)             # index on the left, values on the right
    print(obj.array)       # the values as a PandasArray
    print(obj.index)       # RangeIndex(start=0, stop=4, step=1)


def explain_custom_index() -> None:
    """
    Problem: identify each data point with a meaningful label.
    Why: a custom index lets you select and assign by label instead of by
    position, which is the whole point of a Series over a plain array.
    """
    print("== Custom index labels and label-based selection ==")

    obj2 = pd.Series([4, 7, -5, 3], index=["d", "b", "a", "c"])
    print(obj2)
    print(obj2.index)         # Index(['d', 'b', 'a', 'c'], dtype='object')

    # Select single values or a set of values using the index labels.
    print(obj2["a"])          # -5
    obj2["d"] = 6             # assignment by label
    print(obj2[["c", "a", "d"]])  # select multiple labels at once


def explain_vectorized_ops() -> None:
    """
    Problem: filter, scale, and transform a Series while keeping its labels.
    Why: Boolean filtering, scalar math, and NumPy ufuncs all preserve the
    index-value link, so the result is still labeled by the original index.
    """
    print("== Boolean filtering, scalar math, ufuncs (index preserved) ==")

    obj2 = pd.Series([6, 7, -5, 3], index=["d", "b", "a", "c"])
    print(obj2[obj2 > 0])     # keep only positive values, labels intact
    print(obj2 * 2)           # scalar multiplication broadcasts to each value
    print(np.exp(obj2))       # a NumPy ufunc applied element-wise


def explain_series_as_dict() -> None:
    """
    Problem: treat a Series like an ordered dictionary and convert to/from dicts.
    Why: a Series IS a mapping of labels to values, so `in` tests membership of
    a label, you can build a Series from a dict, and `to_dict` reverses it.
    """
    print("== Series as an ordered dict; dict interop ==")

    obj2 = pd.Series([4, 7, -5, 3], index=["d", "b", "a", "c"])
    # `in` checks the index labels, exactly like a dictionary's keys.
    print("b" in obj2)        # True
    print("e" in obj2)        # False

    # Build a Series from a dict: keys become the index (in insertion order).
    sdata = {"Ohio": 35000, "Texas": 71000, "Oregon": 16000, "Utah": 5000}
    obj3 = pd.Series(sdata)
    print(obj3)
    # Convert a Series back into a plain dictionary.
    print(obj3.to_dict())


def explain_missing_and_alignment() -> None:
    """
    Problem: detect missing data and combine Series with mismatched labels.
    Why: passing an explicit index can introduce labels with no value (NaN);
    isna/notna flag those, and arithmetic auto-aligns on the index, producing
    NaN wherever the two indexes do not overlap.
    """
    print("== Missing data and automatic index alignment ==")

    sdata = {"Ohio": 35000, "Texas": 71000, "Oregon": 16000, "Utah": 5000}
    states = ["California", "Ohio", "Oregon", "Texas"]
    # "California" has no value in sdata -> NaN; "Utah" is dropped (not in states).
    obj4 = pd.Series(sdata, index=states)
    print(obj4)

    # isna/notna detect missing values; both exist as functions and methods.
    print(pd.isna(obj4))
    print(pd.notna(obj4))
    print(obj4.isna())

    # Arithmetic aligns by label: result index is the union; gaps become NaN.
    obj3 = pd.Series(sdata)
    print(obj3 + obj4)


def explain_name_attribute() -> None:
    """
    Problem: give a Series and its index descriptive names; replace the index.
    Why: the `name` attribute integrates with the rest of pandas (e.g., column
    names when a Series becomes a DataFrame column); the index can be swapped
    in place by assigning a new list of labels.
    """
    print("== The name attribute and reassigning the index ==")

    sdata = {"Ohio": 35000, "Texas": 71000, "Oregon": 16000, "Utah": 5000}
    states = ["California", "Ohio", "Oregon", "Texas"]
    obj4 = pd.Series(sdata, index=states)
    obj4.name = "population"       # name the Series itself
    obj4.index.name = "state"     # name the index
    print(obj4)

    # A Series's index can be altered in place by assignment.
    obj = pd.Series([4, 7, -5, 3])
    obj.index = ["Bob", "Steve", "Jeff", "Ryan"]
    print(obj)


def main() -> None:
    explain_creating_series()
    explain_custom_index()
    explain_vectorized_ops()
    explain_series_as_dict()
    explain_missing_and_alignment()
    explain_name_attribute()


main()
