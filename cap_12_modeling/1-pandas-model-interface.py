"""
Interfacing Between pandas and Model Code (Section 12.1)

A common workflow for model development is to use pandas for data loading and
cleaning before switching over to a modeling library to build the model itself.
The point of contact between pandas and other analysis libraries is usually the
NumPy array: you wrangle a DataFrame, then hand a plain ndarray (the "design
matrix") to statsmodels or scikit-learn, and afterward reattach the model's
parameter names to the resulting columns or Series by hand.

This file covers turning a DataFrame into a NumPy array with `to_numpy`, the
caveat that heterogeneous data yields an object array, selecting a subset of
columns with `loc` before converting, rebuilding a DataFrame from a 2-D array
with column names, and handling a nonnumeric column by replacing it with dummy
variables via `pd.get_dummies` (then dropping the original and joining the
result back in).

PANDAS <-> MODEL ESSENTIALS
METHOD/FUNCTION       DESCRIPTION
DataFrame.to_numpy    Convert a (preferably homogeneous) frame to an ndarray
DataFrame.columns     The Index of column names (the model's feature names)
DataFrame(arr, ...)   Rebuild a frame from a 2-D array with optional columns
DataFrame.loc[:, ...] Select a column subset before converting to NumPy
pd.get_dummies        One-hot encode a categorical column into 0/1 columns

Run:
    poetry run python cap_12_modeling/1-pandas-model-interface.py
"""

import pandas as pd


def explain_dataframe_to_numpy() -> None:
    """
    Problem: move data out of a DataFrame into the NumPy array models expect.
    Why: pandas and other analysis libraries meet at the NumPy array. `to_numpy`
    strips the labels and returns the raw values; `columns` records the feature
    names so you can reattach them later. For a homogeneous numeric frame the
    result is a clean float array.
    """
    print("== DataFrame.to_numpy and rebuilding a frame ==")

    data = pd.DataFrame(
        {
            "x0": [1, 2, 3, 4, 5],
            "x1": [0.01, -0.01, 0.25, -4.1, 0.0],
            "y": [-1.5, 0.0, 3.6, 1.3, -2.0],
        }
    )
    print(data)
    print(data.columns)        # Index(['x0', 'x1', 'y'], dtype='object')
    print(data.to_numpy())     # the values as a 2-D ndarray

    # To convert back to a DataFrame, pass the 2-D array with optional column names.
    df2 = pd.DataFrame(data.to_numpy(), columns=["one", "two", "three"])
    print(df2)


def explain_heterogeneous_to_numpy() -> None:
    """
    Problem: understand what happens when the frame mixes numbers and strings.
    Why: `to_numpy` is meant for homogeneous data (e.g. all numeric). With
    heterogeneous columns the only common dtype is Python `object`, so the array
    boxes every value — useless for a numeric model, which is exactly why you
    select numeric columns before converting.
    """
    print("== to_numpy on heterogeneous data yields an object array ==")

    data = pd.DataFrame(
        {
            "x0": [1, 2, 3, 4, 5],
            "x1": [0.01, -0.01, 0.25, -4.1, 0.0],
            "y": [-1.5, 0.0, 3.6, 1.3, -2.0],
        }
    )
    df3 = data.copy()
    df3["strings"] = ["a", "b", "c", "d", "e"]
    print(df3)
    print(df3.to_numpy())      # dtype=object: every value is boxed


def explain_column_subset() -> None:
    """
    Problem: feed a model only a subset of the available columns.
    Why: a model rarely uses every column. Selecting the model columns with
    `loc[:, model_cols]` before calling `to_numpy` keeps the design matrix to
    just the predictors you intend to use.
    """
    print("== Selecting a column subset with loc before to_numpy ==")

    data = pd.DataFrame(
        {
            "x0": [1, 2, 3, 4, 5],
            "x1": [0.01, -0.01, 0.25, -4.1, 0.0],
            "y": [-1.5, 0.0, 3.6, 1.3, -2.0],
        }
    )
    model_cols = ["x0", "x1"]
    print(data.loc[:, model_cols].to_numpy())


def explain_categorical_with_dummies() -> None:
    """
    Problem: bring a nonnumeric column into a numeric design matrix.
    Why: models cannot consume category strings directly. `pd.get_dummies`
    one-hot encodes the column into 0/1 indicator columns; you then drop the
    original column and `join` the dummies back, producing an all-numeric frame.
    (pandas returns boolean dummies by default; we request integer columns with
    `dtype=int` so the design matrix is numeric, as in the book's output.)
    """
    print("== Categorical column -> dummy variables (get_dummies) ==")

    data = pd.DataFrame(
        {
            "x0": [1, 2, 3, 4, 5],
            "x1": [0.01, -0.01, 0.25, -4.1, 0.0],
            "y": [-1.5, 0.0, 3.6, 1.3, -2.0],
        }
    )
    # A nonnumeric Categorical column added to the example dataset.
    data["category"] = pd.Categorical(
        ["a", "b", "a", "a", "b"], categories=["a", "b"]
    )
    print(data)

    # Replace 'category' with dummy variables: build the dummies, drop the
    # original column, and join the result back onto the frame.
    dummies = pd.get_dummies(data["category"], prefix="category", dtype=int)
    data_with_dummies = data.drop("category", axis=1).join(dummies)
    print(data_with_dummies)


def main() -> None:
    explain_dataframe_to_numpy()
    explain_heterogeneous_to_numpy()
    explain_column_subset()
    explain_categorical_with_dummies()


main()
