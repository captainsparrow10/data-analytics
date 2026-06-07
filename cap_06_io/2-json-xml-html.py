"""
JSON, XML, and HTML Data (Section 6.1)

Beyond plain CSV, two other text formats dominate the web. JSON (JavaScript Object
Notation) is the lingua franca of HTTP APIs: a free-form format of objects (dicts),
arrays (lists), strings, numbers, Booleans, and nulls. HTML and XML are the markup
formats behind web pages and structured documents. This file covers converting JSON
to/from Python with the stdlib `json` module, loading JSON into a DataFrame with
`pd.read_json` and exporting with `to_json`, scraping tables out of HTML with
`pd.read_html`, and parsing XML records with `pd.read_xml`. All sample documents are
written to a temporary directory so the file runs offline and leaves no files behind.

JSON / HTML / XML ENTRY POINTS
FUNCTION         DESCRIPTION
json.loads       Parse a JSON string into Python objects (dict/list/...)
json.dumps       Serialize a Python object back into a JSON string
pd.read_json     Read a JSON string/file (array of objects) into a DataFrame
DataFrame.to_json  Serialize a DataFrame to JSON (orient controls the layout)
pd.read_html     Parse every <table> in an HTML document into a list of DataFrames
pd.read_xml      Read a flat set of repeated XML records into a DataFrame

Run:
    poetry run python cap_06_io/2-json-xml-html.py
"""

import json
import tempfile
from pathlib import Path

import pandas as pd


def explain_json_with_stdlib() -> None:
    """
    Problem: convert between a JSON string and Python objects, then build a
    DataFrame from part of the parsed structure.
    Why: `json.loads` turns JSON text into nested dicts/lists; `json.dumps`
    reverses it. JSON is nearly valid Python except for `null`/`true`/`false`.
    A list of dicts maps cleanly onto the DataFrame constructor, and you can
    select a subset of fields via `columns`.
    """
    print("== JSON with the stdlib json module ==")

    obj = """
    {"name": "Wes",
     "cities_lived": ["Akron", "Nashville", "New York", "San Francisco"],
     "pet": null,
     "siblings": [{"name": "Scott", "age": 34, "hobbies": ["guitars", "soccer"]},
                  {"name": "Katie", "age": 42, "hobbies": ["diving", "art"]}]
    }
    """

    # JSON string -> Python objects (note: null becomes None).
    result = json.loads(obj)
    print(result)

    # Python objects -> JSON string.
    asjson = json.dumps(result)
    print(asjson)

    # Build a DataFrame from a list of dicts, keeping only chosen fields.
    siblings = pd.DataFrame(result["siblings"], columns=["name", "age"])
    print(siblings)


def explain_pandas_json() -> None:
    """
    Problem: read a JSON file directly into a DataFrame and export one back to JSON.
    Why: `pd.read_json` assumes, by default, that each object in a top-level JSON
    array is a row. `to_json` serializes a DataFrame; the `orient` argument picks
    the layout ("records" produces the familiar list-of-objects form).
    """
    print("== pandas read_json / to_json ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)
        (examples / "example.json").write_text(
            '[{"a": 1, "b": 2, "c": 3},\n'
            ' {"a": 4, "b": 5, "c": 6},\n'
            ' {"a": 7, "b": 8, "c": 9}]\n'
        )
        # Each object in the array becomes a row.
        data = pd.read_json(examples / "example.json")
        print(data)

        # Export back to JSON: default (column-oriented) and "records" layout.
        print(data.to_json())
        print(data.to_json(orient="records"))


def explain_read_html() -> None:
    """
    Problem: extract tabular data embedded in an HTML page.
    Why: `pd.read_html` (backed by lxml / BeautifulSoup / html5lib) finds every
    <table> in the document and returns a list of DataFrames. By default it parses
    all tables, so you index into the result to get the one you want.
    """
    print("== Scraping HTML tables with read_html ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)
        # A small stand-in for the book's FDIC failed-bank-list HTML file.
        (examples / "banks.html").write_text(
            """<html><body>
            <table>
              <thead>
                <tr><th>Bank Name</th><th>City</th><th>ST</th><th>CERT</th></tr>
              </thead>
              <tbody>
                <tr><td>Allied Bank</td><td>Mulberry</td><td>AR</td><td>91</td></tr>
                <tr><td>The Woodbury Banking Company</td><td>Woodbury</td><td>GA</td><td>11297</td></tr>
                <tr><td>First CornerStone Bank</td><td>King of Prussia</td><td>PA</td><td>35312</td></tr>
              </tbody>
            </table>
            </body></html>
            """
        )
        # read_html returns a LIST of DataFrames (one per <table> found).
        tables = pd.read_html(examples / "banks.html")
        print(len(tables))
        failures = tables[0]
        print(failures.head())


def explain_read_xml() -> None:
    """
    Problem: turn a set of repeated XML records into a DataFrame.
    Why: XML supports nested, hierarchical data with metadata. When records share
    a repeated element with flat children (as in the book's MTA performance files),
    `pd.read_xml` collapses each record into a row in a single call — no manual
    tree walking required.
    """
    print("== Parsing XML records with read_xml ==")

    with tempfile.TemporaryDirectory() as tmp:
        examples = Path(tmp)
        # Two flat <INDICATOR> records, mirroring the book's MTA XML shape.
        (examples / "perf.xml").write_text(
            """<PERFORMANCE>
              <INDICATOR>
                <INDICATOR_SEQ>28445</INDICATOR_SEQ>
                <AGENCY_NAME>Metro-North Railroad</AGENCY_NAME>
                <INDICATOR_NAME>On-Time Performance (West of Hudson)</INDICATOR_NAME>
                <PERIOD_YEAR>2008</PERIOD_YEAR>
                <PERIOD_MONTH>1</PERIOD_MONTH>
                <YTD_TARGET>95.0</YTD_TARGET>
                <YTD_ACTUAL>96.9</YTD_ACTUAL>
              </INDICATOR>
              <INDICATOR>
                <INDICATOR_SEQ>28445</INDICATOR_SEQ>
                <AGENCY_NAME>Metro-North Railroad</AGENCY_NAME>
                <INDICATOR_NAME>On-Time Performance (West of Hudson)</INDICATOR_NAME>
                <PERIOD_YEAR>2008</PERIOD_YEAR>
                <PERIOD_MONTH>2</PERIOD_MONTH>
                <YTD_TARGET>95.0</YTD_TARGET>
                <YTD_ACTUAL>96.0</YTD_ACTUAL>
              </INDICATOR>
            </PERFORMANCE>
            """
        )
        # One line collapses every <INDICATOR> record into a row.
        perf = pd.read_xml(examples / "perf.xml")
        print(perf.head())


def main() -> None:
    explain_json_with_stdlib()
    explain_pandas_json()
    explain_read_html()
    explain_read_xml()


main()
