"""
Lists: A Complete Guide to Mutable Sequences in Python

A list is a variable-length, mutable sequence of Python objects. Unlike tuples,
lists can be changed after creation: you can add, remove, and reorder elements.
This file contains 45 exercises covering list fundamentals and common idioms.

=== LIST OPERATORS & METHODS ===

1. INDEXING ([index])
   Description: Access an element by its position (0-based)
   Example: [10, 20, 30][1] = 20
   Example: [10, 20, 30][-1] = 30 (last element)

2. SLICING ([start:end:step])
   Description: Extract a portion of a list
   Example: [1, 2, 3, 4, 5][1:4] = [2, 3, 4]
   Example: [1, 2, 3, 4, 5][::-1] = [5, 4, 3, 2, 1] (reverse)

3. CONCATENATION (+)
   Description: Combine two lists into one new list
   Example: [1, 2] + [3, 4] = [1, 2, 3, 4]

4. REPETITION (*)
   Description: Repeat a list a specified number of times
   Example: [1, 2] * 3 = [1, 2, 1, 2, 1, 2]

5. LENGTH (len())
   Description: Get the number of elements in a list
   Example: len([1, 2, 3]) = 3

6. MEMBERSHIP (in / not in)
   Description: Check whether an element exists in a list
   Example: 2 in [1, 2, 3] = True
   Example: 5 not in [1, 2, 3] = True

7. APPEND (list.append())
   Description: Add a single element to the end (in place)
   Example: [1, 2].append(3) -> [1, 2, 3]

8. INSERT (list.insert(index, item))
   Description: Insert an element at a specific position (in place)
   Example: [1, 3].insert(1, 2) -> [1, 2, 3]

9. EXTEND (list.extend())
   Description: Append all elements of an iterable (in place)
   Example: [1, 2].extend([3, 4]) -> [1, 2, 3, 4]

10. REMOVE (list.remove(value))
    Description: Remove the first occurrence of a value (in place)
    Example: [1, 2, 2].remove(2) -> [1, 2]

11. POP (list.pop([index]))
    Description: Remove and return an element by index (default: last)
    Example: [1, 2, 3].pop(0) -> returns 1, list becomes [2, 3]

12. INDEX (list.index(value))
    Description: Find the first index of a value
    Example: [1, 2, 3, 2].index(2) = 1

13. COUNT (list.count(value))
    Description: Count occurrences of a value
    Example: [1, 2, 2, 3, 2].count(2) = 3

14. SORT (list.sort()) / SORTED (sorted())
    Description: .sort() reorders in place; sorted() returns a new list
    Example: [3, 1, 2].sort() -> [1, 2, 3]

15. REVERSE (list.reverse())
    Description: Reverse the list in place
    Example: [1, 2, 3].reverse() -> [3, 2, 1]

16. COPY (list.copy() / list[:])
    Description: Create an independent shallow copy
    Example: a = [1, 2]; b = a.copy()  (b is independent of a)

17. AGGREGATES (sum(), min(), max())
    Description: Quick statistics over numeric lists
    Example: sum([1, 2, 3]) = 6, min(...) = 1, max(...) = 3

18. LIST COMPREHENSION ([expr for item in iterable if cond])
    Description: Build a new list declaratively
    Example: [x**2 for x in [1, 2, 3]] = [1, 4, 9]
"""

from itertools import combinations
from typing import Any, cast


def exercise_one():
    """
    Exercise 1: Basic List Operations

    Problem: Access the third element, print the list length, and check if the
    list is empty.

    Purpose: This exercise introduces the fundamentals of working with lists:
    indexing, measuring size with len(), and using the truthiness of a list to
    detect emptiness.

    Given Input: numbers = [10, 20, 30, 40, 50]
    Expected Output: Third element: 30, Length: 5, Empty: False
    """
    numbers = [10, 20, 30, 40, 50]
    third_element = numbers[2]
    length = len(numbers)
    is_empty = len(numbers) == 0
    print(f"Third element: {third_element}, Length: {length}, Empty: {is_empty}")


def exercise_two():
    """
    Exercise 2: List Manipulation

    Problem: Change the second element to 200, append 600, insert 300 at index 2,
    remove 600, and remove the element at index 0.

    Purpose: This exercise demonstrates the core in-place mutation methods of a
    list. Unlike tuples, lists let you reshape their contents freely.

    Given Input: numbers = [100, 50, 400, 500]
    Expected Output: [200, 300, 400, 500]
    """
    numbers = [100, 50, 400, 500]
    numbers[1] = 200          # change second element
    numbers.append(600)       # add to the end
    numbers.insert(2, 300)    # insert at index 2
    numbers.remove(600)       # remove the value 600
    numbers.pop(0)            # remove element at index 0
    print(numbers)


def exercise_three():
    """
    Exercise 3: Sum and Average

    Problem: Calculate the total sum and the mean of the list items.

    Purpose: This exercise shows how built-in aggregate functions combine with
    len() to compute basic statistics without writing loops.

    Given Input: numbers = [10, 20, 30, 40, 50]
    Expected Output: Sum: 150, Average: 30.0
    """
    numbers = [10, 20, 30, 40, 50]
    total = sum(numbers)
    average = total / len(numbers)
    print(f"Sum: {total}, Average: {average}")


def exercise_four():
    """
    Exercise 4: Maximum and Minimum

    Problem: Find the largest and smallest values in the list.

    Purpose: This exercise reinforces that min() and max() work directly on any
    sequence, saving you from manual comparison loops.

    Given Input: numbers = [45, 12, 89, 2, 67]
    Expected Output: Maximum: 89, Minimum: 2
    """
    numbers = [45, 12, 89, 2, 67]
    print(f"Maximum: {max(numbers)}, Minimum: {min(numbers)}")


def exercise_five():
    """
    Exercise 5: Product of Elements

    Problem: Multiply all the numbers in the list together.

    Purpose: This exercise introduces the accumulator pattern, the foundation of
    any reduce-style aggregation where there is no single built-in for the job.

    Given Input: numbers = [2, 3, 5, 7]
    Expected Output: Product: 210
    """
    numbers = [2, 3, 5, 7]
    product = 1
    for n in numbers:
        product *= n
    print(f"Product: {product}")


def exercise_six():
    """
    Exercise 6: Count Even and Odd

    Problem: Categorize the numbers by parity and count how many are even and odd.

    Purpose: This exercise practices conditional counting using the modulo
    operator, a common building block in data validation and bucketing.

    Given Input: numbers = [10, 21, 4, 45, 66, 93, 11]
    Expected Output: Even: 3, Odd: 4
    """
    numbers = [10, 21, 4, 45, 66, 93, 11]
    even = len([n for n in numbers if n % 2 == 0])
    odd = len(numbers) - even
    print(f"Even: {even}, Odd: {odd}")


def exercise_seven():
    """
    Exercise 7: Reverse a List

    Problem: Reverse the order of elements in the list.

    Purpose: This exercise contrasts slicing ([::-1], which returns a new list)
    with the in-place .reverse() method, clarifying when each is appropriate.

    Given Input: numbers = [100, 200, 300, 400, 500]
    Expected Output: [500, 400, 300, 200, 100]
    """
    numbers = [100, 200, 300, 400, 500]
    reversed_numbers = numbers[::-1]
    print(reversed_numbers)


def exercise_eight():
    """
    Exercise 8: Sort Numbers

    Problem: Arrange the list in ascending order.

    Purpose: This exercise distinguishes sorted() (returns a new list) from
    .sort() (mutates in place), an important difference when the original order
    must be preserved.

    Given Input: numbers = [56, 12, 89, 3, 22]
    Expected Output: [3, 12, 22, 56, 89]
    """
    numbers = [56, 12, 89, 3, 22]
    print(sorted(numbers))


def exercise_nine():
    """
    Exercise 9: Copy a List

    Problem: Create an independent duplicate so that modifying the copy does not
    affect the original.

    Purpose: This exercise exposes the difference between assignment (which only
    creates a new reference) and a real copy. This is one of the most common
    sources of bugs for beginners.

    Given Input: fruits = ["Apple", "Banana", "Cherry"]
    Expected Output: Original and copy remain separate after modification
    """
    fruits = ["Apple", "Banana", "Cherry"]
    fruits_copy = fruits.copy()  # or fruits[:]
    fruits_copy.append("Date")
    print(f"Original: {fruits}")
    print(f"Copy: {fruits_copy}")


def exercise_ten():
    """
    Exercise 10: Combine Two Lists

    Problem: Merge two lists into a single sequence.

    Purpose: This exercise shows how the + operator builds a new combined list
    without mutating either source.

    Given Input: a = ["Physics", "Chemistry"], b = ["Maths", "Biology"]
    Expected Output: ['Physics', 'Chemistry', 'Maths', 'Biology']
    """
    a = ["Physics", "Chemistry"]
    b = ["Maths", "Biology"]
    print(a + b)


def exercise_eleven():
    """
    Exercise 11: Extract Middle Elements

    Problem: Slice the middle three items from the list.

    Purpose: This exercise reinforces slice notation for retrieving a contiguous
    subset of elements.

    Given Input: numbers = [10, 20, 30, 40, 50, 60, 70]
    Expected Output: [30, 40, 50]
    """
    numbers = [10, 20, 30, 40, 50, 60, 70]
    print(numbers[2:5])


def exercise_twelve():
    """
    Exercise 12: Swap Elements

    Problem: Exchange the positions of the items at indices 0 and 2.

    Purpose: This exercise applies Python's tuple-unpacking swap idiom to list
    elements, swapping by index without a temporary variable.

    Given Input: numbers = [23, 65, 19, 90]
    Expected Output: [19, 65, 23, 90]
    """
    numbers = [23, 65, 19, 90]
    numbers[0], numbers[2] = numbers[2], numbers[0]
    print(numbers)


def exercise_thirteen():
    """
    Exercise 13: Access Nested Lists

    Problem: Retrieve the value 5 from a nested list structure.

    Purpose: This exercise builds understanding of nested data structures by
    chaining index operators to drill down into sublists.

    Given Input: data = [[1, 2], [3, 4, 5], [6, 7]]
    Expected Output: 5
    """
    data = [[1, 2], [3, 4, 5], [6, 7]]
    print(data[1][2])


def exercise_fourteen():
    """
    Exercise 14: Membership Test

    Problem: Check whether "Tablet" exists in the inventory.

    Purpose: This exercise introduces membership testing with the in keyword, one
    of the most readable features of Python.

    Given Input: inventory = ["Laptop", "Mouse", "Monitor", "Keyboard"]
    Expected Output: False
    """
    inventory = ["Laptop", "Mouse", "Monitor", "Keyboard"]
    print("Tablet" in inventory)


def exercise_fifteen():
    """
    Exercise 15: Longest String

    Problem: Find the string with the most characters.

    Purpose: This exercise demonstrates the key parameter of max(), letting you
    rank items by a derived value (here, length) rather than the items themselves.

    Given Input: words = ["PHP", "Exercises", "Backend", "Python"]
    Expected Output: Exercises
    """
    words = ["PHP", "Exercises", "Backend", "Python"]
    print(max(words, key=len))


def exercise_sixteen():
    """
    Exercise 16: Square Every Item

    Problem: Transform each number into its square using a list comprehension.

    Purpose: This exercise introduces the list comprehension, Python's idiomatic
    way to map a transformation over a sequence.

    Given Input: numbers = [1, 2, 3, 4, 5]
    Expected Output: [1, 4, 9, 16, 25]
    """
    numbers = [1, 2, 3, 4, 5]
    print([n**2 for n in numbers])


def exercise_seventeen():
    """
    Exercise 17: Count Occurrences

    Problem: Tally how many times the value 10 appears.

    Purpose: This exercise uses the built-in .count() method to avoid a manual
    counting loop.

    Given Input: numbers = [10, 20, 30, 10, 40, 10, 50]
    Expected Output: 3 times
    """
    numbers = [10, 20, 30, 10, 40, 10, 50]
    print(f"{numbers.count(10)} times")


def exercise_eighteen():
    """
    Exercise 18: Remove All Occurrences

    Problem: Delete every instance of 20 from the list.

    Purpose: This exercise highlights why a comprehension (which builds a new
    filtered list) is safer than calling .remove() in a loop, which can skip
    elements while mutating during iteration.

    Given Input: numbers = [5, 20, 15, 20, 25, 50, 20]
    Expected Output: [5, 15, 25, 50]
    """
    numbers = [5, 20, 15, 20, 25, 50, 20]
    cleaned = [n for n in numbers if n != 20]
    print(cleaned)


def exercise_nineteen():
    """
    Exercise 19: Remove Empty Strings

    Problem: Filter out blank entries from the list.

    Purpose: This exercise leverages the truthiness of strings (an empty string
    is falsy) to filter concisely.

    Given Input: names = ["Mike", "", "Emma", "Kelly", "", "Brad"]
    Expected Output: ['Mike', 'Emma', 'Kelly', 'Brad']
    """
    names = ["Mike", "", "Emma", "Kelly", "", "Brad"]
    print([name for name in names if name])


def exercise_twenty():
    """
    Exercise 20: Remove Duplicates

    Problem: Keep only the unique values, preserving their first-seen order.

    Purpose: This exercise shows how dict.fromkeys() removes duplicates while
    keeping insertion order, unlike a plain set() which does not guarantee order.

    Given Input: numbers = [10, 20, 10, 30, 40, 40, 20, 50]
    Expected Output: [10, 20, 30, 40, 50]
    """
    numbers = [10, 20, 10, 30, 40, 40, 20, 50]
    unique = list(dict.fromkeys(numbers))
    print(unique)


def exercise_twenty_one():
    """
    Exercise 21: Filter Even Numbers

    Problem: Select only the even values using a list comprehension.

    Purpose: This exercise combines a comprehension with a condition, the most
    common form of declarative filtering.

    Given Input: numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    Expected Output: [2, 4, 6, 8, 10]
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print([n for n in numbers if n % 2 == 0])


def exercise_twenty_two():
    """
    Exercise 22: Index-wise Concatenation

    Problem: Combine two parallel lists element-by-element.

    Purpose: This exercise introduces zip() for processing corresponding elements
    of multiple sequences at once.

    Given Input: a = ["Py", "is", "awes"], b = ["thon", " ", "ome"]
    Expected Output: ['Python', 'is ', 'awesome']
    """
    a = ["Py", "is", "awes"]
    b = ["thon", " ", "ome"]
    print([x + y for x, y in zip(a, b)])


def exercise_twenty_three():
    """
    Exercise 23: Simultaneous Iteration

    Problem: Loop through two lists together using zip.

    Purpose: This exercise demonstrates iterating over paired data without
    manual index bookkeeping.

    Given Input: a = [10, 20, 30], b = [100, 200, 300]
    Expected Output: Paired output of corresponding elements
    """
    a = [10, 20, 30]
    b = [100, 200, 300]
    for x, y in zip(a, b):
        print(f"{x} -> {y}")


def exercise_twenty_four():
    """
    Exercise 24: Insert After Item

    Problem: Add 35 immediately after the value 30.

    Purpose: This exercise combines .index() (to locate a value) with .insert()
    (to place a new value at a computed position).

    Given Input: numbers = [10, 20, 30, 40, 50]
    Expected Output: [10, 20, 30, 35, 40, 50]
    """
    numbers = [10, 20, 30, 40, 50]
    position = numbers.index(30) + 1
    numbers.insert(position, 35)
    print(numbers)


def exercise_twenty_five():
    """
    Exercise 25: Replace if Found

    Problem: Change the first occurrence of 20 to 200.

    Purpose: This exercise shows the locate-then-assign pattern using .index()
    followed by assignment by index.

    Given Input: numbers = [5, 10, 15, 20, 25]
    Expected Output: [5, 10, 15, 200, 25]
    """
    numbers = [5, 10, 15, 20, 25]
    if 20 in numbers:
        numbers[numbers.index(20)] = 200
    print(numbers)


def exercise_twenty_six():
    """
    Exercise 26: Second Largest

    Problem: Find the second highest unique value.

    Purpose: This exercise shows how converting to a set removes duplicates
    before sorting, so the "second largest" is truly distinct.

    Given Input: numbers = [12, 35, 1, 10, 34, 1, 35]
    Expected Output: 34
    """
    numbers = [12, 35, 1, 10, 34, 1, 35]
    unique_sorted = sorted(set(numbers))
    print(unique_sorted[-2])


def exercise_twenty_seven():
    """
    Exercise 27: Most Frequent Element

    Problem: Identify the mode (the most frequently occurring element).

    Purpose: This exercise uses max() with a key based on .count(), a compact way
    to find the element that appears most often.

    Given Input: numbers = [1, 3, 3, 2, 1, 1, 4, 3, 3]
    Expected Output: 3
    """
    numbers = [1, 3, 3, 2, 1, 1, 4, 3, 3]
    most_frequent = max(set(numbers), key=numbers.count)
    print(most_frequent)


def exercise_twenty_eight():
    """
    Exercise 28: Every Nth Element

    Problem: Extract every 3rd item starting from index 0.

    Purpose: This exercise applies the step component of slice notation to sample
    a sequence at regular intervals.

    Given Input: letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g'], n = 3
    Expected Output: ['a', 'd', 'g']
    """
    letters = ["a", "b", "c", "d", "e", "f", "g"]
    n = 3
    print(letters[::n])


def exercise_twenty_nine():
    """
    Exercise 29: Palindrome Check

    Problem: Verify whether the list reads identically forwards and backwards.

    Purpose: This exercise compares a list with its reversed slice, a clean way
    to test for symmetry.

    Given Input: numbers = [1, 2, 3, 2, 1]
    Expected Output: True
    """
    numbers = [1, 2, 3, 2, 1]
    print(numbers == numbers[::-1])


def exercise_thirty():
    """
    Exercise 30: Common Elements

    Problem: Find the items present in all three lists.

    Purpose: This exercise uses set intersection to find the overlap across
    several collections efficiently.

    Given Input:
        a = [1, 5, 10, 20]
        b = [6, 7, 20, 80, 100]
        c = [3, 4, 15, 20, 30, 70, 80]
    Expected Output: [20]
    """
    a = [1, 5, 10, 20]
    b = [6, 7, 20, 80, 100]
    c = [3, 4, 15, 20, 30, 70, 80]
    common = list(set(a) & set(b) & set(c))
    print(common)


def exercise_thirty_one():
    """
    Exercise 31: Filter by Length

    Problem: Select strings whose length is greater than or equal to k.

    Purpose: This exercise combines a comprehension with len() to filter by a
    computed property of each element.

    Given Input: words = ["apple", "pie", "banana", "kiwi", "pear"], k = 5
    Expected Output: ['apple', 'banana']
    """
    words = ["apple", "pie", "banana", "kiwi", "pear"]
    k = 5
    print([w for w in words if len(w) >= k])


def exercise_thirty_two():
    """
    Exercise 32: Check if Sorted

    Problem: Verify whether the list is in ascending order.

    Purpose: This exercise compares a list against its own sorted version, a
    simple and readable sortedness test.

    Given Input: numbers = [10, 20, 30, 25, 40]
    Expected Output: False
    """
    numbers = [10, 20, 30, 25, 40]
    print(numbers == sorted(numbers))


def exercise_thirty_three():
    """
    Exercise 33: Convert to Dictionary

    Problem: Pair a list of keys with a list of values to build a dictionary.

    Purpose: This exercise combines zip() with dict() to construct a lookup table
    from two parallel lists.

    Given Input: keys = ["name", "age", "city"], values = ["Alice", 25, "New York"]
    Expected Output: {'name': 'Alice', 'age': 25, 'city': 'New York'}
    """
    keys = ["name", "age", "city"]
    values: list[Any] = ["Alice", 25, "New York"]
    print(dict(zip(keys, values)))


def exercise_thirty_four():
    """
    Exercise 34: List Difference

    Problem: Find the elements in the first list but not in the second.

    Purpose: This exercise uses set difference to compute which items are unique
    to one collection.

    Given Input: a = [1, 2, 3, 4, 5], b = [2, 4, 6]
    Expected Output: [1, 3, 5]
    """
    a = [1, 2, 3, 4, 5]
    b = [2, 4, 6]
    print([x for x in a if x not in b])


def exercise_thirty_five():
    """
    Exercise 35: Remove Negatives In-place

    Problem: Delete the negative numbers without creating a new list.

    Purpose: This exercise teaches in-place modification via slice assignment
    (numbers[:] = ...), which mutates the original object rather than rebinding
    the name. This matters when other references point to the same list.

    Given Input: numbers = [10, -5, 20, -1, 0, -8]
    Expected Output: [10, 20, 0]
    """
    numbers = [10, -5, 20, -1, 0, -8]
    numbers[:] = [n for n in numbers if n >= 0]
    print(numbers)


def exercise_thirty_six():
    """
    Exercise 36: Extend Nested Lists

    Problem: Add "elderberry" to each inner list.

    Purpose: This exercise iterates over sublists and mutates each one in place
    with .append(), reinforcing how nested mutable structures behave.

    Given Input: data = [['apple', 'banana'], ['cherry', 'date']]
    Expected Output: [['apple', 'banana', 'elderberry'], ['cherry', 'date', 'elderberry']]
    """
    data = [["apple", "banana"], ["cherry", "date"]]
    for inner in data:
        inner.append("elderberry")
    print(data)


def exercise_thirty_seven():
    """
    Exercise 37: Specific Order Concatenation

    Problem: Generate all combinations of elements from two lists.

    Purpose: This exercise uses a nested comprehension to build the Cartesian
    product of two sequences, a common pattern for generating pairings.

    Given Input: a = ["Hello ", "Take "], b = ["Dear", "Sir"]
    Expected Output: ['Hello Dear', 'Hello Sir', 'Take Dear', 'Take Sir']
    """
    a = ["Hello ", "Take "]
    b = ["Dear", "Sir"]
    print([x + y for x in a for y in b])


def exercise_thirty_eight():
    """
    Exercise 38: Flatten 2D List

    Problem: Convert a 2D (one level deep) list into a single flat list.

    Purpose: This exercise uses a nested comprehension to flatten one level of
    nesting concisely.

    Given Input: data = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    Expected Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    data = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    flat = [item for sublist in data for item in sublist]
    print(flat)


def exercise_thirty_nine():
    """
    Exercise 39: Deep Flatten (Recursion)

    Problem: Flatten an arbitrarily nested list structure.

    Purpose: This exercise strengthens recursion and type-checking skills.
    Flattening structures of unknown depth requires recursing into each list
    until only scalar values remain.

    Given Input: data = [1, [2, [3, 4], 5], 6, [7, 8]]
    Expected Output: [1, 2, 3, 4, 5, 6, 7, 8]
    """

    def flatten(nested: list[Any]) -> list[Any]:
        flat: list[Any] = []
        for item in nested:
            if isinstance(item, list):
                flat.extend(flatten(cast(list[Any], item)))  # recurse into the sublist
            else:
                flat.append(item)
        return flat

    data: list[Any] = [1, [2, [3, 4], 5], 6, [7, 8]]
    print(flatten(data))


def exercise_forty():
    """
    Exercise 40: Cumulative Sum

    Problem: Transform the list into the running total at each position.

    Purpose: This exercise demonstrates the running-accumulator pattern, the
    basis of prefix sums used in analytics and dynamic programming.

    Given Input: numbers = [10, 20, 30, 40]
    Expected Output: [10, 30, 60, 100]
    """
    numbers = [10, 20, 30, 40]
    running = 0
    result: list[int] = []
    for n in numbers:
        running += n
        result.append(running)
    print(result)


def exercise_forty_one():
    """
    Exercise 41: Rotate List

    Problem: Shift the elements left by k positions.

    Purpose: This exercise uses slicing to rotate a sequence, a neat alternative
    to element-by-element shifting.

    Given Input: numbers = [1, 2, 3, 4, 5], k = 2
    Expected Output: [3, 4, 5, 1, 2]
    """
    numbers = [1, 2, 3, 4, 5]
    k = 2
    rotated = numbers[k:] + numbers[:k]
    print(rotated)


def exercise_forty_two():
    """
    Exercise 42: Split into Chunks

    Problem: Divide the list into sublists of size N.

    Purpose: This exercise uses range() with a step and slicing to partition a
    sequence into fixed-size batches, common in pagination and batch processing.

    Given Input: numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], N = 3
    Expected Output: [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    n = 3
    chunks = [numbers[i : i + n] for i in range(0, len(numbers), n)]
    print(chunks)


def exercise_forty_three():
    """
    Exercise 43: Move Zeros to End

    Problem: Push all zeros to the right while preserving the order of the rest.

    Purpose: This exercise demonstrates stable partitioning: separate the
    non-zero values (keeping order) and pad the remainder with zeros.

    Given Input: numbers = [0, 1, 0, 3, 12]
    Expected Output: [1, 3, 12, 0, 0]
    """
    numbers = [0, 1, 0, 3, 12]
    non_zeros = [n for n in numbers if n != 0]
    zeros = [0] * (len(numbers) - len(non_zeros))
    print(non_zeros + zeros)


def exercise_forty_four():
    """
    Exercise 44: Generate Primes

    Problem: Create a list of prime numbers up to n using a comprehension.

    Purpose: This exercise combines a list comprehension with a helper predicate,
    showing how to express a filtered generation declaratively.

    Given Input: n = 20
    Expected Output: [2, 3, 5, 7, 11, 13, 17, 19]
    """

    def is_prime(num: int) -> bool:
        if num < 2:
            return False
        for divisor in range(2, int(num**0.5) + 1):
            if num % divisor == 0:
                return False
        return True

    n = 20
    primes = [x for x in range(2, n + 1) if is_prime(x)]
    print(primes)


def exercise_forty_five():
    """
    Exercise 45: Power Set

    Problem: Find all possible subsets of the list.

    Purpose: This exercise uses itertools.combinations to generate every subset
    of each size, building the complete power set. It connects combinatorics with
    Python's standard library tooling.

    Given Input: numbers = [1, 2, 3]
    Expected Output: [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    """
    numbers = [1, 2, 3]
    power_set: list[list[int]] = []
    for size in range(len(numbers) + 1):
        for subset in combinations(numbers, size):
            power_set.append(list(subset))
    print(power_set)


if __name__ == "__main__":
    print("=== Exercise 1: Basic List Operations ===")
    exercise_one()

    print("\n=== Exercise 2: List Manipulation ===")
    exercise_two()

    print("\n=== Exercise 3: Sum and Average ===")
    exercise_three()

    print("\n=== Exercise 4: Maximum and Minimum ===")
    exercise_four()

    print("\n=== Exercise 5: Product of Elements ===")
    exercise_five()

    print("\n=== Exercise 6: Count Even and Odd ===")
    exercise_six()

    print("\n=== Exercise 7: Reverse a List ===")
    exercise_seven()

    print("\n=== Exercise 8: Sort Numbers ===")
    exercise_eight()

    print("\n=== Exercise 9: Copy a List ===")
    exercise_nine()

    print("\n=== Exercise 10: Combine Two Lists ===")
    exercise_ten()

    print("\n=== Exercise 11: Extract Middle Elements ===")
    exercise_eleven()

    print("\n=== Exercise 12: Swap Elements ===")
    exercise_twelve()

    print("\n=== Exercise 13: Access Nested Lists ===")
    exercise_thirteen()

    print("\n=== Exercise 14: Membership Test ===")
    exercise_fourteen()

    print("\n=== Exercise 15: Longest String ===")
    exercise_fifteen()

    print("\n=== Exercise 16: Square Every Item ===")
    exercise_sixteen()

    print("\n=== Exercise 17: Count Occurrences ===")
    exercise_seventeen()

    print("\n=== Exercise 18: Remove All Occurrences ===")
    exercise_eighteen()

    print("\n=== Exercise 19: Remove Empty Strings ===")
    exercise_nineteen()

    print("\n=== Exercise 20: Remove Duplicates ===")
    exercise_twenty()

    print("\n=== Exercise 21: Filter Even Numbers ===")
    exercise_twenty_one()

    print("\n=== Exercise 22: Index-wise Concatenation ===")
    exercise_twenty_two()

    print("\n=== Exercise 23: Simultaneous Iteration ===")
    exercise_twenty_three()

    print("\n=== Exercise 24: Insert After Item ===")
    exercise_twenty_four()

    print("\n=== Exercise 25: Replace if Found ===")
    exercise_twenty_five()

    print("\n=== Exercise 26: Second Largest ===")
    exercise_twenty_six()

    print("\n=== Exercise 27: Most Frequent Element ===")
    exercise_twenty_seven()

    print("\n=== Exercise 28: Every Nth Element ===")
    exercise_twenty_eight()

    print("\n=== Exercise 29: Palindrome Check ===")
    exercise_twenty_nine()

    print("\n=== Exercise 30: Common Elements ===")
    exercise_thirty()

    print("\n=== Exercise 31: Filter by Length ===")
    exercise_thirty_one()

    print("\n=== Exercise 32: Check if Sorted ===")
    exercise_thirty_two()

    print("\n=== Exercise 33: Convert to Dictionary ===")
    exercise_thirty_three()

    print("\n=== Exercise 34: List Difference ===")
    exercise_thirty_four()

    print("\n=== Exercise 35: Remove Negatives In-place ===")
    exercise_thirty_five()

    print("\n=== Exercise 36: Extend Nested Lists ===")
    exercise_thirty_six()

    print("\n=== Exercise 37: Specific Order Concatenation ===")
    exercise_thirty_seven()

    print("\n=== Exercise 38: Flatten 2D List ===")
    exercise_thirty_eight()

    print("\n=== Exercise 39: Deep Flatten (Recursion) ===")
    exercise_thirty_nine()

    print("\n=== Exercise 40: Cumulative Sum ===")
    exercise_forty()

    print("\n=== Exercise 41: Rotate List ===")
    exercise_forty_one()

    print("\n=== Exercise 42: Split into Chunks ===")
    exercise_forty_two()

    print("\n=== Exercise 43: Move Zeros to End ===")
    exercise_forty_three()

    print("\n=== Exercise 44: Generate Primes ===")
    exercise_forty_four()

    print("\n=== Exercise 45: Power Set ===")
    exercise_forty_five()
