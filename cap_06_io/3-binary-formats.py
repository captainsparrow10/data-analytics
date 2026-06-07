"""
Binary Data Formats (Section 6.2)

Text is convenient but not always efficient. For faster, more compact storage,
pandas supports several binary formats. The simplest is Python's built-in `pickle`
serialization (`to_pickle`/`read_pickle`), good for short-term storage only.
Microsoft Excel files are read with `pd.read_excel` / `pd.ExcelFile` and written
with `ExcelWriter` / `to_excel` (via openpyxl). HDF5 ("hierarchical data format")
is a respected format for large scientific arrays: one file can hold many datasets,
supports compression, and lets you read small slices of much larger arrays — the
`HDFStore` class behaves like a dictionary, with `to_hdf`/`read_hdf` as shortcuts.
Everything here runs inside a temporary directory so the repo stays clean.

BINARY FORMAT ENTRY POINTS
FUNCTION / CLASS     DESCRIPTION
DataFrame.to_pickle  Serialize an object to disk in Python's pickle format
pd.read_pickle       Read a pickled pandas object back into memory
pd.ExcelFile         Open a workbook to inspect sheet names and parse sheets
pd.read_excel        Read an Excel sheet straight into a DataFrame
pd.ExcelWriter       Writer object for emitting one or more sheets
DataFrame.to_excel   Write a DataFrame to an Excel sheet
pd.HDFStore          Dict-like handle to an HDF5 file (fixed and table schemas)
DataFrame.to_hdf     Shortcut to write a DataFrame into an HDF5 file
pd.read_hdf          Shortcut to read (and optionally query) from an HDF5 file

Run:
    poetry run python cap_06_io/3-binary-formats.py
"""

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd


def explain_pickle() -> None:
    """
    Problem: serialize a DataFrame to disk and read it back unchanged.
    Why: `to_pickle` writes the in-memory object in Python's binary pickle format;
    `read_pickle` restores it. Pickle is recommended only for short-term storage —
    the format is not guaranteed stable across library versions.
    """
    print("== pickle: to_pickle / read_pickle ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)
        (examples / "ex1.csv").write_text(
            "a,b,c,d,message\n1,2,3,4,hello\n5,6,7,8,world\n9,10,11,12,foo\n"
        )
        frame = pd.read_csv(examples / "ex1.csv")
        print(frame)

        # Round-trip the frame through a pickle file.
        frame.to_pickle(examples / "frame_pickle")
        print(pd.read_pickle(examples / "frame_pickle"))


def explain_excel() -> None:
    """
    Problem: read from and write to Microsoft Excel workbooks.
    Why: `pd.ExcelFile` opens a workbook so you can list `sheet_names` and `parse`
    individual sheets (with `index_col` to promote an index column). `read_excel`
    is the one-shot equivalent. To write, create an `ExcelWriter` and call
    `to_excel`, or pass a path directly to `to_excel`.
    """
    print("== Microsoft Excel files ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)
        frame = pd.DataFrame(
            {
                "a": [1, 5, 9],
                "b": [2, 6, 10],
                "c": [3, 7, 11],
                "d": [4, 8, 12],
                "message": ["hello", "world", "foo"],
            }
        )

        # Write the workbook first (the book reads a pre-existing ex1.xlsx).
        xlsx_path = examples / "ex1.xlsx"
        # Pass a path directly to to_excel (simplest form).
        frame.to_excel(xlsx_path, sheet_name="Sheet1", index=False)

        # Open with ExcelFile to inspect sheets, then parse one.
        xlsx = pd.ExcelFile(xlsx_path)
        print(xlsx.sheet_names)
        print(xlsx.parse(sheet_name="Sheet1"))

        # read_excel is the one-line shortcut.
        print(pd.read_excel(xlsx_path, sheet_name="Sheet1"))

        # Writing via an explicit ExcelWriter (use a context manager; the book's
        # writer.save() is deprecated — closing the writer persists the file).
        with pd.ExcelWriter(examples / "ex2.xlsx") as writer:
            frame.to_excel(writer, sheet_name="Sheet1", index=False)
        print(pd.read_excel(examples / "ex2.xlsx", sheet_name="Sheet1"))


def explain_hdf5() -> None:
    """
    Problem: store and selectively query pandas objects in HDF5.
    Why: `HDFStore` acts like a dict for DataFrames/Series. The "fixed" schema
    (default) is fast but not queryable; the "table" schema (via `put(...,
    format="table")` or `to_hdf(..., format="table")`) is slower but supports
    `where=[...]` query expressions to read only matching rows — key for data too
    big to fit in memory. `read_hdf` is the shortcut reader.
    """
    print("== HDF5: HDFStore, to_hdf / read_hdf ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)
        h5_path = str(examples / "mydata.h5")

        rng = np.random.default_rng(seed=12345)
        frame = pd.DataFrame({"a": rng.standard_normal(100)})

        # HDFStore behaves like a dictionary of objects.
        store = pd.HDFStore(h5_path)
        store["obj1"] = frame
        store["obj1_col"] = frame["a"]
        print(store)
        print(store["obj1"].head())

        # The "table" schema supports query operations via where=[...].
        store.put("obj2", frame, format="table")
        print(store.select("obj2", where=["index >= 10 and index <= 15"]))
        store.close()

        # to_hdf / read_hdf are shortcuts to the same machinery.
        frame.to_hdf(h5_path, key="obj3", format="table")
        print(pd.read_hdf(h5_path, "obj3", where=["index < 5"]))


def main() -> None:
    explain_pickle()
    explain_excel()
    explain_hdf5()


main()
