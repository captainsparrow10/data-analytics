"""
Extension Data Types (Section 7.3)

pandas was originally built upon NumPy, which led to shortcomings: missing-data
handling for integers and Booleans was incomplete (pandas had to upcast to
float64 and use np.nan), string data was memory-hungry, and some types could not
be stored efficiently. pandas now has an *extension type* system that adds new
data types — even ones NumPy does not support natively — as first-class citizens.
This file covers nullable integer/Boolean/string extension types, the dedicated
`pd.NA` sentinel, converting columns with `astype`, and a brief note on
Arrow-backed dtypes.

SOME pandas EXTENSION DATA TYPES
EXTENSION TYPE    DESCRIPTION
Int64Dtype        64-bit nullable signed integer; use "Int64" when passing as string
BooleanDtype      Nullable Boolean data; use "boolean" when passing as string
StringDtype       Dedicated string type (uses pyarrow); use "string" as string
Float64Dtype      64-bit nullable floating point; use "Float64" when passing as string
(others)          Int8/16/32, UInt8/16/32/64, Float32, CategoricalDtype, DatetimeTZDtype

Run:
    poetry run python cap_07_cleaning/4-extension-data-types.py
"""

import pyarrow as pa
import pandas as pd


def explain_legacy_vs_extension() -> None:
    """
    Problem: contrast the legacy NumPy-backed behavior with a nullable integer.
    Why: a plain integer Series with a missing value is silently upcast to float64
    with np.nan. The `pd.Int64Dtype` extension type keeps the integer nature and
    represents the gap with the dedicated `pd.NA` sentinel, which `isna` detects.
    """
    print("== Legacy float64 behavior vs. nullable Int64 ==")

    # Legacy: a missing value forces float64 and np.nan.
    s = pd.Series([1, 2, 3, None])
    print(s)
    print(s.dtype)               # float64

    # Extension type: stays integer; the gap is <NA>.
    s = pd.Series([1, 2, 3, None], dtype=pd.Int64Dtype())
    print(s)
    print(s.isna())
    print(s.dtype)               # Int64Dtype()


def explain_pd_na_sentinel() -> None:
    """
    Problem: understand the value that marks a missing extension-type entry.
    Why: extension arrays use the special `pd.NA` sentinel (not np.nan). The
    capitalized string shorthand "Int64" selects the extension type; the lowercase
    "int64" would give a non-nullable NumPy-based type instead.
    """
    print("== The pd.NA sentinel ==")

    s = pd.Series([1, 2, 3, None], dtype=pd.Int64Dtype())
    print(s[3])                  # <NA>
    print(s[3] is pd.NA)         # True

    # The string shorthand "Int64" (capital I) selects the same extension type.
    s = pd.Series([1, 2, 3, None], dtype="Int64")
    print(s.dtype)


def explain_string_extension() -> None:
    """
    Problem: store text without NumPy object arrays.
    Why: the string extension type (`pd.StringDtype`, requires pyarrow) uses far
    less memory and is usually faster for operations on large datasets than the
    legacy object dtype. Missing values appear as `<NA>`.
    """
    print("== The string extension type ==")

    s = pd.Series(["one", "two", None, "three"], dtype=pd.StringDtype())
    print(s)
    print(s.dtype)               # string


def explain_astype_to_extension() -> None:
    """
    Problem: convert ordinary columns into extension types as part of cleaning.
    Why: extension types can be passed to `astype`, so you can opt into nullable
    integers, dedicated strings, and nullable Booleans column by column. After
    conversion, all three columns represent missing data with the unified `<NA>`.
    """
    print("== Converting columns with astype ==")

    df = pd.DataFrame(
        {
            "A": [1, 2, None, 4],
            "B": ["one", "two", "three", None],
            "C": [False, None, False, True],
        }
    )
    print(df)

    df["A"] = df["A"].astype("Int64")
    df["B"] = df["B"].astype("string")
    df["C"] = df["C"].astype("boolean")
    print(df)
    print(df.dtypes)


def explain_arrow_backed() -> None:
    """
    Problem: opt into Apache Arrow-backed storage for a column.
    Why: pandas can wrap PyArrow arrays via `pd.ArrowDtype`, giving Arrow's
    memory layout and broad type system. This is an advanced option; here we just
    show it is available (it requires the pyarrow library).
    """
    print("== Arrow-backed dtypes (brief) ==")

    # pd.ArrowDtype wraps a pyarrow type; here, a 64-bit integer column.
    s = pd.Series([1, 2, 3, None], dtype=pd.ArrowDtype(pa.int64()))
    print(s)
    print(s.dtype)


def main() -> None:
    explain_legacy_vs_extension()
    explain_pd_na_sentinel()
    explain_string_extension()
    explain_astype_to_extension()
    explain_arrow_backed()


main()
