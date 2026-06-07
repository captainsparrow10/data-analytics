"""
Data Loading & File Formats: Practice Exercises

Hands-on practice for Chapter 6. Each exercise states a small data-loading
problem, builds the source data in code, writes it to a file inside a temporary
directory, reads it back, and prints the result so you can check your work. The
exercises cover the round trip for the formats analysts touch daily: delimited
text (CSV with custom separators, headers, indexes, and NA sentinels), chunked
streaming aggregation, JSON in different orientations, pickle, Excel, and a
SQLite database accessed through both `sqlite3` and SQLAlchemy.

Everything happens inside a single `tempfile.TemporaryDirectory()` created in
`main()` and passed to each exercise, so running this file touches no network and
leaves nothing behind in the repository.

Run:
    poetry run python cap_06_io/exercises.py
"""

import json
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


def exercise_01(tmp: str) -> None:
    """
    Problem: write a small DataFrame to a CSV WITHOUT its row index, then read it
    back so the round trip is identity-preserving.
    Expected: the DataFrame read back equals the original (3 rows, columns
    city/temp_c/humidity), and `equals` reports True.
    """
    # Build the source data in code.
    weather = pd.DataFrame(
        {
            "city": ["Oslo", "Cairo", "Lima"],
            "temp_c": [4, 33, 19],
            "humidity": [81, 22, 74],
        }
    )

    path = Path(tmp) / "weather.csv"
    # index=False keeps the unnamed RangeIndex out of the file, so reading back
    # does not produce a spurious "Unnamed: 0" column.
    weather.to_csv(path, index=False)

    back = pd.read_csv(path)
    print(back)
    # The round trip should reproduce the original frame exactly.
    print("round trip identical:", weather.equals(back))


def exercise_02(tmp: str) -> None:
    """
    Problem: persist a DataFrame whose row labels are meaningful (an ISO code),
    then restore those labels on read instead of getting a default RangeIndex.
    Expected: the reloaded DataFrame has its index named "code" with values
    NO/EG/PE, and `index.name` prints "code".
    """
    table = pd.DataFrame(
        {"country": ["Norway", "Egypt", "Peru"], "gdp_bn": [579, 477, 268]},
        index=pd.Index(["NO", "EG", "PE"], name="code"),
    )

    path = Path(tmp) / "gdp.csv"
    # Default to_csv writes the index; the index name becomes the first header
    # cell, so index_col can re-promote it on read.
    table.to_csv(path)

    back = pd.read_csv(path, index_col="code")
    print(back)
    print("index name:", back.index.name)


def exercise_03(tmp: str) -> None:
    """
    Problem: read a pipe-delimited file that has NO header row, supplying your own
    column names.
    Expected: a DataFrame with columns sku/qty/price and 3 rows, none of the data
    rows consumed as a header.
    """
    # A pipe-separated export with no header line.
    raw = "A1|10|2.50\nB2|4|9.99\nC3|7|1.25\n"
    path = Path(tmp) / "stock.psv"
    path.write_text(raw)

    # sep="|" splits on the pipe; header=None + names assigns labels without
    # treating the first data row as the header.
    back = pd.read_csv(path, sep="|", header=None, names=["sku", "qty", "price"])
    print(back)
    print("dtypes:\n", back.dtypes)


def exercise_04(tmp: str) -> None:
    """
    Problem: a CSV uses the literal strings "?" and "missing" to mark unknown
    values; load it so those become real NaN and count the gaps per column.
    Expected: the "score" column has 1 NaN and the "note" column has 1 NaN; the
    printed per-column NaN counts are both 1.
    """
    raw = "name,score,note\nada,90,ok\nlin,?,retry\nrob,77,missing\n"
    path = Path(tmp) / "scores.csv"
    path.write_text(raw)

    # na_values extends the default sentinel set with these custom markers.
    back = pd.read_csv(path, na_values=["?", "missing"])
    print(back)
    # isna().sum() counts NaN per column after the sentinels were applied.
    print("NaN per column:\n", back.isna().sum())


def exercise_05(tmp: str) -> None:
    """
    Problem: a 5,000-row CSV is too big to load comfortably; stream it in chunks
    and accumulate the total sales per region without ever holding the whole file.
    Expected: a Series of summed "amount" grouped by "region" (4 regions), whose
    grand total equals the sum over the full frame (sanity check prints True).
    """
    # Build a moderately large frame: regions cycle, amounts grow predictably.
    n = 5000
    big = pd.DataFrame(
        {
            "region": (["north", "south", "east", "west"] * (n // 4)),
            "amount": range(1, n + 1),
        }
    )
    path = Path(tmp) / "sales.csv"
    big.to_csv(path, index=False)

    # chunksize yields TextFileReader pieces; we fold each chunk's grouped sum
    # into a running total with add(fill_value=0) so missing groups are handled.
    running = pd.Series(dtype="int64")
    for chunk in pd.read_csv(path, chunksize=1000):
        part = chunk.groupby("region")["amount"].sum()
        running = running.add(part, fill_value=0)
    running = running.sort_index()
    print(running.astype("int64"))
    # Streamed total must match a one-shot sum of the whole file. Series.sum()
    # is typed loosely, so narrow each scalar before comparing.
    # Compare the streamed total against a one-shot sum of the whole file.
    # int() accepts NumPy scalars at runtime; float() first gives pyright a
    # concrete, convertible type to satisfy its static check.
    streamed = int(float(running.sum()))
    # big["amount"] is typed broadly (could be a DataFrame); narrow to a Series.
    amount_col = big["amount"]
    assert isinstance(amount_col, pd.Series)
    full = int(float(amount_col.sum()))
    print("matches full sum:", streamed == full)


def exercise_06(tmp: str) -> None:
    """
    Problem: exchange a table with a web client that expects JSON as a LIST of row
    objects (the "records" orientation); write it, inspect the raw text, read back.
    Expected: the on-disk text is a JSON array of 3 objects, and the reloaded
    DataFrame equals the original. (We use integer quantities here: JSON has no
    decimal type, so a value like 0.3 can round-trip to 0.30000000000000004 and
    break an exact `equals` — integers avoid that float-parsing drift.)
    """
    df = pd.DataFrame(
        {"id": [1, 2, 3], "fruit": ["pear", "kiwi", "fig"], "crates": [12, 8, 3]}
    )

    path = Path(tmp) / "fruit_records.json"
    # orient="records" emits [{col: val, ...}, ...] — the most common API shape.
    df.to_json(path, orient="records")

    # Show the raw text so the structure is visible, then parse to prove shape.
    print("raw json:", path.read_text())
    print("parsed length:", len(json.loads(path.read_text())))

    back = pd.read_json(path, orient="records")
    print(back)
    print("round trip identical:", df.equals(back))


def exercise_07(tmp: str) -> None:
    """
    Problem: serialize the same table in the "columns" orientation (a dict keyed
    by column name) and reload it, preserving the row index labels.
    Expected: reloaded DataFrame has index labels r1/r2 and columns alpha/beta;
    `equals` against the original is True.
    """
    df = pd.DataFrame(
        {"alpha": [10, 20], "beta": [1.5, 2.5]},
        index=["r1", "r2"],
    )

    path = Path(tmp) / "matrix.json"
    # orient="columns" -> {col: {index: value}}, which round-trips the index too.
    df.to_json(path, orient="columns")
    print("raw json:", path.read_text())

    back = pd.read_json(path, orient="columns")
    print(back)
    print("round trip identical:", df.equals(back))


def exercise_08(tmp: str) -> None:
    """
    Problem: cache a DataFrame to disk in pandas' native binary format so dtypes
    survive exactly (no text re-inference), then reload it.
    Expected: a column declared as a pandas "category" dtype is STILL a category
    after read_pickle (text formats would lose this); the dtype print confirms it.
    """
    df = pd.DataFrame(
        {
            "grade": pd.Series(["A", "B", "A", "C"], dtype="category"),
            "points": [4.0, 3.0, 4.0, 2.0],
        }
    )

    path = Path(tmp) / "grades.pkl"
    # Pickle stores the exact in-memory objects, so dtypes are not re-guessed.
    df.to_pickle(path)

    back = pd.read_pickle(path)
    print(back)
    # The categorical dtype is preserved byte-for-byte across the round trip.
    print("grade dtype after read_pickle:", back["grade"].dtype)
    print("round trip identical:", df.equals(back))


def exercise_09(tmp: str) -> None:
    """
    Problem: write a DataFrame to a real .xlsx workbook (via openpyxl) on a named
    sheet, then read just that sheet back.
    Expected: the reloaded DataFrame (read with the first column as the index)
    equals the original; the sheet is named "Q1".
    """
    df = pd.DataFrame(
        {"product": ["pen", "mug", "cap"], "units": [120, 45, 60]},
    ).set_index("product")

    path = Path(tmp) / "report.xlsx"
    # The ExcelWriter context manager flushes/closes the workbook on exit, which
    # is how pandas 3.x persists Excel files (the old .save() is gone).
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Q1")

    # index_col=0 re-promotes the "product" column written as the first column.
    back = pd.read_excel(path, sheet_name="Q1", index_col=0)
    print(back)
    print("round trip identical:", df.equals(back))


def exercise_10(tmp: str) -> None:
    """
    Problem: persist a DataFrame to a SQLite database the LOW-LEVEL way — create a
    table and INSERT rows with the stdlib `sqlite3` driver — then run a filtered
    SELECT and load the result into a DataFrame.
    Expected: only employees in the "eng" department come back (2 rows), with
    columns name/dept/salary.
    """
    db = Path(tmp) / "company.db"
    people = [
        ("ana", "eng", 95000),
        ("bo", "sales", 70000),
        ("cy", "eng", 88000),
    ]

    # Open a connection, create the schema, and bulk-insert with executemany.
    # closing() guarantees the connection is closed; the `with conn` block only
    # commits the transaction, it does NOT close the connection on its own.
    with closing(sqlite3.connect(db)) as conn:
        conn.execute(
            "CREATE TABLE staff (name TEXT, dept TEXT, salary INTEGER)"
        )
        conn.executemany("INSERT INTO staff VALUES (?, ?, ?)", people)
        conn.commit()

        # Run a parameterized SELECT and build a DataFrame from cursor rows.
        cur = conn.execute(
            "SELECT name, dept, salary FROM staff WHERE dept = ?", ("eng",)
        )
        rows = cur.fetchall()
        # cursor.description holds the column names of the result set.
        cols = [d[0] for d in cur.description]

    result = pd.DataFrame(rows, columns=cols)
    print(result)
    print("eng rows:", len(result))


def exercise_11(tmp: str) -> None:
    """
    Problem: read an existing SQLite table the HIGH-LEVEL way — let pandas pull a
    query straight into a DataFrame over a SQLAlchemy engine.
    Expected: `read_sql` returns the rows ordered by salary descending; the top
    salary is 88000 and the DataFrame has 2 rows.
    """
    db = Path(tmp) / "company2.db"

    # Seed the database first with sqlite3 so there is something to query;
    # closing() ensures the connection is released before SQLAlchemy opens it.
    with closing(sqlite3.connect(db)) as conn:
        conn.execute("CREATE TABLE staff (name TEXT, dept TEXT, salary INTEGER)")
        conn.executemany(
            "INSERT INTO staff VALUES (?, ?, ?)",
            [("ana", "eng", 95000), ("cy", "eng", 88000)],
        )
        conn.commit()

    # A SQLAlchemy engine is the connectable pandas prefers for read_sql.
    engine = create_engine(f"sqlite:///{db}")
    with engine.connect() as conn:
        result = pd.read_sql(
            "SELECT name, salary FROM staff ORDER BY salary DESC", conn
        )
    engine.dispose()

    print(result)
    print("top salary:", int(result["salary"].iloc[0]), "| rows:", len(result))


def exercise_12(tmp: str) -> None:
    """
    Problem: round-trip a whole DataFrame through SQLAlchemy using the high-level
    `to_sql` writer and `read_sql_table` reader (no hand-written SQL at all).
    Expected: the table read back has the same shape and values as the original
    inventory frame; `equals` reports True after aligning the index.
    """
    inventory = pd.DataFrame(
        {"item": ["bolt", "nut", "washer"], "count": [500, 480, 1200]}
    )

    db = Path(tmp) / "warehouse.db"
    engine = create_engine(f"sqlite:///{db}")

    # to_sql creates the table and writes the rows; index=False avoids storing
    # the RangeIndex as a column we would have to strip on read.
    inventory.to_sql("inventory", engine, index=False, if_exists="replace")

    # read_sql_table loads the named table whole, no query string needed.
    back = pd.read_sql_table("inventory", engine)
    engine.dispose()

    print(back)
    print("round trip identical:", inventory.equals(back))


def main() -> None:
    # One temporary directory for the whole run; removed automatically on exit so
    # nothing is left in the repository.
    with tempfile.TemporaryDirectory() as tmp:
        print("== Exercise 01: write/read CSV without the index ==")
        exercise_01(tmp)
        print("\n== Exercise 02: preserve a named index via index_col ==")
        exercise_02(tmp)
        print("\n== Exercise 03: headerless pipe-delimited file with names ==")
        exercise_03(tmp)
        print("\n== Exercise 04: custom na_values -> count missing ==")
        exercise_04(tmp)
        print("\n== Exercise 05: chunked read with streaming aggregation ==")
        exercise_05(tmp)
        print("\n== Exercise 06: JSON 'records' orientation round trip ==")
        exercise_06(tmp)
        print("\n== Exercise 07: JSON 'columns' orientation round trip ==")
        exercise_07(tmp)
        print("\n== Exercise 08: pickle preserves categorical dtype ==")
        exercise_08(tmp)
        print("\n== Exercise 09: write/read an Excel sheet (openpyxl) ==")
        exercise_09(tmp)
        print("\n== Exercise 10: SQLite via sqlite3 (CREATE/INSERT/SELECT) ==")
        exercise_10(tmp)
        print("\n== Exercise 11: read_sql over a SQLAlchemy engine ==")
        exercise_11(tmp)
        print("\n== Exercise 12: to_sql / read_sql_table round trip ==")
        exercise_12(tmp)


main()
