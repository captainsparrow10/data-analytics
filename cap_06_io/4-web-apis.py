"""
Interacting with Web APIs (Section 6.3)

Many websites expose public APIs that deliver data feeds as JSON. The recommended
way to call them from Python is the `requests` package: issue a GET request, check
for HTTP errors with `raise_for_status()`, then decode the body with `response.json()`,
which returns parsed Python objects. The book's example fetches the last 30 GitHub
issues for the pandas project. To keep THIS file runnable offline and deterministic,
the live `requests.get(...)` call is shown and explained in comments, while a small
hardcoded JSON payload of the SAME SHAPE is parsed into a DataFrame — so the data
flow (JSON list of dicts -> DataFrame, selecting fields) is identical to the book's.

WEB API WORKFLOW (requests)
STEP                       DESCRIPTION
requests.get(url)          Issue an HTTP GET request, returning a Response
resp.raise_for_status()    Raise an exception if the HTTP status is an error
resp.json()                Decode the JSON body into Python objects (list/dict)
pd.DataFrame(data, ...)    Build a DataFrame from the list of issue dicts

Run:
    poetry run python cap_06_io/4-web-apis.py
"""

import pandas as pd


def explain_github_issues() -> None:
    """
    Problem: load the last 30 GitHub issues for pandas into a DataFrame.
    Why: a REST API returns a JSON array where each element is a dict describing
    one issue. `resp.json()` decodes it to a list of dicts, which feeds the
    DataFrame constructor directly; `columns=[...]` keeps only the fields of
    interest. We keep it offline by parsing a small same-shape payload instead of
    hitting the network.
    """
    print("== GitHub issues via a web API ==")

    # --- The LIVE call (shown for reference; NOT executed so this runs offline) ---
    #
    #   import requests
    #   url = "https://api.github.com/repos/pandas-dev/pandas/issues"
    #   resp = requests.get(url)
    #   resp.raise_for_status()        # good practice: error out on a bad status
    #   data = resp.json()             # -> a Python list of issue dicts
    #
    # Because the API returns real-time data, the live results would differ on
    # every run. Below we use a fixed payload with the SAME SHAPE so the rest of
    # the example (building a DataFrame, selecting fields) is identical.

    data = [
        {
            "number": 48062,
            "title": "REF: make copy keyword non-stateful",
            "labels": [{"id": 76811, "name": "Refactor"}],
            "state": "open",
        },
        {
            "number": 48061,
            "title": "STYLE: upgrade flake8",
            "labels": [],
            "state": "open",
        },
        {
            "number": 48060,
            "title": 'DOC: "Creating a Python environment" in "Creating a development environment"',
            "labels": [{"id": 134699, "name": "Docs"}],
            "state": "open",
        },
        {
            "number": 48059,
            "title": "REGR: Avoid overflow with groupby sum",
            "labels": [{"id": 233160, "name": "Regression"}],
            "state": "open",
        },
    ]

    # Each element is a dict of one issue's fields; data[0]["title"] is the first.
    print(data[0]["title"])

    # Pass the list of dicts straight to the DataFrame and keep chosen columns.
    issues = pd.DataFrame(data, columns=["number", "title", "labels", "state"])
    print(issues)


def main() -> None:
    explain_github_issues()


main()
