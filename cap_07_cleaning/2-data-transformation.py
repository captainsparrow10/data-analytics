"""
Data Transformation: Duplicates, Mapping, Replacing, Renaming (Section 7.2, part 1)

Filtering, cleaning, and other transformations are another class of important
operations. This file covers the first half of section 7.2: removing duplicate
rows (`duplicated`/`drop_duplicates`, including `subset` and `keep`), transforming
data with a function or a mapping (the Series `map` method), replacing values
(`replace` with scalars, lists, or dicts), and renaming axis indexes (`index.map`
in place, or `rename` for a transformed copy).

KEY METHODS IN THIS FILE
METHOD            DESCRIPTION
duplicated        Boolean Series flagging each row that duplicates an earlier row
drop_duplicates   Return a DataFrame with duplicate rows removed (subset/keep)
map               Element-wise transform of a Series via a function or mapping
replace           Substitute one or more values with replacements (list/dict)
rename            Produce a relabeled copy of an object (index/columns)

Run:
    poetry run python cap_07_cleaning/2-data-transformation.py
"""

import numpy as np
import pandas as pd


def explain_removing_duplicates() -> None:
    """
    Problem: detect and remove duplicate rows from a DataFrame.
    Why: `duplicated` returns a Boolean Series marking rows whose column values
    exactly equal an earlier row; `drop_duplicates` returns the frame with those
    rows filtered out. By default both consider ALL columns and keep the FIRST
    occurrence; `subset` restricts the comparison, and `keep="last"` keeps the
    last occurrence instead.
    """
    print("== Removing duplicates ==")

    data = pd.DataFrame({"k1": ["one", "two"] * 3 + ["two"], "k2": [1, 1, 2, 3, 3, 4, 4]})
    print(data)
    print(data.duplicated())          # Boolean Series: is this row a duplicate?
    print(data.drop_duplicates())     # drop the duplicate rows

    # Filter duplicates based only on a subset of columns.
    data["v1"] = range(7)
    print(data.drop_duplicates(subset=["k1"]))

    # keep="last" returns the last observed combination instead of the first.
    print(data.drop_duplicates(["k1", "k2"], keep="last"))


def explain_transform_with_mapping() -> None:
    """
    Problem: derive a new column by mapping each value through a lookup.
    Why: the Series `map` method accepts a function OR a dictionary-like mapping,
    applying it element-wise — a convenient way to do transformations and other
    data-cleaning operations.
    """
    print("== Transforming data using a function or mapping ==")

    data = pd.DataFrame(
        {
            "food": [
                "bacon", "pulled pork", "bacon", "pastrami", "corned beef",
                "bacon", "pastrami", "honey ham", "nova lox",
            ],
            "ounces": [4, 3, 12, 6, 7.5, 8, 3, 5, 6],
        }
    )
    print(data)

    # A mapping of each distinct meat type to the kind of animal.
    meat_to_animal = {
        "bacon": "pig",
        "pulled pork": "pig",
        "pastrami": "cow",
        "corned beef": "cow",
        "honey ham": "pig",
        "nova lox": "salmon",
    }
    # map with a dict-like lookup gives the animal for each food. (The pandas
    # stubs only type map's argument as a callable, so we pass the dict's bound
    # .get method, which is exactly the lookup the book's dict performs.)
    data["animal"] = data["food"].map(meat_to_animal.get)
    print(data)

    # We could also pass a function that does all the work.
    def get_animal(x: str) -> str:
        return meat_to_animal[x]

    print(data["food"].map(get_animal))


def explain_replacing_values() -> None:
    """
    Problem: substitute sentinel values with proper NA (or other replacements).
    Why: `replace` is a simpler, more flexible alternative to `map` for changing a
    subset of values. It accepts a single value, a list (one replacement for all),
    a list of substitutes (one per matched value), or a dict mapping value to
    replacement. Note this is distinct from `str.replace`, which does element-wise
    string substitution (covered in the string-manipulation file).
    """
    print("== Replacing values ==")

    data = pd.Series([1.0, -999.0, 2.0, -999.0, -1000.0, 3.0])
    print(data)
    print(data.replace(-999, np.nan))                  # one value -> NA
    print(data.replace([-999, -1000], np.nan))         # several values -> NA
    print(data.replace([-999, -1000], [np.nan, 0]))    # a substitute per value
    print(data.replace({-999: np.nan, -1000: 0}))      # via a dict


def explain_renaming_axis_indexes() -> None:
    """
    Problem: transform the axis labels of a DataFrame.
    Why: like values, axis labels can be transformed by a function or mapping.
    `index.map` produces a new Index you can assign back (modifying in place);
    `rename` returns a relabeled COPY without touching the original, and accepts
    either functions (e.g. `str.title`) or dicts targeting a subset of labels.
    """
    print("== Renaming axis indexes ==")

    data = pd.DataFrame(
        np.arange(12).reshape((3, 4)),
        index=["Ohio", "Colorado", "New York"],
        columns=["one", "two", "three", "four"],
    )

    # The axis indexes have a map method, just like a Series.
    def transform(x: str) -> str:
        return x[:4].upper()

    print(data.index.map(transform))
    # Assign back to index to modify the DataFrame in place.
    data.index = data.index.map(transform)
    print(data)

    # rename returns a transformed copy without modifying the original.
    print(data.rename(index=str.title, columns=str.upper))
    # rename with a dict relabels only a subset of axis labels.
    print(data.rename(index={"OHIO": "INDIANA"}, columns={"three": "peekaboo"}))


def main() -> None:
    explain_removing_duplicates()
    explain_transform_with_mapping()
    explain_replacing_values()
    explain_renaming_axis_indexes()


main()
