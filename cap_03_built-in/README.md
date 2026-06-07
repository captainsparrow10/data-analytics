# Chapter 1 — Python Built-ins

The core Python language: built-in data structures, control flow, functions, file and
JSON handling, input/output, and two essential standard-library modules (regex and
random). Every file is self-documenting and runnable — a module docstring explains the
topic and its operators, and each exercise is a function documenting the problem, its
purpose, the input, the expected output, and *why* the solution is written that way.

Exercises adapted from [PYnative](https://pynative.com/). **373 exercises** across 13 files.

## Index

### `data-structures/`
| File | Topic | Exercises |
|------|-------|-----------|
| [1-tupple.py](data-structures/1-tupple.py) | Tuples — immutable sequences | 25 |
| [2-list.py](data-structures/2-list.py) | Lists — mutable sequences | 45 |
| [3-set.py](data-structures/3-set.py) | Sets — unique unordered collections | 31 |
| [4-dictionary.py](data-structures/4-dictionary.py) | Dictionaries — key/value mappings | 40 |
| [5-string.py](data-structures/5-string.py) | Strings — immutable text | 38 |

### `control-flow/`
| File | Topic | Exercises |
|------|-------|-----------|
| [1-if-else-for-loop.py](control-flow/1-if-else-for-loop.py) | Conditionals & loops | 40 |

### `functions/`
| File | Topic | Exercises |
|------|-------|-----------|
| [1-functions.py](functions/1-functions.py) | Functions, args, scope, lambda | 18 |
| [2-iterators-generators.py](functions/2-iterators-generators.py) | Iterators & generators | 30 |

### `files/`
| File | Topic | Exercises |
|------|-------|-----------|
| [1-file-handling.py](files/1-file-handling.py) | Reading & writing files | 34 |
| [2-json.py](files/2-json.py) | JSON serialization | 9 |

### `io/`
| File | Topic | Exercises |
|------|-------|-----------|
| [1-input-output.py](io/1-input-output.py) | Input & output formatting | 23 |

### `stdlib/`
| File | Topic | Exercises |
|------|-------|-----------|
| [1-regex.py](stdlib/1-regex.py) | Regular expressions | 30 |
| [2-random.py](stdlib/2-random.py) | Random & secrets | 10 |

## Running

```bash
python3 cap_03_built-in/data-structures/3-set.py   # runs every exercise in the file
```

Each file is kept at 0 pyright-strict errors. See the [project README](../README.md)
for conventions (non-interactive input, tempfile self-containment, reproducible random).
