"""
Index Objects: Holding Axis Labels (Section 5.1)

pandas's Index objects are responsible for holding the axis labels (including a
DataFrame's column names) and other metadata (like the axis name or names). Any
array or other sequence of labels you use when constructing a Series or
DataFrame is internally converted to an Index. Index objects are *immutable*,
which makes them safe to share across data structures, and they behave like a
fixed-size set — except that, unlike a Python set, an Index CAN contain
duplicate labels.

This file covers immutability, sharing an Index, set-like membership, duplicate
labels, and the family of set-logic/edit methods on Index objects.

INDEX METHODS AND PROPERTIES
METHOD/PROPERTY    DESCRIPTION
append             Concatenate with additional Index objects, producing a new Index
difference         Compute set difference as an Index
intersection       Compute set intersection
union              Compute set union
isin               Boolean array: whether each value is contained in the passed collection
delete             New Index with the element at position i deleted
drop               New Index with the passed values deleted
insert             New Index with an element inserted at position i
unique             The array of unique values in the Index
is_unique          True if the Index has no duplicate labels

Run:
    poetry run python cap_03_panda/3-index-objects.py
"""

import numpy as np
import pandas as pd


def explain_immutability_and_sharing() -> None:
    """
    Problem: show that an Index cannot be mutated and can be reused safely.
    Why: immutability is exactly what makes it safe to share one Index object
    across multiple Series/DataFrames — no one can change the labels underneath
    another structure. Attempting to assign into an Index raises TypeError.
    """
    print("== Index objects are immutable; sharing an Index ==")

    obj = pd.Series(np.arange(3), index=["a", "b", "c"])
    index = obj.index
    print(index)        # Index(['a', 'b', 'c'], dtype='object')
    print(index[1:])    # slicing produces a new Index

    # Index objects are immutable, so element assignment is rejected.
    try:
        index[1] = "d"  # type: ignore[index]  # demonstrates the TypeError
    except TypeError as err:
        print("TypeError:", err)

    # Immutability lets the same Index be shared among data structures.
    labels = pd.Index(np.arange(3))
    print(labels)
    obj2 = pd.Series([1.5, -2.5, 0], index=labels)
    print(obj2)
    print(obj2.index is labels)  # True -> the exact same object is reused


def explain_set_behavior_and_duplicates() -> None:
    """
    Problem: use an Index like a set, and observe that duplicates are allowed.
    Why: `in` tests label membership, just like a set; but unlike a Python set,
    an Index may hold repeated labels, and selections on a duplicate label
    return every matching entry.
    """
    print("== Set-like behavior; Index can hold duplicates ==")

    populations = {
        "Ohio": {2000: 1.5, 2001: 1.7, 2002: 3.6},
        "Nevada": {2001: 2.4, 2002: 2.9},
    }
    frame3 = pd.DataFrame(populations)
    frame3.columns.name = "state"
    print(frame3.columns)
    print("Ohio" in frame3.columns)  # True
    print(2003 in frame3.index)      # False

    # Unlike a Python set, a pandas Index can contain duplicate labels.
    print(pd.Index(["foo", "foo", "bar", "bar"]))


def explain_index_methods() -> None:
    """
    Problem: combine and edit Index objects with set logic.
    Why: these methods answer common questions about the labels (what is shared,
    what differs, what is present) and let you derive new Index objects without
    mutating the original — append/insert/delete/drop build edited copies.
    """
    print("== Index methods: set logic and editing ==")

    idx1 = pd.Index(["a", "b", "c"])
    idx2 = pd.Index(["b", "c", "d"])

    print(idx1.append(idx2))        # ['a','b','c','b','c','d']
    print(idx1.difference(idx2))    # in idx1 but not idx2 -> ['a']
    print(idx1.intersection(idx2))  # common -> ['b','c']
    print(idx1.union(idx2))         # all -> ['a','b','c','d']
    print(idx1.isin(["b", "c"]))    # [False True True]
    print(idx1.delete(1))           # remove position 1 -> ['a','c']
    print(idx1.drop("b"))           # remove label 'b' -> ['a','c']
    print(idx1.insert(1, "z"))      # insert at position 1 -> ['a','z','b','c']
    print(pd.Index(["a", "a", "b"]).unique())  # unique labels -> ['a','b']


def main() -> None:
    explain_immutability_and_sharing()
    explain_set_behavior_and_duplicates()
    explain_index_methods()


main()
