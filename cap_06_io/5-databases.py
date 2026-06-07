"""
Interacting with Databases (Section 6.4)

In a business setting, a lot of data lives in SQL relational databases (SQL Server,
PostgreSQL, MySQL, SQLite, ...). This file shows the two layers the book covers.
First, the low-level path with Python's built-in `sqlite3` driver: create a table,
insert rows with `executemany`, run a SELECT, and assemble a DataFrame by hand from
the returned tuples plus the column names in `cursor.description`. Then the
high-level path: connect to the SAME database through SQLAlchemy and let
`pd.read_sql` do all that munging in one line. The database is created inside a
temporary directory so nothing is written into the repo.

DATABASE WORKFLOW
TOOL / METHOD              DESCRIPTION
sqlite3.connect           Open a connection to a SQLite database file
con.execute               Run a single SQL statement (DDL or query)
con.executemany           Run an INSERT once per row of a sequence of params
cursor.fetchall           Retrieve all result rows as a list of tuples
cursor.description        Column metadata; element [0] of each is the column name
sqlalchemy.create_engine  Build a SQLAlchemy engine from a connection URL
pd.read_sql               Read a SQL query's results straight into a DataFrame

Run:
    poetry run python cap_06_io/5-databases.py
"""

import sqlite3
import tempfile
from pathlib import Path

import pandas as pd
import sqlalchemy as sqla


def explain_sqlite3_driver(db_path: str) -> None:
    """
    Problem: create a SQLite table, insert rows, and turn a SELECT into a DataFrame
    using only the stdlib driver.
    Why: most Python SQL drivers return query results as a list of tuples with no
    column names attached. The column names live in `cursor.description` (for
    SQLite, only the name field is populated). Combining the rows with those names
    feeds the DataFrame constructor.
    """
    print("== Low-level access with the sqlite3 driver ==")

    # Create a table with mixed column types.
    query = """
    CREATE TABLE test
    (a VARCHAR(20), b VARCHAR(20),
     c REAL,        d INTEGER
    );"""
    con = sqlite3.connect(db_path)
    con.execute(query)
    con.commit()

    # Insert a few rows with executemany and a parameterized statement.
    data = [
        ("Atlanta", "Georgia", 1.25, 6),
        ("Tallahassee", "Florida", 2.6, 3),
        ("Sacramento", "California", 1.7, 5),
    ]
    stmt = "INSERT INTO test VALUES(?, ?, ?, ?)"
    con.executemany(stmt, data)
    con.commit()

    # SELECT returns a list of tuples (no column names attached).
    cursor = con.execute("SELECT * FROM test")
    rows = cursor.fetchall()
    print(rows)

    # cursor.description holds the column metadata; [0] of each is the name.
    print(cursor.description)
    frame = pd.DataFrame(rows, columns=[x[0] for x in cursor.description])
    print(frame)

    con.close()


def explain_sqlalchemy_read_sql(db_path: str) -> None:
    """
    Problem: avoid repeating the tuple-and-columns munging on every query.
    Why: SQLAlchemy abstracts away differences between databases, and pandas'
    `read_sql` reads a query's results directly into a DataFrame over a SQLAlchemy
    connection — replacing all the manual work above with a single call.
    """
    print("== High-level access with SQLAlchemy + read_sql ==")

    # Connect to the SAME SQLite file created above (sqlite:/// + absolute path).
    db = sqla.create_engine(f"sqlite:///{db_path}")
    print(pd.read_sql("SELECT * FROM test", db))
    db.dispose()


def main() -> None:
    # One temporary directory shared by both demos; cleaned up on exit.
    with tempfile.TemporaryDirectory() as tmp:
        db_path = str(Path(tmp) / "mydata.sqlite")
        explain_sqlite3_driver(db_path)
        explain_sqlalchemy_read_sql(db_path)


main()
