"""
Sets: A Complete Guide to Unordered Collections of Unique Elements in Python

A set is a mutable, unordered collection that stores only unique, hashable elements.
Sets are optimized for membership testing and for mathematical operations such as
union, intersection, and difference. This file contains 31 exercises covering set
fundamentals and common idioms.

=== SET OPERATORS & METHODS ===

1. ADD (set.add(item))
   Description: Insert a single hashable element (in place; no-op if already present)
   Example: {1, 2}.add(3) -> {1, 2, 3}

2. UPDATE (set.update(*iterables))
   Description: Add all elements from one or more iterables (in place)
   Example: {1}.update([2, 3], (4,)) -> {1, 2, 3, 4}

3. REMOVE (set.remove(item))
   Description: Remove an element; raises KeyError if it is absent
   Example: {1, 2}.remove(2) -> {1}

4. DISCARD (set.discard(item))
   Description: Remove an element if present; does nothing if absent (no error)
   Example: {1, 2}.discard(9) -> {1, 2}

5. POP (set.pop())
   Description: Remove and return an arbitrary element; raises KeyError if empty
   Example: {1, 2, 3}.pop() -> returns some element

6. CLEAR (set.clear())
   Description: Remove every element, leaving an empty set
   Example: {1, 2}.clear() -> set()

7. UNION (| or set.union())
   Description: All elements present in either set
   Example: {1, 2} | {2, 3} = {1, 2, 3}

8. INTERSECTION (& or set.intersection())
   Description: Elements present in both sets
   Example: {1, 2, 3} & {2, 3, 4} = {2, 3}

9. DIFFERENCE (- or set.difference())
   Description: Elements in the first set but not in the second
   Example: {1, 2, 3} - {2, 3} = {1}

10. SYMMETRIC DIFFERENCE (^ or set.symmetric_difference())
    Description: Elements in either set but not in both
    Example: {1, 2, 3} ^ {2, 3, 4} = {1, 4}

11. IN-PLACE OPERATORS (|=, &=, -=, ^=)
    Description: update / intersection_update / difference_update / symmetric_difference_update
    Example: a = {1, 2}; a |= {3} -> a == {1, 2, 3}

12. SUBSET / SUPERSET (<=, >= and < , >)
    Description: <= subset, >= superset; < and > require proper (strict) containment
    Example: {1, 2} <= {1, 2, 3} = True ; {1, 2} < {1, 2} = False

13. ISDISJOINT (set.isdisjoint())
    Description: True when two sets share no elements
    Example: {1, 2}.isdisjoint({3, 4}) = True

14. MEMBERSHIP (in / not in)
    Description: Average O(1) lookup, far faster than a list's O(n) scan
    Example: 2 in {1, 2, 3} = True

15. LENGTH (len())
    Description: Number of unique elements
    Example: len({1, 2, 3}) = 3

16. AGGREGATES (sum(), min(), max())
    Description: Numeric reductions work directly on a set
    Example: max({3, 1, 2}) = 3

17. COPY (set.copy())
    Description: Independent shallow copy (assignment only aliases the same set)
    Example: b = a.copy()  (b is independent of a)

18. SET COMPREHENSION ({expr for item in iterable if cond})
    Description: Build a new set declaratively, deduplicating automatically
    Example: {x % 3 for x in range(6)} = {0, 1, 2}

19. FROZENSET (frozenset(iterable))
    Description: Immutable, hashable set; usable as a dict key or set element
    Example: frozenset([1, 2, 2]) = frozenset({1, 2})

Run:
    poetry run python cap_03_built-in/data-structures/3-set.py
"""

from typing import Any, cast


def exercise_one() -> None:
    """
    Exercise 1: Basic Set Operations

    Problem: Create a set, add an element, remove one with remove(), and discard
    another with discard().

    Purpose: This exercise introduces the core mutation methods and, crucially,
    the difference between remove() (raises KeyError if the item is missing) and
    discard() (silently does nothing). Choosing the right one prevents accidental
    crashes when you are not sure an element exists.

    Given Input: fruits = {"apple", "banana", "cherry"}
    Expected Output: progressively shows add, remove, and discard results
    """
    fruits = {"apple", "banana", "cherry"}
    fruits.add("mango")
    print(f"After add: {fruits}")

    fruits.remove("banana")  # remove() would raise KeyError if "banana" were absent
    print(f"After remove: {fruits}")

    fruits.discard("cherry")  # discard() removes safely
    fruits.discard("grape")   # ...and stays silent for an absent element
    print(f"After discard: {fruits}")


def exercise_two() -> None:
    """
    Exercise 2: Clear All Elements

    Problem: Remove all elements from a set while keeping the variable bound.

    Purpose: This exercise shows that .clear() empties the set in place rather
    than rebinding the name to a brand-new object. Any other reference to the same
    set therefore also sees it become empty.

    Given Input: colors = {"red", "green", "blue"}
    Expected Output: set()
    """
    colors = {"red", "green", "blue"}
    colors.clear()
    print(colors)


def exercise_three() -> None:
    """
    Exercise 3: Find the Length of a Set

    Problem: Determine the set size manually using a loop instead of len().

    Purpose: This exercise reinforces that a set is iterable. Counting by hand
    builds intuition for what len() does internally, even though len() is the
    correct tool in real code.

    Given Input: animals = {"cat", "dog", "bird", "fish"}
    Expected Output: Length of set: 4
    """
    animals = {"cat", "dog", "bird", "fish"}
    count = 0
    for _ in animals:
        count += 1
    print(f"Length of set: {count}")


def exercise_four() -> None:
    """
    Exercise 4: Check if a Set is Empty

    Problem: Test whether a set has no elements using conditional logic.

    Purpose: This exercise leverages the truthiness of containers: an empty set is
    falsy, so `if not data` is the idiomatic emptiness check (clearer than
    len(data) == 0).

    Given Input: data = set()
    Expected Output: The set is empty.
    """
    data: set[int] = set()
    if not data:
        print("The set is empty.")
    else:
        print("The set has elements.")


def exercise_five() -> None:
    """
    Exercise 5: Union of Sets

    Problem: Combine two sets into one containing all unique elements.

    Purpose: This exercise introduces the union operator (|), which merges sets
    while automatically discarding duplicates.

    Given Input: set_a = {1, 2, 3, 4}, set_b = {3, 4, 5, 6}
    Expected Output: Union: {1, 2, 3, 4, 5, 6}
    """
    set_a = {1, 2, 3, 4}
    set_b = {3, 4, 5, 6}
    print(f"Union: {set_a | set_b}")


def exercise_six() -> None:
    """
    Exercise 6: Intersection of Sets

    Problem: Find the elements common to both sets.

    Purpose: This exercise demonstrates the intersection operator (&), the natural
    tool for answering "what do these collections share?".

    Given Input: set_a = {1, 2, 3, 4}, set_b = {3, 4, 5, 6}
    Expected Output: Intersection: {3, 4}
    """
    set_a = {1, 2, 3, 4}
    set_b = {3, 4, 5, 6}
    print(f"Intersection: {set_a & set_b}")


def exercise_seven() -> None:
    """
    Exercise 7: Difference of Sets

    Problem: Identify the elements in Set A that do not appear in Set B.

    Purpose: This exercise shows the difference operator (-), which is directional:
    A - B is not the same as B - A.

    Given Input: set_a = {1, 2, 3, 4}, set_b = {3, 4, 5, 6}
    Expected Output: Difference (A - B): {1, 2}
    """
    set_a = {1, 2, 3, 4}
    set_b = {3, 4, 5, 6}
    print(f"Difference (A - B): {set_a - set_b}")


def exercise_eight() -> None:
    """
    Exercise 8: Symmetric Difference

    Problem: Find the elements in either set but not in both.

    Purpose: This exercise introduces the symmetric difference operator (^), which
    keeps exactly the elements that are unique to one side or the other.

    Given Input: set_a = {1, 2, 3, 4}, set_b = {3, 4, 5, 6}
    Expected Output: Symmetric Difference: {1, 2, 5, 6}
    """
    set_a = {1, 2, 3, 4}
    set_b = {3, 4, 5, 6}
    print(f"Symmetric Difference: {set_a ^ set_b}")


def exercise_nine() -> None:
    """
    Exercise 9: Find Max and Min

    Problem: Identify the largest and smallest values in a numeric set.

    Purpose: This exercise confirms that min() and max() work on sets just as they
    do on lists, since a set is a plain iterable of comparable values.

    Given Input: numbers = {42, 7, 19, 85, 3, 56}
    Expected Output: Max: 85, Min: 3
    """
    numbers = {42, 7, 19, 85, 3, 56}
    print(f"Max: {max(numbers)}, Min: {min(numbers)}")


def exercise_ten() -> None:
    """
    Exercise 10: Sum of Set Elements

    Problem: Calculate the total sum manually using a loop instead of sum().

    Purpose: This exercise practices the accumulator pattern over a set, again to
    illuminate what the built-in sum() does for you.

    Given Input: numbers = {10, 20, 30, 40, 50}
    Expected Output: Sum: 150
    """
    numbers = {10, 20, 30, 40, 50}
    total = 0
    for n in numbers:
        total += n
    print(f"Sum: {total}")


def exercise_eleven() -> None:
    """
    Exercise 11: Add a List of Elements

    Problem: Insert multiple items from a list into an existing set with .update().

    Purpose: This exercise shows that .update() accepts any iterable and merges its
    elements, deduplicating against what is already present.

    Given Input: fruits = {"apple", "banana"}, new_fruits = ["cherry", "mango", "apple"]
    Expected Output: Updated set: {'apple', 'banana', 'cherry', 'mango'}
    """
    fruits = {"apple", "banana"}
    new_fruits = ["cherry", "mango", "apple"]
    fruits.update(new_fruits)
    print(f"Updated set: {fruits}")


def exercise_twelve() -> None:
    """
    Exercise 12: Update with Multiple Iterables

    Problem: Add elements from a list, a tuple, and another set in a single call.

    Purpose: This exercise highlights that .update() is variadic: you can pass
    several iterables at once and it folds them all in.

    Given Input: base = {1, 2}, from_list = [3, 4], from_tuple = (5, 6), from_set = {7, 8}
    Expected Output: Updated set: {1, 2, 3, 4, 5, 6, 7, 8}
    """
    base = {1, 2}
    from_list = [3, 4]
    from_tuple = (5, 6)
    from_set = {7, 8}
    base.update(from_list, from_tuple, from_set)
    print(f"Updated set: {base}")


def exercise_thirteen() -> None:
    """
    Exercise 13: Check Subset and Superset

    Problem: Verify whether one set is contained within another and vice versa.

    Purpose: This exercise introduces .issubset() and .issuperset() for testing
    containment relationships between collections.

    Given Input: set_a = {1, 2, 3}, set_b = {1, 2, 3, 4, 5}
    Expected Output: Is set_a a subset of set_b? True
    """
    set_a = {1, 2, 3}
    set_b = {1, 2, 3, 4, 5}
    print(f"Is set_a a subset of set_b? {set_a.issubset(set_b)}")
    print(f"Is set_b a superset of set_a? {set_b.issuperset(set_a)}")


def exercise_fourteen() -> None:
    """
    Exercise 14: Intersection Check with isdisjoint()

    Problem: Test whether two sets share any common elements.

    Purpose: This exercise shows that .isdisjoint() is more efficient and more
    expressive than computing the full intersection just to check whether it is
    empty.

    Given Input: set_a = {1, 2, 3}, set_b = {4, 5, 6}
    Expected Output: Are the sets disjoint? True
    """
    set_a = {1, 2, 3}
    set_b = {4, 5, 6}
    print(f"Are the sets disjoint? {set_a.isdisjoint(set_b)}")


def exercise_fifteen() -> None:
    """
    Exercise 15: Set Difference Update

    Problem: Modify a set by removing every element that also appears in another set.

    Purpose: This exercise contrasts .difference_update() (mutates in place) with
    the - operator (returns a new set). Use the in-place form when you do not need
    to keep the original.

    Given Input: a = {1, 2, 3, 4, 5}, b = {3, 4, 5, 6, 7}
    Expected Output: a = {1, 2}
    """
    a = {1, 2, 3, 4, 5}
    b = {3, 4, 5, 6, 7}
    a.difference_update(b)
    print(f"a = {a}")


def exercise_sixteen() -> None:
    """
    Exercise 16: Set Intersection Update

    Problem: Keep only the elements that appear in both sets, modifying in place.

    Purpose: This exercise shows .intersection_update(), the in-place counterpart
    of the & operator.

    Given Input: a = {1, 2, 3, 4, 5}, b = {3, 4, 5, 6, 7}
    Expected Output: a = {3, 4, 5}
    """
    a = {1, 2, 3, 4, 5}
    b = {3, 4, 5, 6, 7}
    a.intersection_update(b)
    print(f"a = {a}")


def exercise_seventeen() -> None:
    """
    Exercise 17: Set Symmetric Difference Update

    Problem: Retain only the non-overlapping elements between two sets, in place.

    Purpose: This exercise shows .symmetric_difference_update(), the in-place
    counterpart of the ^ operator.

    Given Input: a = {1, 2, 3, 4, 5}, b = {3, 4, 5, 6, 7}
    Expected Output: a = {1, 2, 6, 7}
    """
    a = {1, 2, 3, 4, 5}
    b = {3, 4, 5, 6, 7}
    a.symmetric_difference_update(b)
    print(f"a = {a}")


def exercise_eighteen() -> None:
    """
    Exercise 18: Remove Items Simultaneously

    Problem: Delete several specific items from a set in one operation.

    Purpose: This exercise shows that removing a whole batch of elements is just a
    difference_update() against the set of items to drop, avoiding a manual loop of
    remove() calls.

    Given Input: items = {10, 20, 30, 40, 50, 60}, to_remove = {20, 40, 60}
    Expected Output: items = {10, 30, 50}
    """
    items = {10, 20, 30, 40, 50, 60}
    to_remove = {20, 40, 60}
    items.difference_update(to_remove)
    print(f"items = {items}")


def exercise_nineteen() -> None:
    """
    Exercise 19: The Pop Operation

    Problem: Remove and return an arbitrary element; handle the error on an empty
    set.

    Purpose: This exercise shows that .pop() removes an unpredictable element
    (sets are unordered) and raises KeyError when there is nothing left, which must
    be guarded with try/except.

    Given Input: s = {100, 200, 300}, then s = set()
    Expected Output: Popped: <some element>, then Error: pop from an empty set
    """
    s = {100, 200, 300}
    print(f"Popped: {s.pop()}")

    empty: set[int] = set()
    try:
        empty.pop()
    except KeyError as e:
        print(f"Error: {e}")


def exercise_twenty() -> None:
    """
    Exercise 20: Filter a Set

    Problem: Create a new set containing only the elements divisible by 3.

    Purpose: This exercise introduces the set comprehension with a condition, the
    declarative way to filter while guaranteeing uniqueness.

    Given Input: numbers = {1, 2, 3, 6, 7, 9, 12, 14, 15}
    Expected Output: divisible_by_3 = {3, 6, 9, 12, 15}
    """
    numbers = {1, 2, 3, 6, 7, 9, 12, 14, 15}
    divisible_by_3 = {n for n in numbers if n % 3 == 0}
    print(f"divisible_by_3 = {divisible_by_3}")


def exercise_twenty_one() -> None:
    """
    Exercise 21: Find Common Elements in Lists

    Problem: Locate the shared elements between two lists using set conversion.

    Purpose: This exercise demonstrates a classic trick: convert lists to sets so
    you can use the fast & operator, which also deduplicates the inputs for free.

    Given Input: list1 = [1, 2, 3, 4, 5, 3, 2], list2 = [3, 4, 5, 6, 7, 4, 5]
    Expected Output: common = {3, 4, 5}
    """
    list1 = [1, 2, 3, 4, 5, 3, 2]
    list2 = [3, 4, 5, 6, 7, 4, 5]
    common = set(list1) & set(list2)
    print(f"common = {common}")


def exercise_twenty_two() -> None:
    """
    Exercise 22: Count Unique Words

    Problem: Determine how many distinct words appear in a string.

    Purpose: This exercise combines str.split() with set() to count distinct items,
    a very common text-processing pattern.

    Given Input: text = "the cat sat on the mat the cat"
    Expected Output: Unique word count: 5
    """
    text = "the cat sat on the mat the cat"
    unique_words = set(text.split())
    print(f"Unique word count: {len(unique_words)}")


def exercise_twenty_three() -> None:
    """
    Exercise 23: Convert Set to Joined String

    Problem: Concatenate the set elements into a single string with a delimiter.

    Purpose: This exercise shows str.join() over a set. Because sets are unordered,
    the elements are sorted first so the output is deterministic.

    Given Input: tags = {"python", "set", "programming", "tutorial"}
    Expected Output: a single string with the tags joined by " | "
    """
    tags = {"python", "set", "programming", "tutorial"}
    joined = " | ".join(sorted(tags))
    print(joined)


def exercise_twenty_four() -> None:
    """
    Exercise 24: Proper Subset and Superset

    Problem: Check strict containment relationships using the < and > operators.

    Purpose: This exercise distinguishes <= / >= (allow equality) from < / > (which
    require the sets to differ). A set is a subset of itself but not a *proper*
    subset of itself.

    Given Input: a = {1, 2, 3}, b = {1, 2, 3, 4, 5}
    Expected Output: a is a proper subset of b: True, b is a proper superset of a: True
    """
    a = {1, 2, 3}
    b = {1, 2, 3, 4, 5}
    print(f"a is a proper subset of b: {a < b}")
    print(f"b is a proper superset of a: {b > a}")


def exercise_twenty_five() -> None:
    """
    Exercise 25: Frozen Set

    Problem: Create an immutable set and demonstrate that modifications raise errors.

    Purpose: This exercise introduces frozenset, the hashable, immutable cousin of
    set. Because a frozenset has no mutating methods, the call to .add() is reached
    dynamically (via cast) so the runtime AttributeError can be demonstrated without
    a static type error.

    Given Input: fs = frozenset([1, 2, 3, 4, 5])
    Expected Output: frozenset({1, 2, 3, 4, 5}), then an error on modification
    """
    fs = frozenset([1, 2, 3, 4, 5])
    print(f"frozenset: {fs}")
    try:
        cast(Any, fs).add(6)  # frozenset has no add(); this raises at runtime
    except AttributeError as e:
        print(f"Error: {e}")


def exercise_twenty_six() -> None:
    """
    Exercise 26: Set Comprehension

    Problem: Generate the squares of all even numbers from 1 to 20 in one line.

    Purpose: This exercise combines a comprehension's transform and filter clauses
    to build a set in a single expression.

    Given Input: numbers from 1 to 20 (inclusive)
    Expected Output: {4, 16, 36, 64, 100, 144, 196, 256, 324, 400}
    """
    squares_of_evens = {n**2 for n in range(1, 21) if n % 2 == 0}
    print(squares_of_evens)


def exercise_twenty_seven() -> None:
    """
    Exercise 27: Remove Duplicates (Preserving Order)

    Problem: Strip duplicate values from a list while keeping the original order.

    Purpose: This exercise highlights a key limitation: a plain set() deduplicates
    but loses order. dict.fromkeys() deduplicates AND preserves first-seen order,
    which is what this problem requires.

    Given Input: items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    Expected Output: [3, 1, 4, 5, 9, 2, 6]
    """
    items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    unique_ordered = list(dict.fromkeys(items))
    print(unique_ordered)


def exercise_twenty_eight() -> None:
    """
    Exercise 28: Multi-Set Difference

    Problem: Find the elements in Set A that are absent from both Set B and Set C.

    Purpose: This exercise chains difference operations (A - B - C), showing how set
    algebra composes cleanly across more than two collections.

    Given Input: A = {1..8}, B = {2, 4, 6}, C = {5, 7, 9}
    Expected Output: Result: {1, 3, 8}
    """
    a = {1, 2, 3, 4, 5, 6, 7, 8}
    b = {2, 4, 6}
    c = {5, 7, 9}
    print(f"Result: {a - b - c}")


def exercise_twenty_nine() -> None:
    """
    Exercise 29: Set of Tuples

    Problem: Demonstrate that tuples work as set elements but lists do not.

    Purpose: This exercise drives home the hashability rule: set elements must be
    hashable. Tuples of immutable values are hashable; lists are mutable and
    therefore unhashable, so building a set from them raises TypeError at runtime.

    Given Input: a set of tuples, then an attempt to build a set from lists
    Expected Output: {(1, 2), (3, 4), (5, 6)}, then Error: unhashable type: 'list'
    """
    set_of_tuples = {(1, 2), (3, 4), (5, 6)}
    print(f"Set of tuples: {set_of_tuples}")
    try:
        set_of_lists = set([[1, 2], [3, 4]])  # lists are unhashable
        print(set_of_lists)
    except TypeError as e:
        print(f"Error: {e}")


def exercise_thirty() -> None:
    """
    Exercise 30: Shallow Copy vs. Assignment

    Problem: Illustrate the difference between reference assignment and an
    independent copy.

    Purpose: This exercise exposes a frequent bug source: assignment (alias = original)
    creates a second name for the SAME object, so mutating through one is visible
    through the other. .copy() creates a separate object that is unaffected.

    Given Input: original = {1, 2, 3, 4, 5}
    Expected Output: shows the alias changing with the original, the copy staying put
    """
    original = {1, 2, 3, 4, 5}
    alias = original          # same object, just another name
    independent = original.copy()  # a separate object

    original.add(6)
    print(f"alias sees the change:        {alias}")
    print(f"independent copy is unchanged: {independent}")


def exercise_thirty_one() -> None:
    """
    Exercise 31: Membership Testing Performance

    Problem: Compare lookup speed between a list and a set on a large dataset.

    Purpose: This exercise gives concrete evidence for why sets exist: membership
    testing is O(n) in a list (a linear scan) but average O(1) in a set (a hash
    lookup). The gap is dramatic at scale, which is why sets are the right tool for
    "have I seen this?" checks.

    Given Input: 1,000,000 integers, searching for the worst-case value 999999
    Expected Output: the set lookup is orders of magnitude faster than the list
    """
    import time

    big_list = list(range(1_000_000))
    big_set = set(big_list)
    target = 999_999

    start = time.perf_counter()
    _ = target in big_list  # linear scan to the very end
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    _ = target in big_set   # single hash lookup
    set_time = time.perf_counter() - start

    print(f"List lookup time: {list_time:.6f} seconds")
    print(f"Set lookup time:  {set_time:.6f} seconds")


def main() -> None:
    print("=== Exercise 1: Basic Set Operations ===")
    exercise_one()

    print("\n=== Exercise 2: Clear All Elements ===")
    exercise_two()

    print("\n=== Exercise 3: Find the Length of a Set ===")
    exercise_three()

    print("\n=== Exercise 4: Check if a Set is Empty ===")
    exercise_four()

    print("\n=== Exercise 5: Union of Sets ===")
    exercise_five()

    print("\n=== Exercise 6: Intersection of Sets ===")
    exercise_six()

    print("\n=== Exercise 7: Difference of Sets ===")
    exercise_seven()

    print("\n=== Exercise 8: Symmetric Difference ===")
    exercise_eight()

    print("\n=== Exercise 9: Find Max and Min ===")
    exercise_nine()

    print("\n=== Exercise 10: Sum of Set Elements ===")
    exercise_ten()

    print("\n=== Exercise 11: Add a List of Elements ===")
    exercise_eleven()

    print("\n=== Exercise 12: Update with Multiple Iterables ===")
    exercise_twelve()

    print("\n=== Exercise 13: Check Subset and Superset ===")
    exercise_thirteen()

    print("\n=== Exercise 14: Intersection Check with isdisjoint() ===")
    exercise_fourteen()

    print("\n=== Exercise 15: Set Difference Update ===")
    exercise_fifteen()

    print("\n=== Exercise 16: Set Intersection Update ===")
    exercise_sixteen()

    print("\n=== Exercise 17: Set Symmetric Difference Update ===")
    exercise_seventeen()

    print("\n=== Exercise 18: Remove Items Simultaneously ===")
    exercise_eighteen()

    print("\n=== Exercise 19: The Pop Operation ===")
    exercise_nineteen()

    print("\n=== Exercise 20: Filter a Set ===")
    exercise_twenty()

    print("\n=== Exercise 21: Find Common Elements in Lists ===")
    exercise_twenty_one()

    print("\n=== Exercise 22: Count Unique Words ===")
    exercise_twenty_two()

    print("\n=== Exercise 23: Convert Set to Joined String ===")
    exercise_twenty_three()

    print("\n=== Exercise 24: Proper Subset and Superset ===")
    exercise_twenty_four()

    print("\n=== Exercise 25: Frozen Set ===")
    exercise_twenty_five()

    print("\n=== Exercise 26: Set Comprehension ===")
    exercise_twenty_six()

    print("\n=== Exercise 27: Remove Duplicates (Preserving Order) ===")
    exercise_twenty_seven()

    print("\n=== Exercise 28: Multi-Set Difference ===")
    exercise_twenty_eight()

    print("\n=== Exercise 29: Set of Tuples ===")
    exercise_twenty_nine()

    print("\n=== Exercise 30: Shallow Copy vs. Assignment ===")
    exercise_thirty()

    print("\n=== Exercise 31: Membership Testing Performance ===")
    exercise_thirty_one()


main()
