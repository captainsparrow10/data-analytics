# data-analytics

Study workspace for Python fundamentals and data analysis. Each topic is a single,
self-documenting, runnable Python file: a module docstring explains the type/topic and
its operators, and every exercise is a function with a docstring covering the problem,
its purpose, the given input, the expected output, and *why* the solution is written
that way.

The exercises are adapted from the [PYnative](https://pynative.com/) practice sets.

## Chapters

| # | Chapter | Index |
|---|---------|-------|
| 1 | Python Built-ins | [cap_03_built-in/](cap_03_built-in/README.md) |
| 2 | NumPy Basics: Arrays and Vectorized Computation | [cap_04_numpy/](cap_04_numpy/README.md) |
| 3 | Getting Started with pandas | [cap_05_pandas/](cap_05_pandas/README.md) |
| 6 | Data Loading, Storage, and File Formats | [cap_06_io/](cap_06_io/README.md) |

## Chapter 1 — Built-ins (`cap_03_built-in/`)

```
cap_03_built-in/
├── data-structures/
│   ├── 1-tupple.py            # tuples            (25 exercises)
│   ├── 2-list.py              # lists             (45 exercises)
│   ├── 3-set.py               # sets              (31 exercises)
│   ├── 4-dictionary.py        # dictionaries      (40 exercises)
│   └── 5-string.py            # strings           (38 exercises)
├── control-flow/
│   └── 1-if-else-for-loop.py  # conditionals/loops (40 exercises)
├── functions/
│   ├── 1-functions.py         # functions          (18 exercises)
│   └── 2-iterators-generators.py  # iterators/generators (30 exercises)
├── files/
│   ├── 1-file-handling.py     # file I/O           (34 exercises)
│   └── 2-json.py              # JSON               (9 exercises)
├── io/
│   └── 1-input-output.py      # input & output     (23 exercises)
└── stdlib/
    ├── 1-regex.py             # regular expressions (30 exercises)
    └── 2-random.py            # random / secrets    (10 exercises)
```

## Chapter 3 — pandas (`cap_05_pandas/`)

```
cap_05_pandas/
├── 1-series.py                    # Series: creation, index, selection, dict interop, name   (5.1)
├── 2-dataframe.py                 # DataFrame: construction, loc/iloc, del, .T, to_numpy      (5.1)
├── 3-index-objects.py             # Index: immutability, set logic, duplicates, methods       (5.1)
├── 4-essential-functionality.py   # reindex, drop, indexing/filtering, arithmetic & alignment (5.2)
├── 5-function-sorting-ranking.py  # apply/map, sort_index/sort_values, rank, duplicate labels (5.2)
└── 6-descriptive-statistics.py    # reductions, describe, corr/cov/corrwith, unique/counts    (5.3)
```

## Chapter 6 — data loading (`cap_06_io/`)

```
cap_06_io/
├── 1-reading-writing-text.py  # read_csv options, nrows/chunksize, to_csv, csv module (6.1)
├── 2-json-xml-html.py         # JSON, read_html, read_xml                             (6.1)
├── 3-binary-formats.py        # pickle, Excel, HDF5                                   (6.2)
├── 4-web-apis.py              # GitHub-issues requests example (offline)             (6.3)
└── 5-databases.py             # SQLite via sqlite3, then SQLAlchemy + read_sql        (6.4)
```

## Running an exercise file

Each file runs end to end and prints the result of every exercise:

```bash
python3 cap_03_built-in/data-structures/3-set.py
```

## Conventions (read this before editing)

These conventions keep every file runnable unattended and verifiable.

1. **Non-interactive by design.** Exercises that originally used `input()` (file
   handling, input/output) instead use a fixed value, with the real call shown in a
   comment next to it (e.g. `name = "Alice"  # name = input(...)`). This lets the whole
   file run without blocking for keyboard input.

2. **Self-contained file I/O.** File and JSON exercises never touch the working
   directory. They create a `tempfile.TemporaryDirectory()`, do their work inside it,
   and clean up automatically — so running them leaves no stray files.

3. **Reproducible vs. cryptographic randomness.** In `stdlib/2-random.py`, exercises
   built on the `random` module call `random.seed()` so their output is stable on every
   run. Exercises built on the `secrets` module (OTPs, tokens) are cryptographically
   random *by design* and therefore produce different output each run — this is noted in
   their docstrings.

## Database (isolated, inside the devcontainer)

The devcontainer (`.devcontainer/docker-compose.yml`) starts two containers together:
`app` (where you work) and `db` (PostgreSQL 15). The database is **not published to the
host** — it has no `ports` mapping — so it is reachable **only from inside the
devcontainer**, never from your machine or anyone else's. It is a fully isolated
environment. Data persists across rebuilds in the named Docker volume `pgdata`.

Because `app` shares the db container's network namespace (`network_mode: service:db`),
the database lives at `localhost:5432`. The connection string is provided to `app` via
the `DATABASE_URL` environment variable and wrapped in a small typed helper:

```python
import pandas as pd
from database import get_engine

df = pd.read_sql("SELECT * FROM my_table", get_engine())
df.to_sql("my_table", get_engine(), if_exists="replace", index=False)
```

Smoke-test the connection from inside the devcontainer:

```bash
python database/connection.py   # prints the PostgreSQL server version
```

| setting  | value                |
|----------|----------------------|
| host     | `localhost`          |
| port     | `5432`               |
| user     | `sparrow`            |
| password | `1009`               |
| database | `data_analysis_db`   |

> Want to connect from your host (e.g. DBeaver)? It is intentionally closed off. Add
> `ports: ["5433:5432"]` to the `db` service and use `localhost:5433` — but that breaks
> the "isolated" guarantee, so only do it if you really need host access.

## Local setup (Poetry)

Dependencies are managed with [Poetry](https://python-poetry.org/). The full data stack
(numpy, pandas, matplotlib, IPython, Jupyter, SciPy, scikit-learn, statsmodels) plus
`psycopg2-binary` is declared in `pyproject.toml` using the modern PEP 621 `[project]`
table; `pyright` is a dev-only dependency. The virtualenv lives **inside the repo** at
`.venv/` (git-ignored) and is built on the single Homebrew Python — no extra Python
versions are installed.

First-time setup on macOS:

```bash
brew install python poetry                          # if not already installed
poetry config virtualenvs.in-project true           # keep the venv at ./.venv
poetry env use "$(brew --prefix)/bin/python3"       # create .venv with Homebrew Python
poetry install                                      # runtime + dev dependencies
```

Everyday use — run anything inside the environment with `poetry run`:

```bash
poetry run python cap_04_numpy/1-ndarray-basics.py  # run an exercise file
poetry shell                                        # or drop into the venv
```

Add or remove packages (updates `pyproject.toml` + `poetry.lock`):

```bash
poetry add <package>
poetry add --group dev <package>                    # dev-only tool
```

> **Heads-up if you also use the devcontainer.** It builds its own *Linux* `.venv`
> (Python under `/usr/local/bin`). That venv is invalid on a macOS host and makes every
> `poetry` command fail with `[Errno 2] No such file or directory: 'python'`. Fix: remove
> it and recreate locally — `rm -rf .venv && poetry env use "$(brew --prefix)/bin/python3"`.

## Type checking

Checked with [pyright](https://github.com/microsoft/pyright) in **strict** mode
(configured in `pyproject.toml` under `[tool.pyright]`; `venvPath`/`venv` point it at the
in-project `.venv` so third-party types resolve). Every file is kept at **0 errors**.

```bash
poetry run pyright                # whole project
poetry run pyright cap_04_numpy   # a single chapter
```
