"""
Reading and Writing Data in Text Format (Section 6.1)

Reading data and making it accessible (called *data loading*) is the necessary
first step for most analysis. pandas features a family of functions for reading
tabular text data into a DataFrame, with `read_csv` being the most frequently
used. These functions perform *type inference*: because column data types are not
part of the text format, pandas guesses whether each column is numeric, integer,
Boolean, or string. This file reproduces the book's `examples/` CSV files inside a
temporary directory (so it runs offline and leaves the repo clean), then covers
the key `read_csv` options, reading large files in pieces, writing with `to_csv`,
and the stdlib `csv` module for other delimited formats.

SOME pandas.read_csv ARGUMENTS
ARGUMENT          DESCRIPTION
path              Filesystem location, URL, or file-like object to read from
sep / delimiter   Character sequence or regex used to split fields in each row
header            Row number to use as column names; None if there is no header
index_col         Column number(s)/name(s) to use as the row index in the result
names             List of column names for the result
skiprows          Number of rows, or list of row numbers, to skip at the start
na_values         Sequence of values to treat as NA (added to the defaults)
keep_default_na   Whether to use the default NA value list (True by default)
nrows             Number of rows to read from the start of the file
chunksize         Size of file chunks for iteration (returns a TextFileReader)

Run:
    poetry run python cap_06_io/1-reading-writing-text.py
"""

import csv
import sys
import tempfile
from pathlib import Path

import pandas as pd


def explain_read_csv_basics() -> None:
    """
    Problem: read a comma-separated file into a DataFrame and handle a missing
    header row.
    Why: `read_csv` defaults to a comma delimiter and treats the first row as the
    header. When a file has no header, pass `header=None` to let pandas assign
    default integer column names, or `names=[...]` to supply your own. `index_col`
    promotes a column to the row index (by name or position).
    """
    print("== read_csv: header, names, index_col ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)

        # ex1.csv HAS a header row; comma-delimited.
        (examples / "ex1.csv").write_text(
            "a,b,c,d,message\n"
            "1,2,3,4,hello\n"
            "5,6,7,8,world\n"
            "9,10,11,12,foo\n"
        )
        df = pd.read_csv(examples / "ex1.csv")
        print(df)

        # ex2.csv has NO header row.
        (examples / "ex2.csv").write_text(
            "1,2,3,4,hello\n5,6,7,8,world\n9,10,11,12,foo\n"
        )
        # Let pandas assign default column names...
        print(pd.read_csv(examples / "ex2.csv", header=None))
        # ...or specify the names yourself.
        names = ["a", "b", "c", "d", "message"]
        print(pd.read_csv(examples / "ex2.csv", names=names))
        # Make the "message" column the index of the returned DataFrame.
        print(pd.read_csv(examples / "ex2.csv", names=names, index_col="message"))

        # A hierarchical index is formed by passing a list of columns.
        (examples / "csv_mindex.csv").write_text(
            "key1,key2,value1,value2\n"
            "one,a,1,2\n"
            "one,b,3,4\n"
            "one,c,5,6\n"
            "one,d,7,8\n"
            "two,a,9,10\n"
            "two,b,11,12\n"
            "two,c,13,14\n"
            "two,d,15,16\n"
        )
        parsed = pd.read_csv(examples / "csv_mindex.csv", index_col=["key1", "key2"])
        print(parsed)


def explain_whitespace_and_skiprows() -> None:
    """
    Problem: read a table separated by a variable amount of whitespace, and skip
    junk rows scattered through a file.
    Why: when fields are separated by irregular whitespace, pass a regular
    expression as `sep` (here ``\\s+``). With one fewer column name than data
    columns, pandas infers the first column is the index. `skiprows` drops
    specific rows (e.g. comments) by their position.
    """
    print("== Whitespace delimiter (regex sep) and skiprows ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)

        (examples / "ex3.txt").write_text(
            "            A         B         C\n"
            "aaa -0.264438 -1.026059 -0.619500\n"
            "bbb  0.927272  0.302904 -0.032399\n"
            "ccc -0.264273 -0.386314 -0.217601\n"
            "ddd -0.871858 -0.348382  1.100491\n"
        )
        # Fields are split on runs of whitespace; the lone-extra data column
        # becomes the index automatically.
        result = pd.read_csv(examples / "ex3.txt", sep=r"\s+")
        print(result)

        (examples / "ex4.csv").write_text(
            "# hey!\n"
            "a,b,c,d,message\n"
            "# just wanted to make things more difficult for you\n"
            "# who reads CSV files with computers, anyway?\n"
            "1,2,3,4,hello\n"
            "5,6,7,8,world\n"
            "9,10,11,12,foo\n"
        )
        # Skip the first, third, and fourth rows (0-based) to drop the comments.
        print(pd.read_csv(examples / "ex4.csv", skiprows=[0, 2, 3]))


def explain_missing_values() -> None:
    """
    Problem: control how sentinel placeholders are recognized as missing data.
    Why: by default pandas maps a set of common sentinels (empty string, NA, NULL)
    to NaN. `na_values` adds extra strings to that set; `keep_default_na=False`
    turns the defaults off so ONLY your sentinels count; a dict targets different
    sentinels per column.
    """
    print("== na_values, keep_default_na, per-column sentinels ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)
        (examples / "ex5.csv").write_text(
            "something,a,b,c,d,message\n"
            "one,1,2,3,4,NA\n"
            "two,5,6,,8,world\n"
            "three,9,10,11,12,foo\n"
        )
        result = pd.read_csv(examples / "ex5.csv")
        print(result)
        print(pd.isna(result))  # empty field and "NA" both became NaN

        # Add "NULL" to the list of strings recognized as missing.
        print(pd.read_csv(examples / "ex5.csv", na_values=["NULL"]))

        # Disable the default NA sentinels entirely.
        result2 = pd.read_csv(examples / "ex5.csv", keep_default_na=False)
        print(result2)
        print(result2.isna())

        # Only treat "NA" as missing, nothing else.
        result3 = pd.read_csv(
            examples / "ex5.csv", keep_default_na=False, na_values=["NA"]
        )
        print(result3.isna())

        # Different NA sentinels per column, via a dict.
        sentinels = {"message": ["foo", "NA"], "something": ["two"]}
        print(
            pd.read_csv(
                examples / "ex5.csv", na_values=sentinels, keep_default_na=False
            )
        )


def explain_reading_in_pieces() -> None:
    """
    Problem: process a large file without loading it all into memory at once.
    Why: `nrows` reads only the first N rows. `chunksize` returns a
    TextFileReader you can iterate over, yielding DataFrame pieces of that size —
    ideal for streaming aggregations on files too big for RAM.
    """
    print("== Reading text files in pieces (nrows, chunksize) ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)

        # Build a moderately large CSV with a categorical "key" column.
        rng = pd.Series(list("LBGRQ") * 2000)
        big = pd.DataFrame(
            {
                "one": range(10000),
                "key": rng,
            }
        )
        big.to_csv(examples / "ex6.csv", index=False)

        # Read only the first 5 rows.
        print(pd.read_csv(examples / "ex6.csv", nrows=5))

        # chunksize returns a TextFileReader to iterate over.
        chunker = pd.read_csv(examples / "ex6.csv", chunksize=1000)
        print(type(chunker))  # pandas.io.parsers.readers.TextFileReader

        # Aggregate value counts of "key" across all chunks.
        tot = pd.Series([], dtype="int64")
        for piece in chunker:
            tot = tot.add(piece["key"].value_counts(), fill_value=0)
        tot = tot.sort_values(ascending=False)
        print(tot)


def explain_writing_to_csv() -> None:
    """
    Problem: export a DataFrame back to delimited text with full control.
    Why: `to_csv` writes row and column labels by default; `sep` changes the
    delimiter, `na_rep` substitutes a string for missing values, and
    `index=False`/`header=False`/`columns=[...]` control which labels and columns
    are written and in what order. Writing to `sys.stdout` previews the text.
    """
    print("== Writing data with to_csv ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)
        (examples / "ex5.csv").write_text(
            "something,a,b,c,d,message\n"
            "one,1,2,3,4,NA\n"
            "two,5,6,,8,world\n"
            "three,9,10,11,12,foo\n"
        )
        data = pd.read_csv(examples / "ex5.csv")

        # Write to a file, then read the raw text back to show the output.
        data.to_csv(examples / "out.csv")
        print((examples / "out.csv").read_text())

        # Use a different delimiter (printed to stdout, not a file).
        data.to_csv(sys.stdout, sep="|")
        # Denote missing values with a sentinel string.
        data.to_csv(sys.stdout, na_rep="NULL")
        # Disable both row and column labels.
        data.to_csv(sys.stdout, index=False, header=False)
        # Write only a subset of columns, in a chosen order.
        data.to_csv(sys.stdout, index=False, columns=["a", "b", "c"])


def explain_csv_module() -> None:
    """
    Problem: parse and write a single-character-delimited file with the stdlib
    `csv` module, including a custom dialect.
    Why: for files with one or more malformed lines that trip up `read_csv`, the
    built-in `csv` module gives line-by-line control. `csv.reader` yields lists
    of fields; a `csv.Dialect` subclass bundles delimiter/quoting/line-terminator
    options; `csv.writer` emits rows using the same dialect.
    """
    print("== Other delimited formats with the csv module ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)
        (examples / "ex7.csv").write_text('"a","b","c"\n"1","2","3"\n"1","2","3"\n')

        # Iterating a csv.reader yields lists with quote characters removed.
        with open(examples / "ex7.csv") as f:
            for line in csv.reader(f):
                print(line)

        # Read all lines, then split header from data and build a column dict.
        with open(examples / "ex7.csv") as f:
            lines = list(csv.reader(f))
        header, values = lines[0], lines[1:]
        # zip(*values) transposes rows into columns.
        data_dict = {h: v for h, v in zip(header, zip(*values))}
        print(data_dict)

        # Define a custom dialect: semicolon delimiter, minimal quoting.
        class my_dialect(csv.Dialect):
            lineterminator = "\n"
            delimiter = ";"
            quotechar = '"'
            quoting = csv.QUOTE_MINIMAL

        # Write delimited files manually with csv.writer using the dialect.
        out_path = examples / "mydata.csv"
        with open(out_path, "w") as f:
            writer = csv.writer(f, dialect=my_dialect)
            writer.writerow(("one", "two", "three"))
            writer.writerow(("1", "2", "3"))
            writer.writerow(("4", "5", "6"))
            writer.writerow(("7", "8", "9"))
        print(out_path.read_text())


def main() -> None:
    explain_read_csv_basics()
    explain_whitespace_and_skiprows()
    explain_missing_values()
    explain_reading_in_pieces()
    explain_writing_to_csv()
    explain_csv_module()


main()
