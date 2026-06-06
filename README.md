# data-analytics

Study workspace for Python fundamentals and data analysis. Each topic is a single,
self-documenting, runnable Python file: a module docstring explains the type/topic and
its operators, and every exercise is a function with a docstring covering the problem,
its purpose, the given input, the expected output, and *why* the solution is written
that way.

The exercises are adapted from the [PYnative](https://pynative.com/) practice sets.

## Chapter 1 — Built-ins (`cap_01_built-in/`)

```
cap_01_built-in/
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

## Running an exercise file

Each file runs end to end and prints the result of every exercise:

```bash
python3 cap_01_built-in/data-structures/3-set.py
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

## Type checking

The project is checked with [pyright](https://github.com/microsoft/pyright) in
**strict** mode (configured in `pyproject.toml` under `[tool.pyright]`, the same rules
Pylance applies in the editor). Every file is kept at **0 type errors**.

```bash
npx -y pyright@latest
```
