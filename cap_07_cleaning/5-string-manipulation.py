"""
String Manipulation (Section 7.4)

Python has long been a popular raw data manipulation language thanks to its ease
of use for string and text processing. Most text operations are simple with the
string object's built-in methods; for more complex pattern matching, regular
expressions (the `re` module) are needed; and pandas adds vectorized string and
regex operations over whole arrays via the `.str` accessor, while gracefully
handling missing data. This file covers all three layers.

THREE LAYERS OF STRING TOOLS
LAYER              KEY OPERATIONS
str (built-in)     split, strip, join, in / index / find, count, replace, upper/lower
re module          split, findall, match, search, sub, compile, groups (\\1, \\2)
pandas .str        contains, findall, get, slicing, extract (vectorized, NA-aware)

Run:
    poetry run python cap_07_cleaning/5-string-manipulation.py
"""

import re

import numpy as np
import pandas as pd


def explain_builtin_string_methods() -> None:
    """
    Problem: break apart, clean, recombine, and search plain Python strings.
    Why: built-in methods cover most munging. `split` breaks on a delimiter;
    `strip` trims whitespace; `join` glues a sequence with a separator; `in` is
    the best substring test (with `index`/`find` as alternatives — `index` raises
    if not found while `find` returns -1); `count` tallies occurrences; and
    `replace` substitutes (or deletes, via an empty string) a pattern.
    """
    print("== Python built-in string object methods ==")

    val = "a,b,  guido"
    print(val.split(","))                                  # split on a delimiter
    pieces = [x.strip() for x in val.split(",")]           # split + strip whitespace
    print(pieces)

    first, second, third = pieces
    print(first + "::" + second + "::" + third)            # concatenation
    print("::".join(pieces))                               # the Pythonic way: join

    print("guido" in val)                                  # best substring test
    print(val.index(","))                                  # position; raises if absent
    print(val.find(":"))                                   # -1 when not found
    print(val.count(","))                                  # number of occurrences
    print(val.replace(",", "::"))                          # substitute a pattern
    print(val.replace(",", ""))                            # delete a pattern


def explain_regular_expressions() -> None:
    """
    Problem: match flexible text patterns.
    Why: the `re` module groups into pattern matching, substitution, and
    splitting. `re.split`/`re.compile` split on a regex (`\\s+` = whitespace runs);
    `findall` returns all matches; `search` returns the first match object;
    `match` only matches at the start; `sub` replaces matches; and parenthesized
    groups let `groups()`/`findall` return tuples and `sub` reference them via
    \\1, \\2.
    """
    print("== Regular expressions (the re module) ==")

    text = "foo    bar\t baz  \tqux"
    print(re.split(r"\s+", text))            # split on runs of whitespace
    regex = re.compile(r"\s+")               # compile once, reuse many times
    print(regex.split(text))
    print(regex.findall(text))               # all matched whitespace runs

    # A regex that identifies most email addresses.
    text2 = """Dave dave@google.com
Steve steve@gmail.com
Rob rob@gmail.com
Ryan ryan@yahoo.com"""
    pattern = r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}"
    regex = re.compile(pattern, flags=re.IGNORECASE)
    print(regex.findall(text2))              # all email addresses

    m = regex.search(text2)                  # first match object
    print(m)
    assert m is not None
    print(text2[m.start():m.end()])
    print(regex.match(text2))                # None: no match at the start

    print(regex.sub("REDACTED", text2))      # replace every match

    # Parenthesized groups segment each match into components.
    pattern = r"([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})"
    regex = re.compile(pattern, flags=re.IGNORECASE)
    m = regex.match("wesm@bright.net")
    assert m is not None
    print(m.groups())                        # ('wesm', 'bright', 'net')
    print(regex.findall(text2))              # list of tuples
    # \1, \2, \3 reference the matched groups in the replacement string.
    print(regex.sub(r"Username: \1, Domain: \2, Suffix: \3", text2))


def explain_pandas_string_functions() -> None:
    """
    Problem: apply string operations over a whole Series with missing data.
    Why: mapping a function with `map` fails on NA values; the Series `.str`
    accessor provides array-oriented string methods that skip and propagate NA.
    `str.contains` tests membership, `str.findall` runs a regex per element,
    `str.get`/`str[i]` retrieves an element from list-valued results, `str[:n]`
    slices each string, and `str.extract` returns the captured groups as a
    DataFrame. Converting to the "string" extension type yields boolean (nullable)
    results instead of object.
    """
    print("== String functions in pandas (the .str accessor) ==")

    data = pd.Series(
        {"Dave": "dave@google.com", "Steve": "steve@gmail.com",
         "Rob": "rob@gmail.com", "Wes": np.nan}
    )
    print(data)
    print(data.isna())

    # Vectorized substring test; NA propagates as NaN.
    print(data.str.contains("gmail"))

    # Converting to the string extension type yields a nullable boolean result.
    data_as_string_ext = data.astype("string")
    print(data_as_string_ext.str.contains("gmail"))

    pattern = r"([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})"
    # str.findall with regex flags, then vectorized element retrieval.
    matches = data.str.findall(pattern, flags=re.IGNORECASE).str[0]
    print(matches)
    print(matches.str.get(1))                # the domain from each tuple
    print(data.str[:5])                      # slice the first 5 chars of each
    # str.extract returns the captured groups as a DataFrame.
    print(data.str.extract(pattern, flags=re.IGNORECASE))


def main() -> None:
    explain_builtin_string_methods()
    explain_regular_expressions()
    explain_pandas_string_functions()


main()
