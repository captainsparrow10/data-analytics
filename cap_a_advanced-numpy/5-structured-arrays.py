"""
Structured and Record Arrays (Appendix A.5)

So far the ndarray has been a HOMOGENEOUS container: every element occupies the
same number of bytes given by a single dtype. A *structured* array relaxes that:
each element is like a C struct (hence "structured") or a row in a SQL table,
made of several named fields that may have different types. This file covers:

  * Building a structured dtype as a list of (name, type) tuples.
  * Accessing fields by name and records by position.
  * Nested data types and multidimensional fields.
  * Why structured arrays are useful.

Run:
    poetry run python cap_a_advanced-numpy/5-structured-arrays.py
"""

import numpy as np


def explain_structured_basics() -> None:
    """
    Problem: store rows with differently typed columns in a single ndarray.
    Why: a structured dtype is a list of (field_name, field_type) tuples. Each
    element is then a tuple-like record whose fields are accessed like a dict.
    """
    print("== Structured array basics ==")

    # Two named fields: a float64 'x' and an int32 'y'.
    dtype = [("x", np.float64), ("y", np.int32)]
    sarr = np.array([(1.5, 6), (np.pi, -2)], dtype=dtype)
    print(sarr)

    # Index by position to get one record (a tuple-like object).
    print(sarr[0])           # (1.5, 6)
    print(sarr[0]["y"])      # 6 -- access a field of one record

    # Field names live in dtype.names.
    print(sarr.dtype.names)  # ('x', 'y')

    # Accessing a field returns a strided VIEW (no copy) over that column.
    print(sarr["x"])         # [1.5  3.14159265]


def explain_nested_and_multidim_fields() -> None:
    """
    Problem: represent richer records -- a field that is itself an array, or a
    field that is itself a structured type.
    Why: passing a shape with a field makes it multidimensional; nesting a dtype
    inside a field expresses complex structures as one contiguous memory block.
    """
    print("== Nested and multidimensional fields ==")

    # A multidimensional field: 'x' is an array of length 3 per record.
    dtype = [("x", np.int64, 3), ("y", np.int32)]
    arr = np.zeros(4, dtype=dtype)
    print(arr)

    # arr[0]['x'] is the length-3 array for the first record.
    print(arr[0]["x"])  # [0 0 0]
    # arr['x'] gives a 2D array (one row per record).
    print(arr["x"])     # shape (4, 3)

    # Nested dtype: field 'x' is itself a struct with sub-fields 'a' and 'b'.
    nested_dtype = [("x", [("a", "f8"), ("b", "f4")]), ("y", np.int32)]
    data = np.array([((1, 2), 5), ((3, 4), 6)], dtype=nested_dtype)
    print(data["x"])       # the nested struct column
    print(data["y"])       # [5 6]
    print(data["x"]["a"])  # [1. 3.] -- reach into a nested sub-field


def explain_why_structured() -> None:
    """
    Problem: understand when structured arrays earn their keep.
    Why: they are a lower-level tool than a pandas DataFrame. Because each record
    is a fixed number of bytes laid out like a C struct, they are efficient for
    writing/reading binary data to disk or memory maps and for parsing
    fixed-length record byte streams (e.g. np.fromfile on legacy formats).
    """
    print("== Why use structured arrays ==")

    dtype = [("name", "S10"), ("age", np.int32), ("weight", np.float64)]
    people = np.array(
        [(b"Alice", 30, 55.0), (b"Bob", 42, 80.5)],
        dtype=dtype,
    )
    # Each record is a fixed-size block: 10 + 4 + 8 = 22 bytes (here, padded).
    print(people.dtype.itemsize, "bytes per record")
    print(people["name"])
    print(people["age"].mean())  # vectorized ops still work per field


def main() -> None:
    explain_structured_basics()
    explain_nested_and_multidim_fields()
    explain_why_structured()


main()
