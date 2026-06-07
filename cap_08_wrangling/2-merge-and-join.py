"""
Combining and Merging Datasets: Database-Style Joins (Section 8.2, part 1)

Merge or join operations combine datasets by linking rows using one or more
*keys*. These operations are central to relational (SQL-based) databases. The
`pandas.merge` function is the main entry point: it connects rows in DataFrames
based on one or more keys, implementing database join operations. When the keys
live in the row index instead of a column, `left_index`/`right_index` (or the
`DataFrame.join` convenience method) join on the index.

This file covers `pd.merge` with `on`, `left_on`/`right_on`, the four `how`
join types (inner/left/right/outer), many-to-many joins, merging on multiple
keys, the `suffixes` option for overlapping column names, merging on the index,
and `DataFrame.join`.

SOME pandas.merge ARGUMENTS
ARGUMENT               DESCRIPTION
on                     Column name(s) to join on; must exist in both frames
left_on / right_on     Columns to use as join keys in the left / right frame
how                    Join type: "inner" (default), "left", "right", "outer"
left_index/right_index Use the row index of the left / right frame as its key
suffixes               Strings appended to otherwise-overlapping column names
join (method)          DataFrame method: left join on index by default

Run:
    poetry run python cap_08_wrangling/2-merge-and-join.py
"""

import pandas as pd


def explain_basic_merge() -> None:
    """
    Problem: combine two frames that share a key column.
    Why: `pd.merge` links rows on overlapping column names by default, but it is
    good practice to name the key explicitly with `on`. This is a *many-to-one*
    join: df1 has many rows per key, df2 has one row per key. (The book uses the
    nullable Int64 extension dtype so missing integers become <NA> rather than
    forcing the column to float.)
    """
    print("== Basic many-to-one merge (on=) ==")

    df1 = pd.DataFrame(
        {"key": ["b", "b", "a", "c", "a", "a", "b"], "data1": pd.Series(range(7), dtype="Int64")}
    )
    df2 = pd.DataFrame({"key": ["a", "b", "d"], "data2": pd.Series(range(3), dtype="Int64")})
    print(df1)
    print(df2)

    # Without `on`, merge uses the overlapping column names as keys...
    print(pd.merge(df1, df2))
    # ...but naming the key explicitly is the recommended practice.
    print(pd.merge(df1, df2, on="key"))


def explain_different_key_names() -> None:
    """
    Problem: join two frames whose key columns have different names.
    Why: when the key is called something different in each frame, pass `left_on`
    and `right_on` to name them separately. The result keeps both columns.
    """
    print("== Merging with different key column names (left_on/right_on) ==")

    df3 = pd.DataFrame(
        {"lkey": ["b", "b", "a", "c", "a", "a", "b"], "data1": pd.Series(range(7), dtype="Int64")}
    )
    df4 = pd.DataFrame({"rkey": ["a", "b", "d"], "data2": pd.Series(range(3), dtype="Int64")})
    print(pd.merge(df3, df4, left_on="lkey", right_on="rkey"))


def explain_how_join_types() -> None:
    """
    Problem: control which key combinations survive the join.
    Why: by default merge does an "inner" join (the intersection of keys). The
    other options are "left", "right", and "outer" (the union). Rows that do not
    match on the other side get NA in the missing columns.

    JOIN TYPES (how=)
    inner   key combinations observed in BOTH tables
    left    all key combinations in the LEFT table
    right   all key combinations in the RIGHT table
    outer   all key combinations in EITHER table
    """
    print("== Join types: how = inner / left / right / outer ==")

    df1 = pd.DataFrame(
        {"key": ["b", "b", "a", "c", "a", "a", "b"], "data1": pd.Series(range(7), dtype="Int64")}
    )
    df2 = pd.DataFrame({"key": ["a", "b", "d"], "data2": pd.Series(range(3), dtype="Int64")})

    # Outer join takes the union of keys; "c" and "d" appear with <NA>.
    print(pd.merge(df1, df2, how="outer"))

    df3 = pd.DataFrame(
        {"lkey": ["b", "b", "a", "c", "a", "a", "b"], "data1": pd.Series(range(7), dtype="Int64")}
    )
    df4 = pd.DataFrame({"rkey": ["a", "b", "d"], "data2": pd.Series(range(3), dtype="Int64")})
    print(pd.merge(df3, df4, left_on="lkey", right_on="rkey", how="outer"))


def explain_many_to_many() -> None:
    """
    Problem: join when BOTH frames have repeated keys.
    Why: many-to-many merges form the Cartesian product of the matching rows. With
    three "b" rows on the left and two on the right, the result has six "b" rows.
    The `how` option still controls which distinct keys appear.
    """
    print("== Many-to-many merge (Cartesian product of matching keys) ==")

    df1 = pd.DataFrame(
        {"key": ["b", "b", "a", "c", "a", "b"], "data1": pd.Series(range(6), dtype="Int64")}
    )
    df2 = pd.DataFrame(
        {"key": ["a", "b", "a", "b", "d"], "data2": pd.Series(range(5), dtype="Int64")}
    )
    print(df1)
    print(df2)
    print(pd.merge(df1, df2, on="key", how="left"))
    print(pd.merge(df1, df2, how="inner"))


def explain_multiple_keys() -> None:
    """
    Problem: join on a combination of several columns.
    Why: pass a list of column names to `on` to merge on multiple keys. Think of
    the multiple keys as forming an array of tuples used as a single join key.
    """
    print("== Merging on multiple keys ==")

    left = pd.DataFrame(
        {
            "key1": ["foo", "foo", "bar"],
            "key2": ["one", "two", "one"],
            "lval": pd.Series([1, 2, 3], dtype="Int64"),
        }
    )
    right = pd.DataFrame(
        {
            "key1": ["foo", "foo", "bar", "bar"],
            "key2": ["one", "one", "one", "two"],
            "rval": pd.Series([4, 5, 6, 7], dtype="Int64"),
        }
    )
    print(pd.merge(left, right, on=["key1", "key2"], how="outer"))


def explain_suffixes() -> None:
    """
    Problem: disambiguate columns that overlap (other than the join keys).
    Why: when both frames carry a same-named non-key column, merge appends "_x"
    and "_y" by default; the `suffixes` option lets you choose those strings.
    """
    print("== Overlapping column names (suffixes) ==")

    left = pd.DataFrame(
        {
            "key1": ["foo", "foo", "bar"],
            "key2": ["one", "two", "one"],
            "lval": pd.Series([1, 2, 3], dtype="Int64"),
        }
    )
    right = pd.DataFrame(
        {
            "key1": ["foo", "foo", "bar", "bar"],
            "key2": ["one", "one", "one", "two"],
            "rval": pd.Series([4, 5, 6, 7], dtype="Int64"),
        }
    )
    # Only key1 is a join key, so key2 overlaps and gets a suffix.
    print(pd.merge(left, right, on="key1"))
    print(pd.merge(left, right, on="key1", suffixes=("_left", "_right")))


def explain_merge_on_index() -> None:
    """
    Problem: join when the merge key lives in a DataFrame's row index.
    Why: pass `left_index=True` and/or `right_index=True` so merge uses the index
    as the key. With a hierarchically indexed frame, joining on the index is
    equivalent to a multiple-key merge (pass a list to `left_on`). The index of
    both sides can be used at once with both flags True.
    """
    print("== Merging on the index (left_index/right_index) ==")

    left1 = pd.DataFrame(
        {"key": ["a", "b", "a", "a", "b", "c"], "value": pd.Series(range(6), dtype="Int64")}
    )
    right1 = pd.DataFrame({"group_val": [3.5, 7]}, index=["a", "b"])
    print(left1)
    print(right1)
    # Join left1's "key" column against right1's index.
    print(pd.merge(left1, right1, left_on="key", right_index=True))
    print(pd.merge(left1, right1, left_on="key", right_index=True, how="outer"))

    # Hierarchically indexed right side -> multiple-key merge.
    lefth = pd.DataFrame(
        {
            "key1": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada"],
            "key2": [2000, 2001, 2002, 2001, 2002],
            "data": pd.Series(range(5), dtype="Int64"),
        }
    )
    righth_index = pd.MultiIndex.from_arrays(
        [
            ["Nevada", "Nevada", "Ohio", "Ohio", "Ohio", "Ohio"],
            [2001, 2000, 2000, 2000, 2001, 2002],
        ]
    )
    righth = pd.DataFrame(
        {
            "event1": pd.Series([0, 2, 4, 6, 8, 10], dtype="Int64", index=righth_index),
            "event2": pd.Series([1, 3, 5, 7, 9, 11], dtype="Int64", index=righth_index),
        }
    )
    print(pd.merge(lefth, righth, left_on=["key1", "key2"], right_index=True))
    print(
        pd.merge(lefth, righth, left_on=["key1", "key2"], right_index=True, how="outer")
    )

    # Using the indexes of BOTH frames as the join keys.
    left2 = pd.DataFrame(
        [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
        index=["a", "c", "e"],
        columns=["Ohio", "Nevada"],
    ).astype("Int64")
    right2 = pd.DataFrame(
        [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0], [13, 14]],
        index=["b", "c", "d", "e"],
        columns=["Missouri", "Alabama"],
    ).astype("Int64")
    print(pd.merge(left2, right2, how="outer", left_index=True, right_index=True))


def explain_join_method() -> None:
    """
    Problem: simplify index-on-index merges across several frames.
    Why: `DataFrame.join` performs a LEFT join on the index by default and can
    combine many frames with similar indexes but non-overlapping columns. It can
    also join the passed frame's index onto a column of the calling frame (`on=`),
    and accepts a list of frames for simple index-on-index merges.
    """
    print("== DataFrame.join (index-on-index convenience) ==")

    left1 = pd.DataFrame(
        {"key": ["a", "b", "a", "a", "b", "c"], "value": pd.Series(range(6), dtype="Int64")}
    )
    right1 = pd.DataFrame({"group_val": [3.5, 7]}, index=["a", "b"])
    left2 = pd.DataFrame(
        [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
        index=["a", "c", "e"],
        columns=["Ohio", "Nevada"],
    ).astype("Int64")
    right2 = pd.DataFrame(
        [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0], [13, 14]],
        index=["b", "c", "d", "e"],
        columns=["Missouri", "Alabama"],
    ).astype("Int64")

    # join on the index (outer keeps every label).
    print(left2.join(right2, how="outer"))
    # join the right index onto the left's "key" column.
    print(left1.join(right1, on="key"))

    # Pass a list of frames for simple index-on-index merges.
    another = pd.DataFrame(
        [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0], [16.0, 17.0]],
        index=["a", "c", "e", "f"],
        columns=["New York", "Oregon"],
    )
    print(left2.join([right2, another]))
    print(left2.join([right2, another], how="outer"))


def main() -> None:
    explain_basic_merge()
    explain_different_key_names()
    explain_how_join_types()
    explain_many_to_many()
    explain_multiple_keys()
    explain_suffixes()
    explain_merge_on_index()
    explain_join_method()


main()
