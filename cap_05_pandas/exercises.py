"""
pandas: Practice Exercises

A hands-on set of original exercises covering the pandas fundamentals from this
chapter: building a Series and a DataFrame, inspecting them, selecting columns and
rows with [], .loc and .iloc, boolean filtering, deriving and dropping columns,
handling missing data, sorting and ranking, grouping with aggregation, counting
unique values, merging frames, applying functions over a column, and reshaping
with a pivot table. Each exercise is self-contained and deterministic: the small
DataFrames are written inline, and any randomness uses a seeded generator.

Run:
    poetry run python cap_05_pandas/exercises.py
"""

import numpy as np
import pandas as pd


def exercise_01() -> None:
    """
    Exercise 1: Create a Series

    Problem: Build a Series of three city temperatures (in Celsius) with the city
    names as the index, then print the value for one city by label.

    Expected result: A labeled Series and the temperature for "Oslo" (4).
    """
    # A Series pairs values with an explicit index of labels.
    temps = pd.Series([4, 22, 17], index=["Oslo", "Madrid", "Tokyo"])
    print(temps)
    # Label-based access reads the value tied to "Oslo".
    print(f"Oslo: {temps['Oslo']}")


def exercise_02() -> None:
    """
    Exercise 2: Create a DataFrame from a dict

    Problem: Build a DataFrame of four products with columns "product", "price"
    and "stock" from a dict of equal-length lists.

    Expected result: A 4-row, 3-column table with a default RangeIndex.
    """
    # Each dict key becomes a column; values must share the same length.
    data = {
        "product": ["Pen", "Notebook", "Eraser", "Marker"],
        "price": [1.5, 3.0, 0.8, 2.2],
        "stock": [120, 45, 200, 60],
    }
    df = pd.DataFrame(data)
    print(df)
    print(f"shape: {df.shape}")


def exercise_03() -> None:
    """
    Exercise 3: Inspect a DataFrame

    Problem: For a small sales table, print the first two rows, the column dtypes,
    and the numeric summary from describe().

    Expected result: head(2), the per-column dtypes, and describe() statistics.
    """
    df = pd.DataFrame(
        {
            "city": ["Lima", "Quito", "Bogota", "La Paz", "Cusco"],
            "units": [30, 18, 42, 9, 25],
            "revenue": [300.0, 180.0, 420.0, 90.0, 250.0],
        }
    )
    # head(n) returns the leading n rows for a quick look.
    print(df.head(2))
    # dtypes reports the resolved type of each column.
    print(df.dtypes)
    # describe() summarizes the numeric columns (count, mean, std, quartiles).
    print(df.describe())


def exercise_04() -> None:
    """
    Exercise 4: Select columns

    Problem: From an employee table, select the single "name" column (as a Series)
    and the pair ["name", "salary"] (as a DataFrame).

    Expected result: A Series of names and a 2-column DataFrame.
    """
    df = pd.DataFrame(
        {
            "name": ["Ana", "Beto", "Cora"],
            "dept": ["IT", "HR", "IT"],
            "salary": [5200, 4100, 6000],
        }
    )
    # A single string returns one column as a Series.
    print(df["name"])
    # A list of strings returns those columns as a DataFrame.
    print(df[["name", "salary"]])


def exercise_05() -> None:
    """
    Exercise 5: Select rows with .loc and .iloc

    Problem: Using a DataFrame indexed by student id, fetch the row for id "s2"
    by label and the third row by position.

    Expected result: The same row reached two different ways.
    """
    df = pd.DataFrame(
        {"grade": [88, 73, 95], "subject": ["math", "art", "music"]},
        index=["s1", "s2", "s3"],
    )
    # .loc selects by the index label.
    print(df.loc["s2"])
    # .iloc selects by integer position (0-based), so position 2 is the third row.
    print(df.iloc[2])


def exercise_06() -> None:
    """
    Exercise 6: Boolean filtering

    Problem: From an orders table, keep only the rows whose "amount" is greater
    than 100.

    Expected result: The subset of rows that satisfy the condition.
    """
    df = pd.DataFrame(
        {
            "order": ["A", "B", "C", "D"],
            "amount": [50, 150, 99, 230],
        }
    )
    # A comparison produces a boolean mask aligned to the rows.
    mask = df["amount"] > 100
    # Indexing with the mask keeps only the True rows.
    print(df[mask])


def exercise_07() -> None:
    """
    Exercise 7: Add and derive a column

    Problem: Given quantity and unit_price columns, add a "total" column equal to
    quantity * unit_price.

    Expected result: The table with the new derived column.
    """
    df = pd.DataFrame(
        {
            "item": ["chair", "table", "lamp"],
            "quantity": [4, 1, 3],
            "unit_price": [25.0, 120.0, 15.0],
        }
    )
    # Column arithmetic is vectorized and aligns element-wise by row.
    # Under Copy-on-Write, assign through .loc to write into the frame.
    df.loc[:, "total"] = df["quantity"] * df["unit_price"]
    print(df)


def exercise_08() -> None:
    """
    Exercise 8: Drop a column

    Problem: Remove the temporary "scratch" column from the table.

    Expected result: The table without the dropped column.
    """
    df = pd.DataFrame(
        {
            "name": ["x", "y", "z"],
            "value": [1, 2, 3],
            "scratch": [9, 9, 9],
        }
    )
    # drop with axis="columns" returns a new frame without "scratch".
    cleaned = df.drop(columns="scratch")
    print(cleaned)


def exercise_09() -> None:
    """
    Exercise 9: Detect and drop missing data

    Problem: A table has some missing values. Print the per-cell isna() mask, then
    drop every row that contains at least one missing value.

    Expected result: The boolean mask and the rows with no NaN.
    """
    df = pd.DataFrame(
        {
            "name": ["Ada", "Ben", "Cy", "Deb"],
            "score": [10.0, np.nan, 7.0, 4.0],
            "age": [21, 25, np.nan, 30],
        }
    )
    # isna() flags missing entries cell by cell.
    print(df.isna())
    # dropna() removes any row holding at least one NaN.
    print(df.dropna())


def exercise_10() -> None:
    """
    Exercise 10: Fill missing data

    Problem: Replace the missing values in the "qty" column with that column's
    mean, leaving the other columns untouched.

    Expected result: The table with "qty" gaps filled by the column mean.
    """
    df = pd.DataFrame(
        {
            "store": ["N", "S", "E", "W"],
            "qty": [10.0, np.nan, 30.0, np.nan],
        }
    )
    # The mean ignores NaN by default, giving a representative fill value.
    mean_qty = df["qty"].mean()
    # Assign the filled column back through .loc (Copy-on-Write friendly).
    df.loc[:, "qty"] = df["qty"].fillna(mean_qty)
    print(df)


def exercise_11() -> None:
    """
    Exercise 11: Sort by values

    Problem: Sort a table of mountains by "height" in descending order.

    Expected result: Rows ordered from tallest to shortest.
    """
    df = pd.DataFrame(
        {
            "mountain": ["Aconcagua", "Denali", "Elbrus", "Kilimanjaro"],
            "height": [6961, 6190, 5642, 5895],
        }
    )
    # sort_values with ascending=False puts the largest height first.
    print(df.sort_values("height", ascending=False))


def exercise_12() -> None:
    """
    Exercise 12: Rank a column

    Problem: Add a "rank" column that ranks players by "points", where rank 1 is
    the highest score.

    Expected result: The table with a competition-style rank per player.
    """
    df = pd.DataFrame(
        {
            "player": ["P1", "P2", "P3", "P4"],
            "points": [40, 75, 75, 20],
        }
    )
    # rank(ascending=False) gives rank 1 to the top score; method="min" assigns
    # tied values the same (lowest) rank.
    df.loc[:, "rank"] = df["points"].rank(ascending=False, method="min")
    print(df)


def exercise_13() -> None:
    """
    Exercise 13: Group and aggregate

    Problem: For a table of sales by region, compute the total and mean "amount"
    per region in a single grouped aggregation.

    Expected result: One row per region with its sum and mean.
    """
    df = pd.DataFrame(
        {
            "region": ["N", "S", "N", "S", "N"],
            "amount": [100, 200, 150, 50, 250],
        }
    )
    # groupby splits rows by region; agg applies several functions at once.
    summary = df.groupby("region")["amount"].agg(["sum", "mean"])
    print(summary)


def exercise_14() -> None:
    """
    Exercise 14: Count unique values

    Problem: From a column of survey answers, print how many times each distinct
    answer appears and the list of distinct answers.

    Expected result: value_counts() tallies and the unique() array.
    """
    answers = pd.Series(["yes", "no", "yes", "maybe", "yes", "no"])
    # value_counts() is a Series method; it tallies each distinct value.
    print(answers.value_counts())
    # unique() returns the distinct values in first-seen order.
    print(answers.unique())


def exercise_15() -> None:
    """
    Exercise 15: Merge two DataFrames

    Problem: Join an orders table with a customers table on the shared "cust_id"
    key so each order gains the customer's name.

    Expected result: One combined table aligning orders to customer names.
    """
    orders = pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "cust_id": ["c1", "c2", "c1"],
            "total": [30, 45, 12],
        }
    )
    customers = pd.DataFrame(
        {
            "cust_id": ["c1", "c2"],
            "name": ["Mara", "Nil"],
        }
    )
    # merge performs a relational join on the common key column.
    joined = orders.merge(customers, on="cust_id")
    print(joined)


def exercise_16() -> None:
    """
    Exercise 16: Apply and map over a column

    Problem: Using map, add a "bonus" column equal to 10% of each salary, and
    classify each salary as "high" or "low" with apply against a threshold.

    Expected result: The table with a numeric bonus and a categorical tier.
    """
    df = pd.DataFrame(
        {
            "name": ["Ivy", "Jon", "Kai"],
            "salary": [3000, 8000, 5000],
        }
    )
    # Series.map applies an element-wise function and returns a new Series.
    df.loc[:, "bonus"] = df["salary"].map(lambda s: round(s * 0.10, 2))
    # apply over a Series also works element-wise here, returning a label per row.
    df.loc[:, "tier"] = df["salary"].apply(lambda s: "high" if s >= 5000 else "low")
    print(df)


def exercise_17() -> None:
    """
    Exercise 17: Pivot table

    Problem: From a long table of sales (region x quarter), reshape it into a
    pivot table with regions as rows, quarters as columns, and summed sales as
    the values.

    Expected result: A wide region-by-quarter matrix of summed sales.
    """
    df = pd.DataFrame(
        {
            "region": ["N", "N", "S", "S", "N"],
            "quarter": ["Q1", "Q2", "Q1", "Q2", "Q1"],
            "sales": [100, 120, 80, 90, 50],
        }
    )
    # pivot_table reshapes long data to wide, aggregating duplicates with aggfunc.
    table = df.pivot_table(
        index="region", columns="quarter", values="sales", aggfunc="sum"
    )
    print(table)


def exercise_18() -> None:
    """
    Exercise 18: Random sample with a seed

    Problem: Build a DataFrame of 6 random integer readings using a seeded
    generator, then report the count of readings above the column mean.

    Expected result: A deterministic table and how many readings exceed the mean.
    """
    # A seeded generator makes the "random" data reproducible across runs.
    rng = np.random.default_rng(seed=42)
    df = pd.DataFrame({"reading": rng.integers(low=0, high=100, size=6)})
    threshold = df["reading"].mean()
    # The boolean mask sums to the number of True values.
    above = int((df["reading"] > threshold).sum())
    print(df)
    print(f"mean: {threshold}, above mean: {above}")


def main() -> None:
    print("=== Exercise 1: Create a Series ===")
    exercise_01()

    print("\n=== Exercise 2: Create a DataFrame from a dict ===")
    exercise_02()

    print("\n=== Exercise 3: Inspect a DataFrame ===")
    exercise_03()

    print("\n=== Exercise 4: Select columns ===")
    exercise_04()

    print("\n=== Exercise 5: Select rows with .loc and .iloc ===")
    exercise_05()

    print("\n=== Exercise 6: Boolean filtering ===")
    exercise_06()

    print("\n=== Exercise 7: Add and derive a column ===")
    exercise_07()

    print("\n=== Exercise 8: Drop a column ===")
    exercise_08()

    print("\n=== Exercise 9: Detect and drop missing data ===")
    exercise_09()

    print("\n=== Exercise 10: Fill missing data ===")
    exercise_10()

    print("\n=== Exercise 11: Sort by values ===")
    exercise_11()

    print("\n=== Exercise 12: Rank a column ===")
    exercise_12()

    print("\n=== Exercise 13: Group and aggregate ===")
    exercise_13()

    print("\n=== Exercise 14: Count unique values ===")
    exercise_14()

    print("\n=== Exercise 15: Merge two DataFrames ===")
    exercise_15()

    print("\n=== Exercise 16: Apply and map over a column ===")
    exercise_16()

    print("\n=== Exercise 17: Pivot table ===")
    exercise_17()

    print("\n=== Exercise 18: Random sample with a seed ===")
    exercise_18()


main()
