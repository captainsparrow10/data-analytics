"""
JSON: A Complete Guide to Serializing Data in Python

JSON (JavaScript Object Notation) is a text format for exchanging structured data.
Python's built-in `json` module converts between Python objects and JSON text:
dumps/dump serialize (Python -> JSON), loads/load deserialize (JSON -> Python).
This file contains 9 exercises covering JSON handling.

NOTE: json.loads() returns Any (the shape is only known at runtime), so values read
from JSON are annotated Any; this keeps dynamic/nested access type-clean under strict
checking. Exercise 4 uses a temporary file so it runs without touching the workspace.

=== JSON CONCEPTS ===

1. SERIALIZE (json.dumps(obj))
   Description: Convert a Python object to a JSON string
   Example: json.dumps({"a": 1}) = '{"a": 1}'

2. DESERIALIZE (json.loads(text))
   Description: Parse a JSON string into Python objects (dict, list, str, int, ...)
   Example: json.loads('{"a": 1}') = {"a": 1}

3. FILE I/O (json.dump(obj, file) / json.load(file))
   Description: Write/read JSON directly to/from a file object
   Example: json.dump(data, f)

4. PRETTY PRINTING (indent=, separators=, sort_keys=)
   Description: Control whitespace, item/key separators, and key ordering
   Example: json.dumps(d, indent=2, sort_keys=True)

5. OBJECTS <-> JSON
   Description: Serialize via an instance's __dict__; rebuild by passing parsed fields
   Example: json.dumps(obj.__dict__)

6. ERROR HANDLING (json.JSONDecodeError)
   Description: Raised when the text is not valid JSON
   Example: except json.JSONDecodeError: ...

Run:
    poetry run python cap_03_built-in/files/2-json.py
"""

import json
import tempfile
from pathlib import Path
from typing import Any


def exercise_one() -> None:
    """
    Exercise 1: Dictionary to JSON Conversion

    Problem: Convert a dictionary into JSON format.

    Purpose: This exercise introduces json.dumps(), which serializes a Python dict
    into a JSON-formatted string.

    Given Input: data = {"key1": "value1", "key2": "value2"}
    Expected Output: {"key1": "value1", "key2": "value2"}
    """
    data = {"key1": "value1", "key2": "value2"}
    print(json.dumps(data))


def exercise_two() -> None:
    """
    Exercise 2: Access JSON Value

    Problem: Access the value of key2 from a JSON string.

    Purpose: This exercise uses json.loads() to parse text into a dict, then indexes
    it like any dict. The parsed result is Any, so indexing stays type-clean.

    Given Input: '{"key1": "value1", "key2": "value2"}'
    Expected Output: value2
    """
    json_text = '{"key1": "value1", "key2": "value2"}'
    data: Any = json.loads(json_text)
    print(data["key2"])


def exercise_three() -> None:
    """
    Exercise 3: Pretty Print JSON

    Problem: Pretty-print JSON with indent level 2 and separators (",", " = ").

    Purpose: This exercise shows the formatting controls of json.dumps(): indent adds
    line breaks and nesting, while separators customizes how items and key/value pairs
    are joined.

    Given Input: {"key1": "value1", "key2": "value2"}
    Expected Output: formatted JSON with indent 2 and " = " between keys and values
    """
    data = {"key1": "value1", "key2": "value2"}
    print(json.dumps(data, indent=2, separators=(",", " = ")))


def exercise_four() -> None:
    """
    Exercise 4: Sort and Write JSON

    Problem: Sort JSON data by keys alphabetically and write it to a file.

    Purpose: This exercise combines sort_keys=True (alphabetical key order) with
    json.dump() to write straight to a file object.

    Given Input: {"id": 1, "name": "value2", "age": 29}
    Expected Output: a file with keys ordered age, id, name
    """
    data: dict[str, Any] = {"id": 1, "name": "value2", "age": 29}
    with tempfile.TemporaryDirectory() as tmp:
        json_file = Path(tmp) / "sorted.json"
        with json_file.open("w") as file:
            json.dump(data, file, indent=2, sort_keys=True)
        print(json_file.read_text())


def exercise_five() -> None:
    """
    Exercise 5: Access Nested JSON Key

    Problem: Access the nested key 'salary'.

    Purpose: This exercise drills into a parsed nested structure with chained indexing.

    Given Input: company -> employee -> payble -> salary
    Expected Output: 7000
    """
    json_text = (
        '{"company": {"employee": {"name": "emma", '
        '"payble": {"salary": 7000, "bonus": 800}}}}'
    )
    data: Any = json.loads(json_text)
    print(data["company"]["employee"]["payble"]["salary"])


def exercise_six() -> None:
    """
    Exercise 6: Object to JSON

    Problem: Convert a Vehicle object into JSON.

    Purpose: This exercise serializes a custom object by passing its __dict__ (the
    attribute namespace) to json.dumps(), since json cannot serialize arbitrary
    objects directly.

    Given Input: Vehicle("Toyota Rav4", "2.5L", 32000)
    Expected Output: a JSON object of the vehicle's attributes
    """
    class Vehicle:
        def __init__(self, name: str, engine: str, price: int) -> None:
            self.name = name
            self.engine = engine
            self.price = price

    vehicle = Vehicle("Toyota Rav4", "2.5L", 32000)
    print(json.dumps(vehicle.__dict__, indent=2))


def exercise_seven() -> None:
    """
    Exercise 7: JSON to Object

    Problem: Convert a JSON string into a Vehicle object.

    Purpose: This exercise parses the JSON to a dict, then constructs the object by
    passing the fields into its constructor, enabling dot-notation access afterward.

    Given Input: '{"name": "Toyota Rav4", "engine": "2.5L", "price": 32000}'
    Expected Output: vehicle.name accessible via dot notation
    """
    class Vehicle:
        def __init__(self, name: str, engine: str, price: int) -> None:
            self.name = name
            self.engine = engine
            self.price = price

    json_text = '{"name": "Toyota Rav4", "engine": "2.5L", "price": 32000}'
    data: Any = json.loads(json_text)
    vehicle = Vehicle(data["name"], data["engine"], data["price"])
    print(f"{vehicle.name} | {vehicle.engine} | {vehicle.price}")


def exercise_eight() -> None:
    """
    Exercise 8: JSON Validation

    Problem: Check whether JSON is valid; if invalid, correct it.

    Purpose: This exercise shows that json.loads raises json.JSONDecodeError on
    malformed input. Catching it lets the program detect invalid JSON and recover.

    Given Input: JSON missing a comma after "salary": 7000
    Expected Output: the decode error, then the corrected JSON parsed successfully
    """
    invalid = '{"name": "Jessa" "salary": 7000}'  # missing comma
    try:
        json.loads(invalid)
    except json.JSONDecodeError as error:
        print(f"Invalid JSON: {error.msg}")

    corrected = '{"name": "Jessa", "salary": 7000}'
    print(f"Corrected: {json.loads(corrected)}")


def exercise_nine() -> None:
    """
    Exercise 9: Parse Array for Specific Key

    Problem: Get all values of the key 'name' from an array of objects.

    Purpose: This exercise parses a JSON array into a list of dicts and uses a list
    comprehension to project a single field out of each element.

    Given Input: an array of objects each with id, name, color
    Expected Output: ['name1', 'name2']
    """
    json_text = (
        '[{"id": 1, "name": "name1", "color": "red"}, '
        '{"id": 2, "name": "name2", "color": "blue"}]'
    )
    data: Any = json.loads(json_text)
    names = [item["name"] for item in data]
    print(names)


def main() -> None:
    print("=== Exercise 1: Dictionary to JSON Conversion ===")
    exercise_one()

    print("\n=== Exercise 2: Access JSON Value ===")
    exercise_two()

    print("\n=== Exercise 3: Pretty Print JSON ===")
    exercise_three()

    print("\n=== Exercise 4: Sort and Write JSON ===")
    exercise_four()

    print("\n=== Exercise 5: Access Nested JSON Key ===")
    exercise_five()

    print("\n=== Exercise 6: Object to JSON ===")
    exercise_six()

    print("\n=== Exercise 7: JSON to Object ===")
    exercise_seven()

    print("\n=== Exercise 8: JSON Validation ===")
    exercise_eight()

    print("\n=== Exercise 9: Parse Array for Specific Key ===")
    exercise_nine()


main()
