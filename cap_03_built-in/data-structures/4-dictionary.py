"""
Dictionaries: A Complete Guide to Key-Value Mappings in Python

A dictionary is a mutable mapping from unique, hashable keys to arbitrary values.
It offers average O(1) lookup, insertion, and deletion by key, and since Python 3.7
it preserves insertion order. This file contains 40 exercises covering dictionary
fundamentals and common idioms.

=== DICTIONARY OPERATORS & METHODS ===

1. INDEXING (d[key])
   Description: Read or assign the value for a key; reading a missing key raises KeyError
   Example: {"a": 1}["a"] = 1

2. GET (d.get(key, default))
   Description: Safe read; returns default (None) instead of raising on a missing key
   Example: {"a": 1}.get("b", 0) = 0

3. SETDEFAULT (d.setdefault(key, default))
   Description: Return d[key]; if absent, insert it with default first
   Example: d.setdefault("k", []).append(1)

4. UPDATE (d.update(other))
   Description: Merge another mapping/iterable of pairs in place (overwrites on clash)
   Example: {"a": 1}.update({"b": 2}) -> {"a": 1, "b": 2}

5. POP (d.pop(key[, default]))
   Description: Remove a key and return its value
   Example: {"a": 1}.pop("a") = 1

6. DEL (del d[key])
   Description: Delete a key in place; raises KeyError if absent
   Example: del d["a"]

7. CLEAR (d.clear())
   Description: Remove every item, leaving an empty dict
   Example: {"a": 1}.clear() -> {}

8. MEMBERSHIP (key in d)
   Description: Tests membership against KEYS (not values)
   Example: "a" in {"a": 1} = True

9. VIEWS (d.keys(), d.values(), d.items())
   Description: Dynamic, set-like views over keys, values, and (key, value) pairs
   Example: list({"a": 1}.items()) = [("a", 1)]

10. MERGE OPERATORS (| and |=)  [Python 3.9+]
    Description: d1 | d2 returns a merged dict; |= merges in place (right wins on clash)
    Example: {"a": 1} | {"a": 2} = {"a": 2}

11. UNPACKING ({**d1, **d2})
    Description: Spread one or more dicts into a new one (right wins on clash)
    Example: {**{"a": 1}, **{"b": 2}} = {"a": 1, "b": 2}

12. DICT COMPREHENSION ({k: v for ...})
    Description: Build a dict declaratively from any iterable
    Example: {x: x**2 for x in range(3)} = {0: 0, 1: 1, 2: 4}

13. CONSTRUCTORS (dict(zip(...)), dict(list_of_pairs), dict.fromkeys(keys, default))
    Description: Build dicts from paired iterables, pair lists, or a key list + default
    Example: dict(zip(["a"], [1])) = {"a": 1}

14. LENGTH (len(d))
    Description: Number of key-value pairs
    Example: len({"a": 1, "b": 2}) = 2
"""

from typing import Any, cast


def exercise_one():
    """
    Exercise 1: Basic Dictionary Operations

    Problem: Add a new key-value pair, modify an existing value, and access a key.

    Purpose: This exercise covers the three everyday operations on a dict: insert,
    update, and read by key. Assigning to an existing key overwrites it; assigning
    to a new key creates it.

    Given Input: student = {"name": "Alice", "age": 20, "grade": "B"}
    Expected Output: updated dict with age 21 and city added, plus Name: Alice
    """
    student: dict[str, Any] = {"name": "Alice", "age": 20, "grade": "B"}
    student["city"] = "New York"  # new key -> insert
    student["age"] = 21           # existing key -> overwrite
    print(student)
    print(f"Name: {student['name']}")


def exercise_two():
    """
    Exercise 2: Dictionary Operations

    Problem: Remove a specific key, retrieve all key-value pairs, and check key
    existence.

    Purpose: This exercise shows del for deletion, .items() for iterating pairs,
    and that the `in` operator checks KEYS, which is the most common gotcha for
    beginners expecting it to check values.

    Given Input: car = {"brand": "Toyota", "model": "Camry", "year": 2022, "color": "blue"}
    Expected Output: dict without 'color', the items view, and True/False checks
    """
    car: dict[str, Any] = {"brand": "Toyota", "model": "Camry", "year": 2022, "color": "blue"}
    del car["color"]
    print(car)
    print(list(car.items()))
    print(f"'brand' in car: {'brand' in car}")
    print(f"'price' in car: {'price' in car}")


def exercise_three():
    """
    Exercise 3: Dictionary from Two Lists

    Problem: Create a dictionary by mapping two equal-length lists.

    Purpose: This exercise pairs zip() with dict() to build a mapping. The values
    list is heterogeneous, so it is annotated list[Any]; otherwise pyright would
    infer list[Unknown] in strict mode.

    Given Input: keys = ["name", "age", "city"], values = ["Bob", 25, "London"]
    Expected Output: {'name': 'Bob', 'age': 25, 'city': 'London'}
    """
    keys = ["name", "age", "city"]
    values: list[Any] = ["Bob", 25, "London"]
    print(dict(zip(keys, values)))


def exercise_four():
    """
    Exercise 4: Clear Dictionary

    Problem: Remove all items while keeping the dictionary object intact.

    Purpose: This exercise shows .clear() empties the dict in place, so every
    reference to the same object sees it become empty (unlike rebinding to {}).

    Given Input: inventory = {"apples": 10, "bananas": 5, "oranges": 8}
    Expected Output: {}
    """
    inventory = {"apples": 10, "bananas": 5, "oranges": 8}
    inventory.clear()
    print(inventory)


def exercise_five():
    """
    Exercise 5: Merge Dictionaries

    Problem: Combine two dictionaries, with the second taking precedence on clashes.

    Purpose: This exercise demonstrates the | merge operator (3.9+). When a key
    exists in both, the right-hand dictionary's value wins.

    Given Input: dict1 = {"a": 1, "b": 2}, dict2 = {"b": 3, "c": 4}
    Expected Output: {'a': 1, 'b': 3, 'c': 4}
    """
    dict1 = {"a": 1, "b": 2}
    dict2 = {"b": 3, "c": 4}
    print(dict1 | dict2)


def exercise_six():
    """
    Exercise 6: Access Nested Dictionary

    Problem: Retrieve a value from a nested dictionary structure.

    Purpose: This exercise chains indexing to drill into a nested dict. The outer
    dict is annotated dict[str, Any] because its values are heterogeneous (a string
    and a sub-dict); without it, indexing the union type would be a strict error.

    Given Input: person = {"name": "Carol", "address": {"city": "Paris", "zip": "75001"}}
    Expected Output: City: Paris
    """
    person: dict[str, Any] = {"name": "Carol", "address": {"city": "Paris", "zip": "75001"}}
    print(f"City: {person['address']['city']}")


def exercise_seven():
    """
    Exercise 7: Access 'history' Key From Nested Dictionary

    Problem: Extract the value associated with "history" from a nested grades dict.

    Purpose: This exercise reinforces nested access, again using dict[str, Any] for
    the heterogeneous outer mapping.

    Given Input: student = {"name": "Dave", "grades": {"math": 88, "science": 92, "history": 75}}
    Expected Output: History grade: 75
    """
    student: dict[str, Any] = {"name": "Dave", "grades": {"math": 88, "science": 92, "history": 75}}
    print(f"History grade: {student['grades']['history']}")


def exercise_eight():
    """
    Exercise 8: Initialize Dictionary with Default Values

    Problem: Create a dictionary from a list of keys all sharing one default value.

    Purpose: This exercise shows dict.fromkeys(), the cleanest way to seed a mapping
    with a uniform starting value (careful: a mutable default would be SHARED, so
    fromkeys is best used with immutable defaults like 0).

    Given Input: keys = ["math", "science", "english", "history"], default = 0
    Expected Output: {'math': 0, 'science': 0, 'english': 0, 'history': 0}
    """
    keys = ["math", "science", "english", "history"]
    default = 0
    print(dict.fromkeys(keys, default))


def exercise_nine():
    """
    Exercise 9: Rename a Key of Dictionary

    Problem: Change a key's name while preserving its value.

    Purpose: This exercise shows that "renaming" is really pop-the-old-key and
    assign-the-new-one, since keys are immutable identifiers, not editable in place.

    Given Input: employee = {"fname": "John", "age": 30, "dept": "Engineering"}
    Expected Output: {'first_name': 'John', 'age': 30, 'dept': 'Engineering'}
    """
    employee: dict[str, Any] = {"fname": "John", "age": 30, "dept": "Engineering"}
    employee["first_name"] = employee.pop("fname")
    print(employee)


def exercise_ten():
    """
    Exercise 10: Delete a List of Keys

    Problem: Remove multiple specific keys in one operation.

    Purpose: This exercise uses .pop(key, None) in a loop so that a missing key
    does not crash the routine, a safer batch-delete than del.

    Given Input: product = {"id": 101, "name": "Laptop", "price": 999, "stock": 50, "warehouse": "A3"}
    Expected Output: {'id': 101, 'name': 'Laptop', 'price': 999}
    """
    product: dict[str, Any] = {
        "id": 101, "name": "Laptop", "price": 999, "stock": 50, "warehouse": "A3"
    }
    for key in ["stock", "warehouse"]:
        product.pop(key, None)
    print(product)


def exercise_eleven():
    """
    Exercise 11: Check Value Existence

    Problem: Verify whether a specific value exists anywhere in a dictionary.

    Purpose: This exercise highlights that `in` checks keys, so to search values you
    must test against d.values() explicitly.

    Given Input: roles = {"alice": "admin", "bob": "editor", "carol": "viewer"}
    Expected Output: 'editor' exists as a value: True, 'manager' exists as a value: False
    """
    roles = {"alice": "admin", "bob": "editor", "carol": "viewer"}
    print(f"'editor' exists as a value: {'editor' in roles.values()}")
    print(f"'manager' exists as a value: {'manager' in roles.values()}")


def exercise_twelve():
    """
    Exercise 12: Sum All Values

    Problem: Calculate the total of all numerical values in a dictionary.

    Purpose: This exercise shows that sum() consumes the .values() view directly,
    no manual loop required.

    Given Input: expenses = {"rent": 1200, "food": 300, "transport": 150, "utilities": 200}
    Expected Output: Total expenses: 1850
    """
    expenses = {"rent": 1200, "food": 300, "transport": 150, "utilities": 200}
    print(f"Total expenses: {sum(expenses.values())}")


def exercise_thirteen():
    """
    Exercise 13: Extract Subset of Keys

    Problem: Create a new dictionary containing only the specified keys.

    Purpose: This exercise uses a dict comprehension guarded by membership so that
    requesting a missing key never raises.

    Given Input: user with id/username/email/password/joined; extract id, username, email
    Expected Output: {'id': 42, 'username': 'jdoe', 'email': 'jdoe@example.com'}
    """
    user: dict[str, Any] = {
        "id": 42,
        "username": "jdoe",
        "email": "jdoe@example.com",
        "password": "s3cr3t",
        "joined": "2021-03-15",
    }
    wanted = ["id", "username", "email"]
    subset = {k: user[k] for k in wanted if k in user}
    print(subset)


def exercise_fourteen():
    """
    Exercise 14: Map Two Lists (zip)

    Problem: Combine lists of keys and values into a single dictionary using zip.

    Purpose: This exercise repeats the zip+dict idiom; the values list is annotated
    list[Any] because it mixes strings and an int.

    Given Input: attributes = ["brand", "model", "year", "color"], details = ["Honda", "Civic", 2023, "silver"]
    Expected Output: {'brand': 'Honda', 'model': 'Civic', 'year': 2023, 'color': 'silver'}
    """
    attributes = ["brand", "model", "year", "color"]
    details: list[Any] = ["Honda", "Civic", 2023, "silver"]
    print(dict(zip(attributes, details)))


def exercise_fifteen():
    """
    Exercise 15: Count Character Frequencies

    Problem: Count how many times each character appears in a string.

    Purpose: This exercise builds a frequency table with .get(char, 0), the classic
    counter idiom that avoids a separate "first time seen?" check.

    Given Input: text = "hello world"
    Expected Output: {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}
    """
    text = "hello world"
    freq: dict[str, int] = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    print(freq)


def exercise_sixteen():
    """
    Exercise 16: Modify Nested Dictionary

    Problem: Change a specific value inside a nested dictionary.

    Purpose: This exercise shows that mutating a nested dict is just chained
    indexing on the left of an assignment.

    Given Input: company = {"name": "TechCorp", "location": {"city": "Berlin", "country": "Germany"}}
    Expected Output: location city becomes 'Munich'
    """
    company: dict[str, Any] = {
        "name": "TechCorp",
        "location": {"city": "Berlin", "country": "Germany"},
    }
    company["location"]["city"] = "Munich"
    print(company)


def exercise_seventeen():
    """
    Exercise 17: Update Deeply Nested Key

    Problem: Modify a value located several levels deep.

    Purpose: This exercise extends chained indexing to multiple levels, showing the
    pattern scales to any depth.

    Given Input: data = {"school": {"department": {"class": {"teacher": "Mr. Smith", "students": 30}}}}
    Expected Output: students becomes 35
    """
    data: dict[str, Any] = {
        "school": {"department": {"class": {"teacher": "Mr. Smith", "students": 30}}}
    }
    data["school"]["department"]["class"]["students"] = 35
    print(data)


def exercise_eighteen():
    """
    Exercise 18: Dictionary Comprehension

    Problem: Generate a dictionary of squared numbers from 1 to 10.

    Purpose: This exercise introduces the dict comprehension, mapping each key to a
    computed value in one expression.

    Given Input: numbers 1 through 10
    Expected Output: {1: 1, 2: 4, ..., 10: 100}
    """
    squares = {n: n**2 for n in range(1, 11)}
    print(squares)


def exercise_nineteen():
    """
    Exercise 19: Filter Dictionary

    Problem: Create a new dict with only the pairs whose value satisfies a condition.

    Purpose: This exercise filters with a guarded dict comprehension over .items().

    Given Input: scores = {"Alice": 82, "Bob": 45, "Carol": 91, "Dave": 58, "Eve": 73}
    Expected Output: {'Alice': 82, 'Carol': 91, 'Eve': 73}
    """
    scores = {"Alice": 82, "Bob": 45, "Carol": 91, "Dave": 58, "Eve": 73}
    passing = {name: score for name, score in scores.items() if score > 60}
    print(passing)


def exercise_twenty():
    """
    Exercise 20: Key of Minimum Value

    Problem: Find the key associated with the smallest value.

    Purpose: This exercise shows min() over the keys with a key= function that looks
    up each value. A lambda is used (rather than dict.get) because get's return type
    includes None, which is not comparable.

    Given Input: stock = {"apples": 34, "bananas": 12, "oranges": 57, "grapes": 8, "mangoes": 23}
    Expected Output: Lowest stock item: grapes
    """
    stock = {"apples": 34, "bananas": 12, "oranges": 57, "grapes": 8, "mangoes": 23}
    lowest = min(stock, key=lambda k: stock[k])
    print(f"Lowest stock item: {lowest}")


def exercise_twenty_one():
    """
    Exercise 21: Key of Maximum Value

    Problem: Find the key associated with the highest value.

    Purpose: This exercise mirrors the previous one with max(). On ties, max()
    returns the first key encountered in insertion order.

    Given Input: scores = {"Alice": 88, "Bob": 95, "Carol": 72, "Dave": 95, "Eve": 84}
    Expected Output: Top scorer: Bob
    """
    scores = {"Alice": 88, "Bob": 95, "Carol": 72, "Dave": 95, "Eve": 84}
    top = max(scores, key=lambda k: scores[k])
    print(f"Top scorer: {top}")


def exercise_twenty_two():
    """
    Exercise 22: List of Tuples to Dictionary

    Problem: Convert a list of key-value tuples into a dictionary.

    Purpose: This exercise shows that dict() accepts any iterable of (key, value)
    pairs directly.

    Given Input: pairs = [("name", "Alice"), ("age", 25), ("city", "Paris")]
    Expected Output: {'name': 'Alice', 'age': 25, 'city': 'Paris'}
    """
    pairs: list[tuple[str, Any]] = [("name", "Alice"), ("age", 25), ("city", "Paris")]
    print(dict(pairs))


def exercise_twenty_three():
    """
    Exercise 23: Find Common Keys

    Problem: Identify all keys present in both dictionaries.

    Purpose: This exercise uses the set-like behavior of .keys() views, so the &
    operator finds shared keys directly.

    Given Input: d1 = {"a": 1, "b": 2, "c": 3}, d2 = {"b": 20, "c": 30, "d": 40}
    Expected Output: Common keys: {'b', 'c'}
    """
    d1 = {"a": 1, "b": 2, "c": 3}
    d2 = {"b": 20, "c": 30, "d": 40}
    print(f"Common keys: {d1.keys() & d2.keys()}")


def exercise_twenty_four():
    """
    Exercise 24: Dictionary Difference

    Problem: Find keys in the first dictionary that are absent from the second.

    Purpose: This exercise applies the - operator to key views for a directional
    difference.

    Given Input: d1 = {"a": 1, "b": 2, "c": 3}, d2 = {"b": 20, "d": 40}
    Expected Output: Keys only in d1: {'a', 'c'}
    """
    d1 = {"a": 1, "b": 2, "c": 3}
    d2 = {"b": 20, "d": 40}
    print(f"Keys only in d1: {d1.keys() - d2.keys()}")


def exercise_twenty_five():
    """
    Exercise 25: Dictionary Intersection

    Problem: Build a dict with only the key-value pairs identical in both inputs.

    Purpose: This exercise shows that comparing pairs (not just keys) requires
    checking both that the key exists in the other dict AND that the values match.

    Given Input: d1 = {"a": 1, "b": 2, "c": 3}, d2 = {"a": 1, "b": 99, "c": 3}
    Expected Output: Intersection: {'a': 1, 'c': 3}
    """
    d1 = {"a": 1, "b": 2, "c": 3}
    d2 = {"a": 1, "b": 99, "c": 3}
    shared = {k: v for k, v in d1.items() if d2.get(k) == v}
    print(f"Intersection: {shared}")


def exercise_twenty_six():
    """
    Exercise 26: Word Count

    Problem: Count word frequencies in a string, case-insensitively.

    Purpose: This exercise lowercases first so that "The" and "the" count together,
    then applies the .get(word, 0) counter idiom.

    Given Input: text = "the cat sat on the mat the cat"
    Expected Output: {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1}
    """
    text = "the cat sat on the mat the cat"
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    print(counts)


def exercise_twenty_seven():
    """
    Exercise 27: Remove None Values

    Problem: Remove all key-value pairs whose value is None.

    Purpose: This exercise filters with `is not None` (identity, the correct test
    for None) rather than truthiness, which would also drop valid falsy values
    like 0 or "".

    Given Input: data = {"name": "Alice", "age": None, "city": "Paris", "score": None}
    Expected Output: {'name': 'Alice', 'city': 'Paris'}
    """
    data: dict[str, str | None] = {
        "name": "Alice", "age": None, "city": "Paris", "score": None
    }
    cleaned = {k: v for k, v in data.items() if v is not None}
    print(cleaned)


def exercise_twenty_eight():
    """
    Exercise 28: Sort Dictionary by Keys

    Problem: Sort a dictionary by its keys in ascending order.

    Purpose: This exercise shows that sorted() over .items() (which sorts by the
    first tuple element, the key) feeds dict() to rebuild an ordered mapping.

    Given Input: data = {"banana": 3, "apple": 5, "cherry": 1, "date": 4}
    Expected Output: {'apple': 5, 'banana': 3, 'cherry': 1, 'date': 4}
    """
    data = {"banana": 3, "apple": 5, "cherry": 1, "date": 4}
    print(dict(sorted(data.items())))


def exercise_twenty_nine():
    """
    Exercise 29: Sort Dictionary by Values

    Problem: Sort a dictionary's items based on their values.

    Purpose: This exercise supplies a key= lambda selecting the value (x[1]) so the
    ordering is by value instead of by key.

    Given Input: scores = {"Alice": 88, "Bob": 72, "Charlie": 95, "Diana": 60}
    Expected Output: {'Diana': 60, 'Bob': 72, 'Alice': 88, 'Charlie': 95}
    """
    scores = {"Alice": 88, "Bob": 72, "Charlie": 95, "Diana": 60}
    print(dict(sorted(scores.items(), key=lambda item: item[1])))


def exercise_thirty():
    """
    Exercise 30: Unique Values Check

    Problem: Verify whether all dictionary values are distinct.

    Purpose: This exercise compares len(values) against len(set(values)): if dropping
    duplicates changes the count, some values repeated.

    Given Input: data = {"a": 1, "b": 2, "c": 3, "d": 2}
    Expected Output: False
    """
    data = {"a": 1, "b": 2, "c": 3, "d": 2}
    all_unique = len(set(data.values())) == len(data)
    print(all_unique)


def exercise_thirty_one():
    """
    Exercise 31: Check for Subset

    Problem: Verify whether one dictionary is a subset of another.

    Purpose: This exercise uses the set-like .items() view: subset.items() <= main.items()
    is True only when every pair of `subset` appears identically in `main`.

    Given Input: main = {"a": 1, "b": 2, "c": 3, "d": 4}, subset = {"a": 1, "c": 3}
    Expected Output: True
    """
    main = {"a": 1, "b": 2, "c": 3, "d": 4}
    subset = {"a": 1, "c": 3}
    print(subset.items() <= main.items())


def exercise_thirty_two():
    """
    Exercise 32: Sort Dictionary by Value Length

    Problem: Sort a dictionary by the character length of its string values.

    Purpose: This exercise shows a derived sort key: len(item[1]) sorts by how long
    each value string is, not by the value itself.

    Given Input: words = {"a": "banana", "b": "kiwi", "c": "strawberry", "d": "fig"}
    Expected Output: {'d': 'fig', 'b': 'kiwi', 'a': 'banana', 'c': 'strawberry'}
    """
    words = {"a": "banana", "b": "kiwi", "c": "strawberry", "d": "fig"}
    print(dict(sorted(words.items(), key=lambda item: len(item[1]))))


def exercise_thirty_three():
    """
    Exercise 33: Key with Longest List

    Problem: Find the key whose list value has the most elements.

    Purpose: This exercise uses max() over keys with key=lambda k: len(data[k]),
    measuring each value's length to pick the winner.

    Given Input: data = {"fruits": [...3...], "vegs": [...1...], "grains": [...2...]}
    Expected Output: fruits
    """
    data: dict[str, list[str]] = {
        "fruits": ["apple", "banana", "cherry"],
        "vegs": ["carrot"],
        "grains": ["rice", "wheat"],
    }
    longest = max(data, key=lambda k: len(data[k]))
    print(longest)


def exercise_thirty_four():
    """
    Exercise 34: Convert Dictionary to JSON

    Problem: Convert a nested dictionary into formatted JSON.

    Purpose: This exercise introduces json.dumps with indent= for human-readable,
    pretty-printed output, the standard way to serialize a dict to text.

    Given Input: person = {"name": "Alice", "age": 30, "address": {"city": "Mumbai", "pin": "400001"}}
    Expected Output: indented JSON string
    """
    import json

    person: dict[str, Any] = {
        "name": "Alice",
        "age": 30,
        "address": {"city": "Mumbai", "pin": "400001"},
    }
    print(json.dumps(person, indent=2))


def exercise_thirty_five():
    """
    Exercise 35: Invert Dictionary

    Problem: Swap keys and values so original values become keys.

    Purpose: This exercise inverts a mapping with a dict comprehension. It works
    cleanly only when values are unique AND hashable (so they can become keys).

    Given Input: original = {"a": 1, "b": 2, "c": 3}
    Expected Output: {1: 'a', 2: 'b', 3: 'c'}
    """
    original = {"a": 1, "b": 2, "c": 3}
    inverted = {value: key for key, value in original.items()}
    print(inverted)


def exercise_thirty_six():
    """
    Exercise 36: Invert with Duplicate Values

    Problem: Invert a dictionary where several keys share a value, grouping the
    original keys into lists.

    Purpose: This exercise shows .setdefault(value, []).append(key), the idiom for
    safely accumulating into per-key lists without a separate initialization step.

    Given Input: original = {"a": 1, "b": 2, "c": 1, "d": 3, "e": 2}
    Expected Output: {1: ['a', 'c'], 2: ['b', 'e'], 3: ['d']}
    """
    original = {"a": 1, "b": 2, "c": 1, "d": 3, "e": 2}
    grouped: dict[int, list[str]] = {}
    for key, value in original.items():
        grouped.setdefault(value, []).append(key)
    print(grouped)


def exercise_thirty_seven():
    """
    Exercise 37: Flatten Nested Dictionary

    Problem: Convert a multi-level nested dict into a single level using
    dot-separated compound keys.

    Purpose: This exercise applies recursion: when a value is itself a dict, recurse
    with an extended key prefix; otherwise record the leaf. The isinstance check
    narrows the value to a dict, and cast restores its element types for the
    recursive call (same idiom as the list/tuple flatten exercises).

    Given Input: nested = {"a": 1, "b": {"c": 2, "d": {"e": 3, "f": 4}}}
    Expected Output: {'a': 1, 'b.c': 2, 'b.d.e': 3, 'b.d.f': 4}
    """

    def flatten(d: dict[str, Any], prefix: str = "") -> dict[str, Any]:
        flat: dict[str, Any] = {}
        for key, value in d.items():
            compound = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                flat.update(flatten(cast(dict[str, Any], value), compound))
            else:
                flat[compound] = value
        return flat

    nested: dict[str, Any] = {"a": 1, "b": {"c": 2, "d": {"e": 3, "f": 4}}}
    print(flatten(nested))


def exercise_thirty_eight():
    """
    Exercise 38: Group by First Letter

    Problem: Organize words into a dictionary grouped by their starting letter.

    Purpose: This exercise again uses setdefault to build groups, keyed by word[0].

    Given Input: words = ["apple", "avocado", "banana", "blueberry", "cherry", "apricot"]
    Expected Output: {'a': ['apple', 'avocado', 'apricot'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}
    """
    words = ["apple", "avocado", "banana", "blueberry", "cherry", "apricot"]
    groups: dict[str, list[str]] = {}
    for word in words:
        groups.setdefault(word[0], []).append(word)
    print(groups)


def exercise_thirty_nine():
    """
    Exercise 39: Merge and Sum Overlapping

    Problem: Merge two dictionaries, adding values for keys that appear in both.

    Purpose: This exercise shows accumulation across dicts: copy the first, then for
    each pair of the second add to the existing value (defaulting to 0 via .get).

    Given Input: dict1 = {"a": 10, "b": 20, "c": 30}, dict2 = {"b": 5, "c": 15, "d": 25}
    Expected Output: {'a': 10, 'b': 25, 'c': 45, 'd': 25}
    """
    dict1 = {"a": 10, "b": 20, "c": 30}
    dict2 = {"b": 5, "c": 15, "d": 25}
    merged = dict(dict1)  # start from a copy so the original is untouched
    for key, value in dict2.items():
        merged[key] = merged.get(key, 0) + value
    print(merged)


def exercise_forty():
    """
    Exercise 40: Deep vs. Shallow Copy

    Problem: Demonstrate how shallow and deep copies differ with nested mutable
    structures.

    Purpose: This exercise exposes the subtlety: a shallow copy duplicates the top
    level but SHARES the nested list, so mutating the list shows up in both. A deep
    copy clones every level, so the copies are fully independent.

    Given Input: original = {"name": "Alice", "scores": [90, 85, 92]}
    Expected Output: shows the shallow copy reflecting the change, the deep copy not
    """
    import copy

    original: dict[str, Any] = {"name": "Alice", "scores": [90, 85, 92]}
    shallow = original.copy()
    deep = copy.deepcopy(original)

    original["scores"].append(100)  # mutate the nested list in place
    print(f"shallow shares the list:  {shallow['scores']}")
    print(f"deep copy is independent: {deep['scores']}")


if __name__ == "__main__":
    print("=== Exercise 1: Basic Dictionary Operations ===")
    exercise_one()

    print("\n=== Exercise 2: Dictionary Operations ===")
    exercise_two()

    print("\n=== Exercise 3: Dictionary from Two Lists ===")
    exercise_three()

    print("\n=== Exercise 4: Clear Dictionary ===")
    exercise_four()

    print("\n=== Exercise 5: Merge Dictionaries ===")
    exercise_five()

    print("\n=== Exercise 6: Access Nested Dictionary ===")
    exercise_six()

    print("\n=== Exercise 7: Access 'history' Key From Nested Dictionary ===")
    exercise_seven()

    print("\n=== Exercise 8: Initialize Dictionary with Default Values ===")
    exercise_eight()

    print("\n=== Exercise 9: Rename a Key of Dictionary ===")
    exercise_nine()

    print("\n=== Exercise 10: Delete a List of Keys ===")
    exercise_ten()

    print("\n=== Exercise 11: Check Value Existence ===")
    exercise_eleven()

    print("\n=== Exercise 12: Sum All Values ===")
    exercise_twelve()

    print("\n=== Exercise 13: Extract Subset of Keys ===")
    exercise_thirteen()

    print("\n=== Exercise 14: Map Two Lists (zip) ===")
    exercise_fourteen()

    print("\n=== Exercise 15: Count Character Frequencies ===")
    exercise_fifteen()

    print("\n=== Exercise 16: Modify Nested Dictionary ===")
    exercise_sixteen()

    print("\n=== Exercise 17: Update Deeply Nested Key ===")
    exercise_seventeen()

    print("\n=== Exercise 18: Dictionary Comprehension ===")
    exercise_eighteen()

    print("\n=== Exercise 19: Filter Dictionary ===")
    exercise_nineteen()

    print("\n=== Exercise 20: Key of Minimum Value ===")
    exercise_twenty()

    print("\n=== Exercise 21: Key of Maximum Value ===")
    exercise_twenty_one()

    print("\n=== Exercise 22: List of Tuples to Dictionary ===")
    exercise_twenty_two()

    print("\n=== Exercise 23: Find Common Keys ===")
    exercise_twenty_three()

    print("\n=== Exercise 24: Dictionary Difference ===")
    exercise_twenty_four()

    print("\n=== Exercise 25: Dictionary Intersection ===")
    exercise_twenty_five()

    print("\n=== Exercise 26: Word Count ===")
    exercise_twenty_six()

    print("\n=== Exercise 27: Remove None Values ===")
    exercise_twenty_seven()

    print("\n=== Exercise 28: Sort Dictionary by Keys ===")
    exercise_twenty_eight()

    print("\n=== Exercise 29: Sort Dictionary by Values ===")
    exercise_twenty_nine()

    print("\n=== Exercise 30: Unique Values Check ===")
    exercise_thirty()

    print("\n=== Exercise 31: Check for Subset ===")
    exercise_thirty_one()

    print("\n=== Exercise 32: Sort Dictionary by Value Length ===")
    exercise_thirty_two()

    print("\n=== Exercise 33: Key with Longest List ===")
    exercise_thirty_three()

    print("\n=== Exercise 34: Convert Dictionary to JSON ===")
    exercise_thirty_four()

    print("\n=== Exercise 35: Invert Dictionary ===")
    exercise_thirty_five()

    print("\n=== Exercise 36: Invert with Duplicate Values ===")
    exercise_thirty_six()

    print("\n=== Exercise 37: Flatten Nested Dictionary ===")
    exercise_thirty_seven()

    print("\n=== Exercise 38: Group by First Letter ===")
    exercise_thirty_eight()

    print("\n=== Exercise 39: Merge and Sum Overlapping ===")
    exercise_thirty_nine()

    print("\n=== Exercise 40: Deep vs. Shallow Copy ===")
    exercise_forty()
