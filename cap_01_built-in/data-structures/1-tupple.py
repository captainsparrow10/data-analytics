"""
Tuples: A Complete Guide to Immutable Sequences in Python

A tuple is a fixed-length, immutable sequence of Python objects which, once assigned,
cannot be changed. This file contains 22 exercises covering tuple fundamentals.

=== TUPLE OPERATORS ===

1. CONCATENATION (+)
   Description: Combine two tuples into one
   Example: (1, 2) + (3, 4) = (1, 2, 3, 4)

2. REPETITION (*)
   Description: Repeat a tuple a specified number of times
   Example: (1, 2) * 3 = (1, 2, 1, 2, 1, 2)

3. INDEXING ([index])
   Description: Access an element by its position (0-based)
   Example: (10, 20, 30)[1] = 20
   Example: (10, 20, 30)[-1] = 30 (last element)

4. SLICING ([start:end:step])
   Description: Extract a portion of a tuple
   Example: (1, 2, 3, 4, 5)[1:4] = (2, 3, 4)
   Example: (1, 2, 3, 4, 5)[::-1] = (5, 4, 3, 2, 1) (reverse)

5. LENGTH (len())
   Description: Get the number of elements in a tuple
   Example: len((1, 2, 3)) = 3

6. MEMBERSHIP (in)
   Description: Check if an element exists in a tuple
   Example: 2 in (1, 2, 3) = True
   Example: 5 in (1, 2, 3) = False

7. NON-MEMBERSHIP (not in)
   Description: Check if an element does NOT exist in a tuple
   Example: 5 not in (1, 2, 3) = True

8. MINIMUM (min())
   Description: Find the smallest element
   Example: min((5, 2, 8, 1)) = 1

9. MAXIMUM (max())
   Description: Find the largest element
   Example: max((5, 2, 8, 1)) = 8

10. SUM (sum())
    Description: Calculate the sum of all elements (only for numeric tuples)
    Example: sum((1, 2, 3, 4)) = 10

11. EQUALITY (==)
    Description: Check if two tuples are identical
    Example: (1, 2) == (1, 2) = True
    Example: (1, 2) == (2, 1) = False

12. INEQUALITY (!=)
    Description: Check if two tuples are different
    Example: (1, 2) != (2, 1) = True

13. COMPARISON (<, >, <=, >=)
    Description: Compare tuples lexicographically
    Example: (1, 2) < (1, 3) = True
    Example: (2, 0) > (1, 9) = True

14. ITERATION (for)
    Description: Loop through each element in a tuple
    Example: for item in (1, 2, 3): print(item)
    Output: 1, 2, 3

15. UNPACKING
    Description: Assign tuple elements to multiple variables
    Example: a, b, c = (1, 2, 3)
    Result: a=1, b=2, c=3

16. COUNT (tuple.count())
    Description: Count occurrences of an element
    Example: (1, 2, 2, 3, 2).count(2) = 3

17. INDEX (tuple.index())
    Description: Find the first index of an element
    Example: (1, 2, 3, 2).index(2) = 1
"""

from typing import Any, NamedTuple, cast


def exercise_one():
    """
    Exercise 1: Basic Tuple Operations

    Problem: Create a tuple, access its elements by index, and find its length.

    Purpose: This exercise introduces you to the fundamental building blocks of working
    with tuples: creating them, retrieving individual elements using index positions,
    and measuring their size using len().

    Given Input: fruits = ("apple", "banana", "cherry", "date")
    Expected Output: First element: apple, Last element: date, and Length: 4
    """
    fruits = ("apple", "banana", "cherry", "date")
    first_element = fruits[0]
    last_element = fruits[-1]
    length = len(fruits)
    print(
        f"First element: {first_element}, Last element: {last_element}, and Length: {length}"
    )


def exercise_two():
    """
    Exercise 2: The Trailing Comma

    Problem: Create a tuple containing a single item, the number 50, and confirm its type.

    Purpose: This exercise highlights one of the most common beginner mistakes with tuples:
    assuming that parentheses alone create a tuple. A trailing comma is required when the
    tuple has only one element.

    Given Input: A single integer value 50
    Expected Output: (50,) and <class 'tuple'>
    """
    single_item_tuple = 50
    print(single_item_tuple)
    print(type(single_item_tuple))

    single_item_tuple = (50,)
    print(single_item_tuple)
    print(type(single_item_tuple))


def exercise_three():
    """
    Exercise 3: Tuple Repetition

    Problem: Repeat a tuple three times using the * operator.

    Purpose: This exercise shows how the * operator works with sequences. Repeating a tuple
    is a concise way to generate patterned data without writing loops.

    Given Input: colors = ("red", "green")
    Expected Output: ('red', 'green', 'red', 'green', 'red', 'green')
    """
    colors = ("red", "green")
    repeated_colors = colors * 3
    print(repeated_colors)


def exercise_four():
    """
    Exercise 4: Tuple Concatenation

    Problem: Join three separate tuples into one new tuple using the + operator.

    Purpose: This exercise demonstrates how to combine multiple tuples without modifying
    any of the originals. Concatenation is useful when you need to assemble a final
    ordered collection from several independent parts.

    Given Input: a = (1, 2), b = (3, 4), and c = (5, 6)
    Expected Output: (1, 2, 3, 4, 5, 6)
    """
    a = (1, 2)
    b = (3, 4)
    c = (5, 6)
    combined_tuple = a + b + c
    print(combined_tuple)


def exercise_five():
    """
    Exercise 5: Tuple Slicing

    Problem: Extract a specific portion of a tuple using slice notation.

    Purpose: This exercise teaches you how to retrieve a contiguous subset of elements
    from a tuple without a loop. Slicing is fundamental to working with sequences.

    Given Input: numbers = (10, 20, 30, 40, 50, 60, 70)
    Expected Output: (30, 40, 50)
    """
    numbers = (10, 20, 30, 40, 50, 60, 70)
    sliced_tuple = numbers[2:5]
    print(sliced_tuple)


def exercise_six():
    """
    Exercise 6: Tuple Reversal

    Problem: Reverse the order of elements in a tuple.

    Purpose: This exercise shows how to reverse a tuple even though tuples have no built-in
    .reverse() method. You will practice using slice notation with a step value.

    Given Input: items = (1, 2, 3, 4, 5)
    Expected Output: (5, 4, 3, 2, 1)
    """
    items = (1, 2, 3, 4, 5)
    reversed_items = items[::-1]
    print(reversed_items)

    reversed_portion = items[4:1:-1]
    print(reversed_portion)


def exercise_seven():
    """
    Exercise 7: Type Casting

    Problem: Convert a list into a tuple using the tuple() constructor.

    Purpose: This exercise demonstrates how to convert between mutable and immutable
    sequence types. Converting a list to a tuple is useful when you want to protect
    data from accidental modification.

    Given Input: my_list = [10, 20, 30, 40, 50]
    Expected Output: (10, 20, 30, 40, 50) and <class 'tuple'>
    """
    my_list = [10, 20, 30, 40, 50]
    my_tuple = tuple(my_list)
    print(my_tuple)
    print(type(my_tuple))


def exercise_eight():
    """
    Exercise 8: Tuple to String

    Problem: Convert a tuple of characters into a single joined string.

    Purpose: This exercise shows how to bridge the gap between tuples and strings.
    The str.join() method is a core Python tool for assembling strings from
    iterable sequences.

    Given Input: chars = ('a', 'b', 'c')
    Expected Output: abc
    """
    chars = ("a", "b", "c")
    joined_string = "".join(chars)
    print(joined_string)


def exercise_nine():
    """
    Exercise 9: Tuple Membership Testing

    Problem: Check whether a specific element exists inside a tuple using the in keyword.

    Purpose: This exercise introduces membership testing, one of the most readable and
    expressive features of Python. Checking for the presence of a value in a collection
    is a task that appears constantly in real-world code.

    Given Input: fruits = ("apple", "banana", "cherry", "date")
    Expected Output: True and False
    """
    fruits = ("apple", "banana", "cherry", "date")
    print("banana" in fruits)
    print("grape" in fruits)  # type: ignore


def exercise_ten():
    """
    Exercise 10: Counting Elements

    Problem: Use the .count() method to find how many times a specific element
    appears in a tuple.

    Purpose: This exercise introduces one of the two built-in methods that tuples
    provide. Knowing how to count occurrences without writing a manual loop is
    practical for frequency analysis and data validation.

    Given Input: votes = ("yes", "no", "yes", "yes", "no", "yes")
    Expected Output: yes appears 4 times and no appears 2 times
    """
    votes = ("yes", "no", "yes", "yes", "no", "yes")
    yes_count = votes.count("yes")
    no_count = votes.count("no")
    print(f"yes appears {yes_count} times and no appears {no_count} times")


def exercise_eleven():
    """
    Exercise 11: Tuple Unpacking

    Problem: Unpack a four-element tuple into four distinct variables in a single assignment.

    Purpose: This exercise introduces tuple unpacking, one of Python's most elegant
    features. Unpacking makes code more readable by giving meaningful names to
    positional data, and it is widely used when working with function return values.

    Given Input: person = ("Alice", 30, "Engineer", "Pune")
    Expected Output: Name: Alice, Age: 30, Job: Engineer, and City: Pune
    """
    person = ("Alice", 30, "Engineer", "Pune")
    name, age, job, city = person
    print(f"Name: {name}, Age: {age}, Job: {job}, and City: {city}")


def exercise_twelve():
    """
    Exercise 12: The Swap Trick

    Problem: Swap the values of two variables using tuple unpacking, without using
    a temporary third variable.

    Purpose: This exercise demonstrates one of Python's most well-known idioms.
    The swap trick works because Python evaluates the entire right-hand side as a
    tuple before performing any assignment.

    Given Input: a = 100, b = 200
    Expected Output: After swap: a = 200, b = 100
    """
    a = 100
    b = 200
    a, b = b, a
    print(f"After swap: a = {a}, b = {b}")


def exercise_thirteen():
    """
    Exercise 13: Nested Tuple Access

    Problem: Access a specific element that is stored inside a tuple which is itself
    nested inside another tuple.

    Purpose: This exercise builds your understanding of nested data structures. Tuples
    can contain other tuples as elements, and chaining index operators is the standard
    way to drill down into them.

    Given Input: matrix = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    Expected Output: 6
    """
    matrix = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    element = matrix[1][2]
    print(element)


def exercise_fourteen():
    """
    Exercise 14: Tuple Statistics

    Problem: Calculate the total, highest value, and lowest value from a tuple of
    integers using the built-in sum(), max(), and min() functions.

    Purpose: This exercise shows that Python's built-in aggregate functions work
    directly on tuples, not just lists. Being able to derive quick statistics from
    an immutable sequence is a practical time-saver in data processing.

    Given Input: scores = (88, 95, 70, 62, 99, 74, 85)
    Expected Output: Sum: 573, Max: 99, and Min: 62
    """
    scores = (88, 95, 70, 62, 99, 74, 85)
    total = sum(scores)
    highest = max(scores)
    lowest = min(scores)
    print(f"Sum: {total}, Max: {highest}, and Min: {lowest}")


def exercise_fifteen():
    """
    Exercise 15: Sort Tuple of Tuples
    Problem Statement: Write a Python program to sort a tuple of tuples based on the second item in each nested tuple.

    Purpose: This exercise teaches you how to use the key parameter of Python’s sorted() function with a lambda to sort structured data by a specific field – a technique used constantly when ordering records, rankings, and tabular data.
    Given Input: students = (("Alice", 88), ("Bob", 73), ("Charlie", 95), ("Diana", 61))

    Expected Output:

    Sorted: (('Diana', 61), ('Bob', 73), ('Alice', 88), ('Charlie', 95))
    """
    students = (("Alice", 88), ("Bob", 73), ("Charlie", 95), ("Diana", 61))
    sorted_students = tuple(sorted(students, key=lambda x: x[1]))
    sorted_students_with_filter = tuple(
        s for s in sorted(students, key=lambda x: x[1]) if s[1] < 70
    )

    """The sorted() function returns a new sorted list, and we convert it back to a tuple using the tuple() constructor. The key parameter is set to a lambda function that takes each nested tuple (representing a student) and returns the second item (the score) for sorting purposes."""
    print(
        f"Sorted: {sorted_students}"
    )  # output: Sorted: (('Diana', 61), ('Bob', 73), ('Alice', 88), ('Charlie', 95))
    print(
        f"Sorted with filter: {sorted_students_with_filter}"
    )  # output: Sorted with filter: (('Diana', 61),)


def exercise_sixteen():
    """
    Exercise 16: Tuple Filtering
    Problem Statement: Write a Python program to filter a tuple and keep only the elements that satisfy a given condition, using both filter() and a list comprehension approach.

    Purpose: This exercise demonstrates two idiomatic ways to select a subset of items from a sequence based on a condition. Filtering is a foundational operation in data processing, validation, and functional-style programming.

    Given Input: numbers = (3, 14, 7, 22, 9, 41, 18, 5), keep only values greater than 10

    Expected Output: Filtered: (14, 22, 41, 18)
    """
    numbers = (3, 14, 7, 22, 9, 41, 18, 5)

    # Using filter() with a lambda function
    filtered_numbers_filter = tuple(filter(lambda x: x > 10, numbers))

    # Using a list comprehension and converting to a tuple
    filtered_numbers_comprehension = tuple(x for x in numbers if x > 10)

    print(f"Filtered using filter(): {filtered_numbers_filter}")
    print(f"Filtered using comprehension: {filtered_numbers_comprehension}")


def exercise_seventeen():
    """
    Exercise 17: Tuple Mapping
    Problem Statement: Write a Python program to apply a square function to every item in a tuple using map(), and also demonstrate the equivalent generator expression approach.

    Purpose: This exercise introduces the functional programming concept of mapping a transformation over a sequence. The map() function and its comprehension equivalent appear regularly in data transformation, preprocessing pipelines, and mathematical computations.

    Given Input: numbers = (1, 2, 3, 4, 5, 6)

    Expected Output: Squared: (1, 4, 9, 16, 25, 36)
    """
    numbers = (1, 2, 3, 4, 5, 6)

    # Using map() with a lambda function
    squared_numbers_map = tuple(map(lambda x: x**2, numbers))

    # Using a generator expression and converting to a tuple
    squared_numbers_comprehension = tuple(x**2 for x in numbers)

    print(f"Squared using map(): {squared_numbers_map}")
    print(f"Squared using comprehension: {squared_numbers_comprehension}")


def exercise_eighteen():
    """
    Exercise 18: Tuple Dictionary Mapping
    Problem Statement: Write a Python program to zip two tuples together – one holding keys and the other holding values – to create a dictionary.

    Purpose: This exercise demonstrates a common pattern for building dictionaries from paired data sources. Combining zip() with dict() is widely used when parsing CSV headers, mapping configuration keys to values, and constructing lookup tables from separate lists.

    Given Input: keys = ("name", "age", "city") and values = ("Alice", 30, "Pune")

    Expected Output: {'name': 'Alice', 'age': 30, 'city': 'Pune'}
    """
    keys = ("name", "age", "city")
    values = ("Alice", 30, "Pune")
    mapped_dict = dict(zip(keys, values))
    print(mapped_dict)


def exercise_nineteen():
    """
    Exercise 19: Tuple Intersection
    Problem Statement: Write a Python program to find all elements that are common to two different tuples.

    Purpose: This exercise introduces set intersection as a tool for comparing collections. Finding shared elements between two sequences is a core operation in data analysis, deduplication, access control (shared permissions), and any scenario where you need to identify overlap between datasets.

    Given Input: t1 = (1, 2, 3, 4, 5, 6) and t2 = (4, 5, 6, 7, 8, 9)

    Expected Output: (4, 5, 6)
    """
    t1 = (1, 2, 3, 4, 5, 6)
    t2 = (4, 5, 6, 7, 8, 9)
    intersection = tuple(set(t1) & set(t2))
    # The set() constructor converts the tuples into sets, which are unordered collections of unique elements. The & operator computes the intersection of the two sets, resulting in a new set that contains only the elements that are present in both sets. Finally, we convert the resulting set back into a tuple using the tuple() constructor. but if intersection = tuple(set(t1) & t2), it will not work because t2 is a tuple, and the & operator cannot be applied directly between a set and a tuple. Both operands need to be of the same type (in this case, sets) for the intersection operation to work correctly.
    # what happend in 1,2,3,7,8,9 is that they are not in both sets, so they are not included in the intersection result. why? because the intersection operation only includes elements that are present in both sets. Since 1, 2, 3 are only in t1 and 7, 8, 9 are only in t2, they do not meet the criteria for being included in the intersection. The intersection will only contain the elements that are common to both sets, which in this case are 4, 5, and 6.
    print(f"Intersection: {intersection}")


def exercise_twenty():
    """
    Exercise 20: The “Modification” Hack
    Problem Statement: Write a Python program to “modify” a tuple by converting it to a list, changing a specific item, and converting it back to a tuple.

    Purpose: This exercise highlights the immutability of tuples and demonstrates the standard workaround used when a one-off change is needed. Understanding this pattern also helps you appreciate why tuples are immutable by design and when to choose a list instead.

    Given Input: colours = ("red", "green", "blue"), replace "green" with "yellow"

    Expected Output:

    Original: ('red', 'green', 'blue')
    Modified: ('red', 'yellow', 'blue')
    """
    colours = ("red", "green", "blue")
    print(f"Original: {colours}")
    colours_list: list[str] = list(colours)

    colours_list[1] = "yellow"
    modified_colours = tuple(colours_list)
    print(f"Modified: {modified_colours}")


def exercise_twenty_one():
    """
    Exercise 21: Tuple Mutability

    Problem Statement: Create a tuple that contains a list as one of its elements. Modify the list in place and observe that the tuple’s identity stays the same while its contents appear to change.

    Purpose: This exercise uncovers one of Python’s most instructive subtleties: a tuple is immutable in the sense that its references cannot be reassigned, but if a reference points to a mutable object such as a list, that object itself can still be changed. Understanding this distinction is essential for writing predictable, bug-free code.

    Given Input: t = (1, 2, [3, 4, 5]), append 99 to the inner list

    Expected Output:

    Before: (1, 2, [3, 4, 5])
    After:  (1, 2, [3, 4, 5, 99])
    Same object? True
    """
    t = (1, 2, [3, 4, 5])
    print(f"Before: {t}")
    t[2].append(99)
    print(f"After:  {t}")
    print(f"Same object? {id(t) == id((1, 2, [3, 4, 5, 99]))}")


def exercise_twenty_two():
    """
    Exercise 22: Nested Tuple Flattening
    Problem Statement: Write a recursive Python function to flatten a deeply nested tuple of tuples into a single flat tuple containing all the individual values.

    Purpose: This exercise strengthens your understanding of recursion and type checking. Flattening nested structures is a practical requirement when processing tree-shaped data, parsed expressions, or hierarchical configurations where depth is not known in advance.

    Given Input: nested = (1, (2, 3), (4, (5, (6, 7))))

    Expected Output: Flattened: (1, 2, 3, 4, 5, 6, 7)
    """

    def flatten_tuple(nested: tuple[Any, ...]) -> tuple[Any, ...]:
        """Recursively flatten a nested tuple structure."""
        flat: list[Any] = []
        for item in nested:
            if isinstance(item, tuple):  # if the item is a tuple...
                flat.extend(
                    flatten_tuple(cast(tuple[Any, ...], item))
                )  # ...flatten it and extend the flat list with its contents
            else:  # if the item is not a tuple...
                flat.append(item)  # ...append it directly
        return tuple(flat)  # convert the flat list to a tuple

    nested = (1, (2, 3), (4, (5, (6, 7))))
    flattened = flatten_tuple(nested)
    print(f"Flattened: {flattened}")


def exercise_twenty_three():
    """
    Exercise 23: Memory Efficiency
    Problem Statement: Use the sys module to measure and compare the memory consumed by a list and a tuple, each holding the same one million integer elements.

    Purpose: This exercise gives you concrete, measurable evidence for one of the key practical advantages of tuples over lists: lower memory overhead. This matters in performance-sensitive applications that hold large collections of fixed data in memory.

    Given Input: A range of one million integers, range(1_000_000), stored as both a list and a tuple

    Expected Output: Printed byte sizes for the list and the tuple, followed by the difference in bytes (exact values vary by Python version and platform)
    """
    import sys

    million_list = list(range(1_000_000))
    million_tuple = tuple(million_list)

    list_size = sys.getsizeof(million_list)
    tuple_size = sys.getsizeof(million_tuple)

    print(f"List size: {list_size} bytes")
    print(f"Tuple size: {tuple_size} bytes")
    print(f"Difference: {list_size - tuple_size} bytes")


def exercise_twenty_four():
    """
    Exercise 24: NamedTuples

    Problem Statement: Use NamedTuple to define an Employee data structure with named fields, create a few instances, and perform a calculation such as finding the highest-paid employee.

    Purpose: This exercise introduces NamedTuple as a lightweight way to create readable, self-documenting data objects without the overhead of a full class. Named tuples are used extensively in standard library code, data pipelines, and anywhere structured records need to be passed around efficiently.

    Given Input: Three employees – ("Alice", "Engineering", 95000), ("Bob", "Marketing", 72000), ("Charlie", "Engineering", 88000)

    Expected Output:

    Alice works in Engineering and earns $95,000
    Bob works in Marketing and earns $72,000
    Charlie works in Engineering and earns $88,000
    Highest paid: Alice ($95,000)
    """

    class Employee(NamedTuple):
        name: str
        department: str
        salary: int

    employees: list[Employee] = [
        Employee("Alice", "Engineering", 95000),
        Employee("Bob", "Marketing", 72000),
        Employee("Charlie", "Engineering", 88000),
    ]

    for emp in employees:
        print(f"{emp.name} works in {emp.department} and earns ${emp.salary:,}")

    highest_paid = max(employees, key=lambda e: e.salary)
    print(f"Highest paid: {highest_paid.name} (${highest_paid.salary:,})")


def exercise_twenty_five():
    """
    Exercise 25: The Hashability Paradox

    Problem Statement: Write a Python program that experiments with using tuples as dictionary keys. Demonstrate why a fully immutable tuple like (1, 2) works as a key, while a tuple containing a mutable object like (1, [2]) raises a TypeError.

    Purpose: This exercise builds a deep understanding of Python’s hashing rules. Dictionary keys must be hashable, meaning their value must never change after being inserted. A tuple containing a mutable list violates this guarantee, which is why Python rejects it. This concept is fundamental to understanding how sets and dictionaries work internally.

    Given Input: Attempt to use (1, 2) and (1, [2]) as dictionary keys

    Expected Output:
        (1, 2) as key: success, value = "immutable tuple"
        (1, [2]) as key: TypeError - unhashable type: 'list'
    """
    my_dict = {}
    try:
        my_dict[(1, 2)] = "immutable tuple"
        print(f"(1, 2) as key: success, value = {my_dict[(1, 2)]}")
    except TypeError as e:
        print(f"(1, 2) as key: TypeError - {e}")

    try:
        my_dict[(1, [2])] = "mutable tuple"
        print(f"(1, [2]) as key: success, value = {my_dict[(1, [2])]}")
    except TypeError as e:
        print(f"(1, [2]) as key: TypeError - {e}")


if __name__ == "__main__":
    print("=== Exercise 1: Basic Tuple Operations ===")
    exercise_one()

    print("\n=== Exercise 2: The Trailing Comma ===")
    exercise_two()

    print("\n=== Exercise 3: Tuple Repetition ===")
    exercise_three()

    print("\n=== Exercise 4: Tuple Concatenation ===")
    exercise_four()

    print("\n=== Exercise 5: Tuple Slicing ===")
    exercise_five()

    print("\n=== Exercise 6: Tuple Reversal ===")
    exercise_six()

    print("\n=== Exercise 7: Type Casting ===")
    exercise_seven()

    print("\n=== Exercise 8: Tuple to String ===")
    exercise_eight()

    print("\n=== Exercise 9: Tuple Membership Testing ===")
    exercise_nine()

    print("\n=== Exercise 10: Counting Elements ===")
    exercise_ten()

    print("\n=== Exercise 11: Tuple Unpacking ===")
    exercise_eleven()

    print("\n=== Exercise 12: The Swap Trick ===")
    exercise_twelve()

    print("\n=== Exercise 13: Nested Tuple Access ===")
    exercise_thirteen()

    print("\n=== Exercise 14: Tuple Statistics ===")
    exercise_fourteen()

    print("\n=== Exercise 15: Sort Tuple of Tuples ===")
    exercise_fifteen()

    print("\n=== Exercise 16: Tuple Filtering ===")
    exercise_sixteen()

    print("\n=== Exercise 17: Tuple Mapping ===")
    exercise_seventeen()

    print("\n=== Exercise 18: Tuple Dictionary Mapping ===")
    exercise_eighteen()

    print("\n=== Exercise 19: Tuple Intersection ===")
    exercise_nineteen()

    print("\n=== Exercise 20: The “Modification” Hack ===")
    exercise_twenty()

    print("\n=== Exercise 21: Tuple Mutability ===")
    exercise_twenty_one()

    print("\n=== Exercise 22: Nested Tuple Flattening ===")
    exercise_twenty_two()

    print("\n=== Exercise 23: Memory Efficiency ===")
    exercise_twenty_three()

    print("\n=== Exercise 24: NamedTuples ===")
    exercise_twenty_four()

    print("\n=== Exercise 25: Tuple Dictionary Keys ===")
    exercise_twenty_five()
