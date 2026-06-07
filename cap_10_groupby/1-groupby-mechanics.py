"""
GroupBy Mechanics: Split-Apply-Combine (Section 10.1)

Categorizing a dataset and applying a function to each group — whether an
aggregation or a transformation — is a critical part of a data analysis
workflow. Hadley Wickham coined the term *split-apply-combine* for group
operations: in the first stage, the data in a pandas object is *split* into
groups based on one or more *keys*; then a function is *applied* to each group,
producing a new value; finally the results are *combined* into a result object.

A grouping key can take many forms, and they need not all be of the same type:
a list/array of values the same length as the axis, a column name in a
DataFrame, a dict or Series mapping axis labels to group names, or a function
invoked on the axis index.

This file covers grouping a column by one/several keys, group `size`/`count`,
`dropna`, iterating over groups, selecting a column or subset, grouping with
dicts and Series, grouping with functions, and grouping by index levels.

KEY OPERATIONS IN THIS FILE
METHOD/CONCEPT       DESCRIPTION
groupby(keys)        Split an object into groups by column(s), array(s), or keys
GroupBy.mean/size    Aggregate each group; `size` counts rows (incl. NA groups)
iterate groups       `for name, group in grouped:` yields (key, chunk) tuples
grouped["col"]       Column subsetting on a GroupBy for focused aggregation
groupby(mapping)     Group via a dict/Series correspondence of labels to groups
groupby(function)    Group by calling a function on each index label (e.g. len)
groupby(level=)      Aggregate using one level of a hierarchical axis index

Run:
    poetry run python cap_10_groupby/1-groupby-mechanics.py
"""

import numpy as np
import pandas as pd


def _example_frame() -> pd.DataFrame:
    """Build the book's small key1/key2/data1/data2 DataFrame deterministically."""
    # The book uses np.random.standard_normal(7); default_rng is the modern API.
    rng = np.random.default_rng(seed=12345)
    return pd.DataFrame(
        {
            "key1": ["a", "a", None, "b", "b", "a", None],
            "key2": pd.Series([1, 2, 1, 2, 1, None, 1], dtype="Int64"),
            "data1": rng.standard_normal(7),
            "data2": rng.standard_normal(7),
        }
    )


def explain_groupby_basics() -> None:
    """
    Problem: compute the mean of a column using labels from another column.
    Why: `df["data1"].groupby(df["key1"])` produces a GroupBy object — it has not
    computed anything yet; it just holds the information needed to apply an
    operation to each group. Calling `.mean()` splits the data by the unique key
    values and aggregates, returning a Series indexed by the group keys. Passing
    a LIST of keys groups by every unique pair, yielding a hierarchical index.
    """
    print("== GroupBy basics: one key, multiple keys ==")

    df = _example_frame()
    print(df)

    # A GroupBy object is lazy: it knows the grouping but computes nothing yet.
    grouped = df["data1"].groupby(df["key1"])
    print(grouped)          # <...SeriesGroupBy object at 0x...>
    print(grouped.mean())   # group means, indexed by the unique key1 values

    # Passing a list of arrays groups by every observed pair -> MultiIndex result.
    means = df["data1"].groupby([df["key1"], df["key2"]]).mean()
    # .mean() is typed broadly (it could be a scalar); narrow to a Series so the
    # .unstack() call below resolves cleanly.
    assert isinstance(means, pd.Series)
    print(means)
    print(means.unstack())  # pivot the inner key level into columns


def explain_grouping_with_external_arrays() -> None:
    """
    Problem: group using arrays that live outside the DataFrame.
    Why: the group keys can be any arrays of the right length, not just columns.
    Here states and years are standalone arrays aligned to the rows.
    """
    print("== Grouping with external arrays of the right length ==")

    df = _example_frame()
    states = np.array(["OH", "CA", "CA", "OH", "OH", "CA", "OH"])
    years = [2005, 2005, 2006, 2005, 2006, 2005, 2006]
    print(df["data1"].groupby([states, years]).mean())


def explain_grouping_by_column_names() -> None:
    """
    Problem: group a whole DataFrame by one or more of its own columns.
    Why: when the grouping info is in the same frame, pass the column NAME(S) as
    the key. Non-key string columns are "nuisance" columns: the book relied on
    them being silently dropped, but pandas 3.0 raises instead, so we pass
    `numeric_only=True` to aggregate only the numeric columns. `size` returns
    group sizes; `count` returns the number of non-null values per group. Missing
    values in a group key are dropped by default — pass `dropna=False` to keep.
    """
    print("== Grouping by column name(s); size, count, dropna ==")

    df = _example_frame()
    # numeric_only=True skips the nuisance string column key1 when it is not a key.
    print(df.groupby("key1").mean(numeric_only=True))
    print(df.groupby("key2").mean(numeric_only=True))
    print(df.groupby(["key1", "key2"]).mean(numeric_only=True))

    # size counts rows per group (a Series); missing key values are excluded...
    print(df.groupby(["key1", "key2"]).size())
    # ...unless dropna=False keeps NA groups in the result.
    print(df.groupby("key1", dropna=False).size())
    print(df.groupby(["key1", "key2"], dropna=False).size())

    # count gives the number of non-null values in each group.
    print(df.groupby("key1").count())


def explain_iterating_over_groups() -> None:
    """
    Problem: iterate over the pieces a GroupBy produces.
    Why: a GroupBy supports iteration, yielding 2-tuples of (group name, chunk).
    With multiple keys the name is a tuple of the key values. A handy recipe is
    building a dict of the chunks via a dict comprehension.
    """
    print("== Iterating over groups ==")

    df = _example_frame()
    for name, group in df.groupby("key1"):
        print(name)
        print(group)

    # With multiple keys, the first element of each tuple is a tuple of values.
    # (The stubs type the group name as a single Hashable, so we keep it as one
    # `key` variable rather than destructuring it into (k1, k2) at the loop head.)
    for key, group in df.groupby(["key1", "key2"]):
        print(key)
        print(group)

    # Computing a dict of the data pieces in one line.
    pieces = {name: group for name, group in df.groupby("key1")}
    print(pieces["b"])


def explain_grouping_columns_by_kind() -> None:
    """
    Problem: group the COLUMNS of a DataFrame (not the rows) by a correspondence.
    Why: the book groups columns with `groupby(..., axis="columns")`. The
    `axis="columns"` argument on groupby was removed in pandas 2.x, so we
    transpose, group the (now) rows by the mapping, aggregate, and transpose back.
    """
    print("== Grouping columns by kind (transpose -> group -> transpose) ==")

    df = _example_frame()
    mapping = {"key1": "key", "key2": "key", "data1": "data", "data2": "data"}
    # Group the numeric "data" columns; key columns are kept separate by the map.
    by_kind = df[["data1", "data2"]].T.groupby({"data1": "data", "data2": "data"}).sum()
    assert isinstance(by_kind, pd.DataFrame)
    print(by_kind.T)
    # The mapping above shows the full correspondence the book passes via axis.
    print(mapping)


def explain_selecting_columns() -> None:
    """
    Problem: aggregate only a few columns of a grouped DataFrame.
    Why: indexing a GroupBy with a column name (or list of names) is column
    subsetting for aggregation. `df.groupby("k")["data2"]` is shorthand for
    `df["data2"].groupby(df["k"])`. A scalar name yields a SeriesGroupBy; a list
    yields a (grouped) DataFrame.
    """
    print("== Selecting a column or subset of columns ==")

    df = _example_frame()
    # A list of columns -> grouped DataFrame result.
    print(df.groupby(["key1", "key2"])[["data2"]].mean())

    # A single column name -> grouped Series result.
    s_grouped = df.groupby(["key1", "key2"])["data2"]
    print(s_grouped)          # <...SeriesGroupBy object at 0x...>
    print(s_grouped.mean())


def explain_grouping_with_dict_and_series() -> None:
    """
    Problem: group using a dict or Series that maps labels to group names.
    Why: grouping information may exist as a correspondence rather than an array.
    A dict/Series maps each column (here) to a group; unused keys are fine. We
    group the COLUMNS, which in pandas 3.0 means transpose -> group -> transpose.
    """
    print("== Grouping with dictionaries and Series ==")

    rng = np.random.default_rng(seed=12345)
    people = pd.DataFrame(
        rng.standard_normal((5, 5)),
        columns=["a", "b", "c", "d", "e"],
        index=["Joe", "Steve", "Wanda", "Jill", "Trey"],
    )
    # Set a few NA values (Copy-on-Write: assign through .iloc).
    people.iloc[2:3, [1, 2]] = np.nan
    print(people)

    # A column->group mapping. Key "f" is unused, which is OK.
    mapping = {"a": "red", "b": "red", "c": "blue", "d": "blue", "e": "red", "f": "orange"}
    by_column = people.T.groupby(mapping).sum()
    assert isinstance(by_column, pd.DataFrame)
    print(by_column.T)

    # The same works for a Series, a fixed-size mapping.
    map_series = pd.Series(mapping)
    print(map_series)
    counts = people.T.groupby(map_series).count()
    assert isinstance(counts, pd.DataFrame)
    print(counts.T)


def explain_grouping_with_functions() -> None:
    """
    Problem: derive the group key by calling a function on each index label.
    Why: any function passed as a key is called once per index value, and its
    return value is used as the group name — a generic alternative to a dict or
    Series. Functions can be MIXED with arrays/dicts/Series; everything is
    converted to arrays internally.
    """
    print("== Grouping with functions ==")

    rng = np.random.default_rng(seed=12345)
    people = pd.DataFrame(
        rng.standard_normal((5, 5)),
        columns=["a", "b", "c", "d", "e"],
        index=["Joe", "Steve", "Wanda", "Jill", "Trey"],
    )
    # Group rows by the length of each person's name with the built-in len.
    print(people.groupby(len).sum())

    # Mixing a function with an explicit array of keys.
    key_list = ["one", "one", "one", "two", "two"]
    print(people.groupby([len, key_list]).min())


def explain_grouping_by_index_levels() -> None:
    """
    Problem: aggregate using one level of a hierarchical axis index.
    Why: for hierarchically indexed data you can group by a level via `level=`.
    The book groups the COLUMN levels with `axis="columns"`; since that argument
    was removed, we transpose, group the rows by the level, and transpose back.
    """
    print("== Grouping by index levels ==")

    rng = np.random.default_rng(seed=12345)
    columns = pd.MultiIndex.from_arrays(
        [["US", "US", "US", "JP", "JP"], [1, 3, 5, 1, 3]],
        names=["cty", "tenor"],
    )
    hier_df = pd.DataFrame(rng.standard_normal((4, 5)), columns=columns)
    print(hier_df)

    # Count by the "cty" column level: transpose -> group by level -> transpose.
    by_cty = hier_df.T.groupby(level="cty").count()
    assert isinstance(by_cty, pd.DataFrame)
    print(by_cty.T)


def main() -> None:
    explain_groupby_basics()
    explain_grouping_with_external_arrays()
    explain_grouping_by_column_names()
    explain_iterating_over_groups()
    explain_grouping_columns_by_kind()
    explain_selecting_columns()
    explain_grouping_with_dict_and_series()
    explain_grouping_with_functions()
    explain_grouping_by_index_levels()


main()
