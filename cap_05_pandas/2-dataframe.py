"""
DataFrame: A Rectangular Table of Data (Section 5.1)

A DataFrame represents a rectangular table of data and contains an ordered,
named collection of columns, each of which can be a different value type
(numeric, string, Boolean, etc.). The DataFrame has both a row index and a
column index; it can be thought of as a dictionary of Series all sharing the
same index. It is the workhorse structure for tabular, heterogeneous data.

This file covers constructing a DataFrame from a dict of equal-length lists,
`head`/`tail`, controlling column order, retrieving columns (bracket and
attribute access) and rows (`loc`/`iloc`), assigning and deleting columns,
constructing from a nested dict, transposing, naming the index/columns, and
exporting to a NumPy array.

DATAFRAME ESSENTIALS
ATTRIBUTE/METHOD   DESCRIPTION
head / tail        First / last five rows (handy for large frames)
columns            The Index of column labels
loc / iloc         Row (and column) selection by label / by integer position
del df[col]        Delete a column, like deleting a dict key
T                  Transpose: swap rows and columns
to_numpy           Return the data as a two-dimensional ndarray

Run:
    poetry run python cap_05_pandas/2-dataframe.py
"""

import numpy as np
import pandas as pd


def explain_constructing() -> None:
    """
    Problem: build a DataFrame and peek at its rows.
    Why: a dict of equal-length lists/arrays is the most common constructor;
    each key becomes a column. head/tail show only the first/last five rows so
    large tables stay readable. The `columns` keyword fixes the column order.
    """
    print("== Constructing a DataFrame; head/tail; column order ==")

    data = {
        "state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada", "Nevada"],
        "year": [2000, 2001, 2002, 2001, 2002, 2003],
        "pop": [1.5, 1.7, 3.6, 2.4, 2.9, 3.2],
    }
    frame = pd.DataFrame(data)
    print(frame)
    print(frame.head())   # first five rows
    print(frame.tail())   # last five rows

    # Passing `columns` arranges the columns in the requested order.
    print(pd.DataFrame(data, columns=["year", "state", "pop"]))


def explain_retrieving_columns_rows() -> None:
    """
    Problem: pull individual columns and rows out of a DataFrame.
    Why: columns come out as Series via bracket or attribute access; a column
    requested in `columns` but absent from the data appears as all-NaN. Rows are
    retrieved by label with `loc` and by integer position with `iloc`.
    """
    print("== Retrieving columns and rows ==")

    data = {
        "state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada", "Nevada"],
        "year": [2000, 2001, 2002, 2001, 2002, 2003],
        "pop": [1.5, 1.7, 3.6, 2.4, 2.9, 3.2],
    }
    # "debt" is not in the data, so it is created as an all-NaN column.
    frame2 = pd.DataFrame(data, columns=["year", "state", "pop", "debt"])
    print(frame2)
    print(frame2.columns)

    # A column is retrieved as a Series by dict-like or attribute access.
    print(frame2["state"])
    print(frame2.year)

    # Rows are retrieved by label with loc, by integer position with iloc.
    print(frame2.loc[1])
    print(frame2.iloc[2])


def explain_assigning_columns() -> None:
    """
    Problem: add, modify, and delete DataFrame columns.
    Why: a column can be set to a scalar (broadcast), an array (length must
    match), or a Series (which realigns by label, inserting NaN for missing
    labels). The `del` keyword removes a column just like a dict key.
    """
    print("== Assigning and deleting columns ==")

    data = {
        "state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada", "Nevada"],
        "year": [2000, 2001, 2002, 2001, 2002, 2003],
        "pop": [1.5, 1.7, 3.6, 2.4, 2.9, 3.2],
    }
    frame2 = pd.DataFrame(data, columns=["year", "state", "pop", "debt"])

    frame2["debt"] = 16.5            # scalar broadcasts to every row
    print(frame2)
    frame2["debt"] = np.arange(6.0)  # an array; its length must match the rows
    print(frame2)

    # A Series realigns by label; labels absent from the frame become NaN.
    val = pd.Series([-1.2, -1.5, -1.7], index=["two", "four", "five"])
    frame2["debt"] = val
    print(frame2)

    # Assigning a column that doesn't exist creates a new one.
    frame2["eastern"] = frame2["state"] == "Ohio"
    print(frame2)

    # The del keyword removes a column. (New columns cannot be made via the
    # dot-attribute form — only existing ones are readable that way.)
    del frame2["eastern"]
    print(frame2.columns)


def explain_nested_dict_and_transpose() -> None:
    """
    Problem: build a DataFrame from a nested dict and flip its axes.
    Why: with a dict of dicts, outer keys become columns and inner keys become
    the row index (unioned across columns). `.T` transposes, swapping rows and
    columns just like a NumPy array.
    """
    print("== Constructing from a nested dict; transpose ==")

    populations = {
        "Ohio": {2000: 1.5, 2001: 1.7, 2002: 3.6},
        "Nevada": {2001: 2.4, 2002: 2.9},
    }
    frame3 = pd.DataFrame(populations)
    print(frame3)

    # Transpose: rows become columns and vice versa.
    print(frame3.T)


def explain_index_names_and_to_numpy() -> None:
    """
    Problem: label the row/column axes and export the raw values.
    Why: `index.name`/`columns.name` are displayed and integrate with pandas;
    `to_numpy()` returns the underlying 2D ndarray, choosing a dtype broad
    enough to hold every column (object when columns mix types).
    """
    print("== index.name / columns.name; to_numpy ==")

    populations = {
        "Ohio": {2000: 1.5, 2001: 1.7, 2002: 3.6},
        "Nevada": {2001: 2.4, 2002: 2.9},
    }
    frame3 = pd.DataFrame(populations)
    frame3.index.name = "year"
    frame3.columns.name = "state"
    print(frame3)

    # to_numpy returns the data as a 2D ndarray (here, float64).
    print(frame3.to_numpy())


def main() -> None:
    explain_constructing()
    explain_retrieving_columns_rows()
    explain_assigning_columns()
    explain_nested_dict_and_transpose()
    explain_index_names_and_to_numpy()


main()
