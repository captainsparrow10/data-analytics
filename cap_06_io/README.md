# Chapter 6 — Data Loading, Storage, and File Formats

Getting data into (and out of) pandas is the first step of nearly every analysis. This
chapter covers the main I/O categories: reading and writing text formats (CSV and other
delimited files), the web-native formats JSON/XML/HTML, efficient binary formats (pickle,
Excel, HDF5), pulling data from web APIs with `requests`, and loading the results of SQL
queries from a relational database.

Same format as the earlier chapters: every file is self-documenting and runnable — a
module docstring explains the topic (with a reference table where the book has one), and
each exercise is a function documenting the problem, its purpose, and *why* the solution is
written that way, reproducing the book's `In [..]` examples faithfully.

Every file is **self-contained and offline**: the book reads files from an `examples/`
directory, but these files instead build the equivalent sample data inside a
`tempfile.TemporaryDirectory()` (or `mkdtemp` for the database), do their work there, and
clean up — so running them never touches the repo and needs no network.

## Index

The full chapter, in strict book order (6.1 → 6.4), one file per sub-section:

| File | Topic | Book section | Status |
|------|-------|--------------|--------|
| `1-reading-writing-text.py` | `read_csv` options (header, names, index_col, skiprows, na_values), reading in pieces (`nrows`/`chunksize`), `to_csv`, the `csv` module + Dialect | 6.1 | ✅ done |
| `2-json-xml-html.py` | JSON (`json.loads`/`dumps`, `read_json`/`to_json`), `read_html`, `read_xml` | 6.1 | ✅ done |
| `3-binary-formats.py` | pickle, Microsoft Excel (`ExcelFile`/`ExcelWriter`/`read_excel`), HDF5 (`HDFStore`/`to_hdf`/`read_hdf`) | 6.2 | ✅ done |
| `4-web-apis.py` | GitHub-issues `requests` example (live call shown, parsed offline) | 6.3 | ✅ done |
| `5-databases.py` | SQLite via `sqlite3`, then SQLAlchemy + `read_sql` | 6.4 | ✅ done |
| `exercises.py` | Practice exercises | — | ✅ done |

## Running

```bash
poetry run python cap_06_io/1-reading-writing-text.py   # runs every exercise in the file
```

## pandas 3.0 / NumPy 2.x notes

The book targets older pandas; these files were adapted to the installed pandas **3.0.3**
and NumPy **2.4.6**:

- `ExcelWriter.save()` is deprecated → use the `ExcelWriter` context manager so closing
  the writer persists the workbook (file 3).
- The web-API example runs offline: the live `requests.get(...)` call is shown in comments
  and a same-shape JSON payload is parsed instead, so output is deterministic (file 4).
- HDF5 examples use `np.random.default_rng(seed=...)` instead of the legacy
  `np.random.standard_normal` for reproducible output (file 3).

pandas comes from the project's Poetry dependencies. See the [project README](../README.md)
for setup and conventions, and [Chapter 5](../cap_05_pandas/README.md) for the established
exercise pattern.
