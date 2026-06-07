"""
Join, Combine & Reshape: Practice Exercises

Combining and reshaping data is where real analysis begins: information arrives
split across files, stored under different column names, or laid out in a shape
that fights the question you want to ask. These exercises practice the pandas
tools for that work -- database-style joins (pd.merge and DataFrame.join),
stacking frames together (pd.concat), patching gaps from a second source
(combine_first), building hierarchical (MultiIndex) labels, and pivoting between
"long" and "wide" layouts (stack/unstack, pivot, melt). Every problem builds its
own small in-code frame so the focus stays on the operation, not the data.

Run:
    poetry run python cap_08_wrangling/exercises.py
"""

import numpy as np
import pandas as pd


def exercise_01() -> None:
    """
    Exercise 1: Inner merge on a shared key

    Problem: Two frames describe orders and customers. Join each order to its
    customer's city using the shared "customer_id" column. Only orders whose
    customer exists in both frames should survive.

    Purpose: pd.merge defaults to how="inner", keeping only keys present in BOTH
    frames -- the natural choice when a row only makes sense once enriched.

    Given Input:
        orders:    order_id / customer_id / amount
        customers: customer_id / city
    Expected Output: one row per order that has a matching customer, with city.
    """
    orders = pd.DataFrame(
        {"order_id": [1, 2, 3, 4], "customer_id": [10, 11, 10, 99], "amount": [50, 30, 80, 20]}
    )
    customers = pd.DataFrame({"customer_id": [10, 11, 12], "city": ["Lima", "Quito", "Bogota"]})
    # inner is the default: order 4 (customer 99) and customer 12 both drop out.
    merged = pd.merge(orders, customers, on="customer_id")
    print(merged)


def exercise_02() -> None:
    """
    Exercise 2: Left merge keeps every left row

    Problem: Attach each employee's department name, but keep employees even when
    their department code has no match in the lookup table.

    Purpose: how="left" preserves ALL rows of the left frame; unmatched keys get
    NaN on the right-hand columns -- the safe default when the left frame is the
    record of truth you must not lose.

    Given Input:
        employees: name / dept_code
        depts:     dept_code / dept_name
    Expected Output: every employee, with dept_name NaN where no match exists.
    """
    employees = pd.DataFrame(
        {"name": ["Ana", "Beto", "Carla"], "dept_code": ["ENG", "SALES", "X99"]}
    )
    depts = pd.DataFrame({"dept_code": ["ENG", "SALES"], "dept_name": ["Engineering", "Sales"]})
    # "Carla" has dept_code X99 with no match -> kept, dept_name becomes NaN.
    merged = pd.merge(employees, depts, on="dept_code", how="left")
    print(merged)


def exercise_03() -> None:
    """
    Exercise 3: Right and outer merges

    Problem: Given product prices and a (partial) stock count, show (a) a right
    merge that keeps every priced product, and (b) an outer merge that keeps the
    union of all product ids from both frames.

    Purpose: how="right" mirrors "left" toward the right frame; how="outer" keeps
    the UNION of keys, filling gaps on either side with NaN. Together they round
    out the four join directions.

    Given Input:
        prices: product / price
        stock:  product / units
    Expected Output: the right-merge result, then the outer-merge result.
    """
    prices = pd.DataFrame({"product": ["pen", "pad", "ink"], "price": [2.0, 5.0, 9.0]})
    stock = pd.DataFrame({"product": ["pad", "ink", "clip"], "units": [40, 0, 100]})
    # right: keep every row of `stock` (the right frame); "pen" drops out.
    right = pd.merge(prices, stock, on="product", how="right")
    # outer: keep the union -> pen, pad, ink, clip all appear.
    outer = pd.merge(prices, stock, on="product", how="outer")
    print("right merge:")
    print(right)
    print("\nouter merge:")
    print(outer)


def exercise_04() -> None:
    """
    Exercise 4: Merge on multiple keys

    Problem: Join daily sales to a targets table where a row is identified by the
    COMBINATION of "region" and "quarter", not by either alone.

    Purpose: When no single column is a unique identifier, pass a list to `on`.
    pandas matches on the tuple of all listed columns at once.

    Given Input:
        sales:   region / quarter / revenue
        targets: region / quarter / goal
    Expected Output: rows aligned on the (region, quarter) pair.
    """
    sales = pd.DataFrame(
        {
            "region": ["N", "N", "S", "S"],
            "quarter": ["Q1", "Q2", "Q1", "Q2"],
            "revenue": [100, 120, 90, 95],
        }
    )
    targets = pd.DataFrame(
        {"region": ["N", "N", "S", "S"], "quarter": ["Q1", "Q2", "Q1", "Q2"], "goal": [110, 110, 80, 100]}
    )
    # the key is the pair (region, quarter); pass both column names as a list.
    merged = pd.merge(sales, targets, on=["region", "quarter"])
    print(merged)


def exercise_05() -> None:
    """
    Exercise 5: Overlapping column names and suffixes

    Problem: Both frames carry a "score" column that means different things
    (an exam score vs a review score). Merge on "student" and disambiguate the
    two columns.

    Purpose: When non-key columns collide, pandas appends suffixes. The defaults
    ("_x", "_y") are cryptic, so pass `suffixes` to give them meaningful names.

    Given Input:
        exams:   student / score
        reviews: student / score
    Expected Output: one row per student with score_exam and score_review.
    """
    exams = pd.DataFrame({"student": ["A", "B", "C"], "score": [88, 72, 95]})
    reviews = pd.DataFrame({"student": ["A", "B", "C"], "score": [4, 5, 3]})
    # both have "score"; rename the clashing columns via suffixes for clarity.
    merged = pd.merge(exams, reviews, on="student", suffixes=("_exam", "_review"))
    print(merged)


def exercise_06() -> None:
    """
    Exercise 6: Merge on the index

    Problem: A frame of monthly revenue is indexed by month code. A separate
    frame of expenses is ALSO indexed by month code. Combine them by index.

    Purpose: When the join keys live in the index rather than a column, set
    left_index=True and right_index=True so merge aligns on the labels directly.

    Given Input:
        revenue (index=month): revenue
        expense (index=month): expense
    Expected Output: a frame aligned on the month index with both columns.
    """
    revenue = pd.DataFrame({"revenue": [200, 250, 300]}, index=["jan", "feb", "mar"])
    expense = pd.DataFrame({"expense": [120, 130, 160]}, index=["jan", "feb", "mar"])
    # no key columns -> align on the index of both sides.
    merged = pd.merge(revenue, expense, left_index=True, right_index=True)
    print(merged)


def exercise_07() -> None:
    """
    Exercise 7: DataFrame.join for index-aligned frames

    Problem: Combine three index-aligned frames (height, weight, age), each keyed
    by person name, into a single profile table.

    Purpose: DataFrame.join is the concise shortcut for index-on-index merges and
    accepts a LIST of frames, joining them all in one call -- cleaner than chaining
    several pd.merge calls.

    Given Input:
        three frames indexed by name, one column each.
    Expected Output: a single frame with height, weight, age columns.
    """
    height = pd.DataFrame({"height": [170, 165, 180]}, index=["Ivo", "Lena", "Marc"])
    weight = pd.DataFrame({"weight": [68, 55, 80]}, index=["Ivo", "Lena", "Marc"])
    age = pd.DataFrame({"age": [30, 25, 42]}, index=["Ivo", "Lena", "Marc"])
    # join accepts a list and aligns all of them on the shared index at once.
    profile = height.join([weight, age])
    print(profile)


def exercise_08() -> None:
    """
    Exercise 8: Concatenate along rows (stacking) and columns

    Problem: Two batches of measurements share the same columns -- stack them into
    one long frame. Then take two frames sharing the same index and glue them
    side by side.

    Purpose: pd.concat with axis=0 (default) appends rows; axis=1 aligns on the
    index and appends columns. ignore_index=True renumbers the rows after a
    vertical stack so the index stays clean.

    Given Input:
        batch1, batch2: same columns (sensor / value)
        left, right:    same index, different columns
    Expected Output: the row-stacked frame, then the column-joined frame.
    """
    batch1 = pd.DataFrame({"sensor": ["s1", "s2"], "value": [10, 20]})
    batch2 = pd.DataFrame({"sensor": ["s3", "s4"], "value": [30, 40]})
    # axis=0 stacks rows; ignore_index gives a fresh 0..3 RangeIndex.
    stacked = pd.concat([batch1, batch2], ignore_index=True)

    left = pd.DataFrame({"x": [1, 2, 3]}, index=["a", "b", "c"])
    right = pd.DataFrame({"y": [4, 5, 6]}, index=["a", "b", "c"])
    # axis=1 aligns on the index and places columns side by side.
    sided = pd.concat([left, right], axis=1)

    print("row-stacked:")
    print(stacked)
    print("\ncolumn-joined:")
    print(sided)


def exercise_09() -> None:
    """
    Exercise 9: Concatenate with keys to label the source

    Problem: Combine three regional frames into one, while remembering which
    region each block of rows came from.

    Purpose: The `keys` argument of pd.concat creates an OUTER MultiIndex level
    tagging each piece. This preserves provenance so you can later slice by source
    or group on the new outer level.

    Given Input:
        north, south, east: each with column "sales"
    Expected Output: a frame whose outer index level names the source region.
    """
    north = pd.DataFrame({"sales": [10, 12]})
    south = pd.DataFrame({"sales": [7, 9]})
    east = pd.DataFrame({"sales": [5, 6]})
    # keys become an outer index level that records each block's origin.
    combined = pd.concat([north, south, east], keys=["north", "south", "east"])
    print(combined)
    # the outer level lets us pull one source back out cleanly.
    print("\njust 'south':")
    print(combined.loc["south"])


def exercise_10() -> None:
    """
    Exercise 10: Patch missing values with combine_first

    Problem: A primary readings series has gaps (NaN). A backup series has values
    for some of those gaps. Produce a series that prefers the primary value but
    falls back to the backup wherever the primary is missing.

    Purpose: combine_first aligns two objects by label and fills NaNs in the
    caller with values from the argument -- ideal for layering a fallback source
    over a preferred one without overwriting good data.

    Given Input:
        primary: index a..d with some NaN
        backup:  index a..e
    Expected Output: primary values where present, backup values for the gaps,
    plus any labels only the backup had.
    """
    primary = pd.Series([1.0, np.nan, np.nan, 4.0], index=["a", "b", "c", "d"])
    backup = pd.Series([9.0, 2.0, 3.0, 9.0, 5.0], index=["a", "b", "c", "d", "e"])
    # keep primary where it has a value; use backup only to fill the NaNs.
    patched = primary.combine_first(backup)
    print(patched)


def exercise_11() -> None:
    """
    Exercise 11: Build a MultiIndex on a Series and a DataFrame

    Problem: Create a Series whose index has two levels (city, year), then build a
    DataFrame whose ROW index also has those two levels. Read back one city's
    slice using partial indexing.

    Purpose: A MultiIndex (hierarchical index) lets several keys identify a single
    row. from_tuples is the explicit way to construct one, and partial indexing
    (.loc on the outer level) retrieves a whole sub-table at once.

    Given Input: (city, year) pairs with population values.
    Expected Output: the MultiIndexed Series, then one city's slice.
    """
    pairs = [("Lima", 2020), ("Lima", 2021), ("Oslo", 2020), ("Oslo", 2021)]
    index = pd.MultiIndex.from_tuples(pairs, names=["city", "year"])
    population = pd.Series([10.0, 10.2, 0.7, 0.7], index=index)

    frame = pd.DataFrame({"pop": [10.0, 10.2, 0.7, 0.7], "gdp": [60, 65, 40, 42]}, index=index)

    print("MultiIndexed Series:")
    print(population)
    print("\nDataFrame, partial index 'Lima':")
    # partial indexing on the outer level returns Lima's rows across years.
    print(frame.loc["Lima"])


def exercise_12() -> None:
    """
    Exercise 12: stack and unstack

    Problem: Start from a small wide frame (rows=day, columns=metric). Move the
    column labels down into the index with stack, then push them back up to
    columns with unstack.

    Purpose: stack pivots the innermost COLUMN level into a new innermost ROW
    level (wide -> long); unstack is its exact inverse (long -> wide). They are
    the lowest-level reshaping primitives that pivot/melt build on.

    Given Input: frame indexed by day with columns temp / humidity.
    Expected Output: the stacked Series, then the round-trip back to the frame.
    """
    frame = pd.DataFrame(
        {"temp": [20, 22], "humidity": [55, 60]}, index=["mon", "tue"]
    )
    # stack drops the column labels into a second index level -> a long Series.
    stacked = frame.stack()
    # unstack lifts that inner level back up into columns -> original shape.
    unstacked = stacked.unstack()
    print("stacked (long):")
    print(stacked)
    print("\nunstacked (wide again):")
    print(unstacked)


def exercise_13() -> None:
    """
    Exercise 13: pivot (long -> wide) and melt (wide -> long)

    Problem: A long "tidy" log has one row per (date, metric) observation. Pivot
    it into a wide table with one column per metric. Then melt that wide table
    back into the original long shape.

    Purpose: pivot reshapes long -> wide using one column for the new index, one
    for the new columns, and one for the values. melt is the inverse, collapsing
    several value columns into (variable, value) pairs. This pair is the everyday
    bridge between storage-friendly long data and analysis-friendly wide data.

    Given Input: long frame date / metric / value.
    Expected Output: the pivoted wide frame, then the melted long frame.
    """
    long = pd.DataFrame(
        {
            "date": ["d1", "d1", "d2", "d2"],
            "metric": ["clicks", "views", "clicks", "views"],
            "value": [3, 40, 5, 55],
        }
    )
    # pivot: date -> index, metric -> columns, value -> cells.
    wide = long.pivot(index="date", columns="metric", values="value")
    # melt: collapse the metric columns back into (metric, value) rows.
    remelted = wide.reset_index().melt(
        id_vars="date", var_name="metric", value_name="value"
    )
    print("pivoted (wide):")
    print(wide)
    print("\nmelted (long again):")
    print(remelted)


def main() -> None:
    print("=== Exercise 1: Inner merge on a shared key ===")
    exercise_01()

    print("\n=== Exercise 2: Left merge keeps every left row ===")
    exercise_02()

    print("\n=== Exercise 3: Right and outer merges ===")
    exercise_03()

    print("\n=== Exercise 4: Merge on multiple keys ===")
    exercise_04()

    print("\n=== Exercise 5: Overlapping column names and suffixes ===")
    exercise_05()

    print("\n=== Exercise 6: Merge on the index ===")
    exercise_06()

    print("\n=== Exercise 7: DataFrame.join for index-aligned frames ===")
    exercise_07()

    print("\n=== Exercise 8: Concatenate along rows and columns ===")
    exercise_08()

    print("\n=== Exercise 9: Concatenate with keys to label the source ===")
    exercise_09()

    print("\n=== Exercise 10: Patch missing values with combine_first ===")
    exercise_10()

    print("\n=== Exercise 11: Build a MultiIndex on a Series and a DataFrame ===")
    exercise_11()

    print("\n=== Exercise 12: stack and unstack ===")
    exercise_12()

    print("\n=== Exercise 13: pivot and melt ===")
    exercise_13()


main()
