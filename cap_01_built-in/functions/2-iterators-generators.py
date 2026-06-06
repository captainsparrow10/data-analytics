"""
Iterators & Generators: A Complete Guide to Lazy Sequences in Python

An ITERABLE is anything you can loop over (it implements __iter__). An ITERATOR is the
object that actually produces values one at a time (it implements __next__ and raises
StopIteration when exhausted). A GENERATOR is the easiest way to build an iterator:
a function that uses `yield` to produce values lazily, suspending and resuming its
state between calls. Lazy evaluation means values are computed on demand, so you can
model infinite or very large sequences without holding them all in memory. This file
contains 30 exercises covering iterators and generators.

=== ITERATOR & GENERATOR CONCEPTS ===

1. ITERABLE vs ITERATOR
   Description: iter(iterable) returns an iterator; next(iterator) advances it
   Example: it = iter([1, 2]); next(it) = 1

2. STOPITERATION
   Description: The signal an iterator raises when there are no more values
   Example: caught with try/except in manual iteration

3. GENERATOR FUNCTION (yield)
   Description: A function that yields values lazily, resuming where it left off
   Example: def gen(): yield 1; yield 2

4. GENERATOR EXPRESSION ((expr for ...))
   Description: A lazy comprehension; like a list comp but produced on demand
   Example: (x * x for x in range(3))

5. YIELD FROM
   Description: Delegate iteration to a sub-iterable (great for recursion)
   Example: yield from other_gen()

6. INFINITE GENERATORS
   Description: A generator with no natural end; consume with islice/break
   Example: while True: yield n; n += 1

7. CLASS-BASED ITERATOR (__iter__ / __next__)
   Description: Build an iterator manually by implementing the iterator protocol
   Example: class It: def __next__(self): ...

8. COROUTINE METHODS (send / throw / close)
   Description: Two-way generators: feed values in, inject exceptions, or stop early
   Example: total = yield ; gen.send(10)

9. RESOURCE SAFETY (try/finally in generators)
   Description: finally runs even if the generator is closed early, freeing resources
   Example: try: yield row finally: close()

10. LAZY EVALUATION / MEMORY
    Description: Values are produced on demand, enabling streaming over huge inputs
    Example: reading a file line by line instead of loading it whole
"""

import itertools
import tempfile
from pathlib import Path
from typing import Any, Generator, Iterable, Iterator, cast


def exercise_one():
    """
    Exercise 1: The Square Generator

    Problem: Create a generator that yields the squares of numbers from 1 to n.

    Purpose: This exercise introduces the simplest generator function: a `yield`
    inside a loop produces one value per iteration, lazily.

    Given Input: n = 5
    Expected Output: 1 4 9 16 25
    """
    def squares(n: int) -> Iterator[int]:
        for i in range(1, n + 1):
            yield i * i

    print(*squares(5))


def exercise_two():
    """
    Exercise 2: Even Number Iterator

    Problem: Write a class-based iterator that returns even numbers up to a limit.

    Purpose: This exercise implements the iterator protocol by hand: __iter__ returns
    the iterator object, and __next__ advances the state and raises StopIteration when
    the limit is passed.

    Given Input: limit = 10
    Expected Output: 0 2 4 6 8 10
    """
    class EvenNumbers:
        def __init__(self, limit: int) -> None:
            self.limit = limit
            self.current = 0

        def __iter__(self) -> "EvenNumbers":
            return self

        def __next__(self) -> int:
            if self.current > self.limit:
                raise StopIteration
            value = self.current
            self.current += 2
            return value

    print(*EvenNumbers(10))


def exercise_three():
    """
    Exercise 3: Custom Range

    Problem: Re-implement a simplified range() using a generator.

    Purpose: This exercise shows how range's lazy behavior can be reproduced with a
    simple while loop and yield.

    Given Input: start = 2, stop = 10, step = 2
    Expected Output: 2 4 6 8
    """
    def my_range(start: int, stop: int, step: int = 1) -> Iterator[int]:
        current = start
        while current < stop:
            yield current
            current += step

    print(*my_range(2, 10, 2))


def exercise_four():
    """
    Exercise 4: Reverse String Iterator

    Problem: Write an iterator class that returns a string's characters in reverse.

    Purpose: This exercise stores an index that walks backward, yielding one character
    per __next__ call until it reaches the start.

    Given Input: text = "hello"
    Expected Output: o l l e h
    """
    class ReverseString:
        def __init__(self, text: str) -> None:
            self.text = text
            self.index = len(text)

        def __iter__(self) -> "ReverseString":
            return self

        def __next__(self) -> str:
            if self.index == 0:
                raise StopIteration
            self.index -= 1
            return self.text[self.index]

    print(*ReverseString("hello"))


def exercise_five():
    """
    Exercise 5: Vowel Filter

    Problem: Create a generator that yields only the vowels found in a string.

    Purpose: This exercise filters inside a generator, yielding selectively rather
    than building a list.

    Given Input: text = "Hello, World!"
    Expected Output: e o o
    """
    def vowels(text: str) -> Iterator[str]:
        for char in text:
            if char.lower() in "aeiou":
                yield char

    print(*vowels("Hello, World!"))


def exercise_six():
    """
    Exercise 6: Power of Two

    Problem: Write a generator expression that yields powers of 2.

    Purpose: This exercise introduces the generator expression: the same syntax as a
    list comprehension but with parentheses, producing values lazily.

    Given Input: n = 8
    Expected Output: 1 2 4 8 16 32 64 128
    """
    n = 8
    powers = (2**i for i in range(n))
    print(*powers)


def exercise_seven():
    """
    Exercise 7: Finite Fibonacci

    Problem: Produce the first n Fibonacci numbers with a generator.

    Purpose: This exercise keeps two running variables across yields, demonstrating
    how a generator preserves state between resumptions.

    Given Input: n = 8
    Expected Output: 0 1 1 2 3 5 8 13
    """
    def fibonacci(n: int) -> Iterator[int]:
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b

    print(*fibonacci(8))


def exercise_eight():
    """
    Exercise 8: Infinite Counter

    Problem: Create a generator that counts up from 1 forever.

    Purpose: This exercise shows an infinite generator. Because it never ends on its
    own, the caller must bound it (here with itertools.islice).

    Given Input: print values until the counter reaches 5
    Expected Output: 1 2 3 4 5
    """
    def count_up() -> Iterator[int]:
        n = 1
        while True:
            yield n
            n += 1

    print(*itertools.islice(count_up(), 5))


def exercise_nine():
    """
    Exercise 9: Manual Iteration

    Problem: Use iter() and next() to print each element, catching StopIteration.

    Purpose: This exercise exposes what a for loop does internally: get an iterator,
    repeatedly call next(), and stop when StopIteration is raised.

    Given Input: numbers = [10, 20, 30]
    Expected Output: 10 20 30
    """
    numbers = [10, 20, 30]
    iterator = iter(numbers)
    while True:
        try:
            print(next(iterator), end=" ")
        except StopIteration:
            break
    print()


def exercise_ten():
    """
    Exercise 10: Step Iterator

    Problem: Create an iterator over start..stop with a step that may be a float.

    Purpose: This exercise generalizes range to floats (which range cannot do),
    using a while loop and accumulation.

    Given Input: start = 0.0, stop = 1.0, step = 0.25
    Expected Output: 0.0 0.25 0.5 0.75
    """
    def frange(start: float, stop: float, step: float) -> Iterator[float]:
        current = start
        while current < stop:
            yield current
            current += step

    print(*frange(0.0, 1.0, 0.25))


def exercise_eleven():
    """
    Exercise 11: File Line Reader

    Problem: Write a generator that reads a large text file line by line, avoiding a
    full in-memory load.

    Purpose: This exercise demonstrates the canonical memory-saving use of generators.
    A temporary file is created so the exercise is self-contained and runnable.

    Given Input: a text file with three lines
    Expected Output: the three lines printed in order
    """
    def read_lines(path: Path) -> Iterator[str]:
        with path.open() as file:
            for line in file:
                yield line.rstrip("\n")

    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "data.txt"
        data_file.write_text("first line\nsecond line\nthird line\n")
        for line in read_lines(data_file):
            print(line)


def exercise_twelve():
    """
    Exercise 12: CSV Row Parser

    Problem: Create a generator yielding CSV rows as dictionaries, using the first row
    as the keys.

    Purpose: This exercise builds a per-row dict by zipping the header with each data
    row, a streaming parser that never holds the whole file in memory.

    Given Input: a CSV with name, age, city columns and three data rows
    Expected Output: three dicts, one per row
    """
    def parse_csv(path: Path) -> Iterator[dict[str, str]]:
        with path.open() as file:
            header = file.readline().strip().split(",")
            for line in file:
                values = line.strip().split(",")
                yield dict(zip(header, values))

    with tempfile.TemporaryDirectory() as tmp:
        csv_file = Path(tmp) / "people.csv"
        csv_file.write_text(
            "name,age,city\nAlice,30,NYC\nBob,25,LA\nCarol,40,SF\n"
        )
        for row in parse_csv(csv_file):
            print(row)


def exercise_thirteen():
    """
    Exercise 13: The Pipeline

    Problem: Create one generator yielding numbers and another squaring them, then
    pipe the first into the second.

    Purpose: This exercise shows generator composition: the output of one generator is
    the input iterable of the next, forming a lazy processing pipeline.

    Given Input: numbers = [1, 2, 3, 4, 5]
    Expected Output: 1 4 9 16 25
    """
    def gen_numbers(nums: list[int]) -> Iterator[int]:
        for n in nums:
            yield n

    def gen_squares(source: Iterable[int]) -> Iterator[int]:
        for n in source:
            yield n * n

    print(*gen_squares(gen_numbers([1, 2, 3, 4, 5])))


def exercise_fourteen():
    """
    Exercise 14: List Flattener

    Problem: Use `yield from` to recursively flatten a nested list.

    Purpose: This exercise shows `yield from`, which delegates to a sub-generator. For
    a nested list it recurses; for a scalar it yields directly. The isinstance check is
    narrowed with cast so the recursive call stays type-clean.

    Given Input: nested = [1, [2, [3, 4], 5], [6, 7], 8]
    Expected Output: 1 2 3 4 5 6 7 8
    """
    def flatten(nested: list[Any]) -> Iterator[Any]:
        for item in nested:
            if isinstance(item, list):
                yield from flatten(cast(list[Any], item))
            else:
                yield item

    nested: list[Any] = [1, [2, [3, 4], 5], [6, 7], 8]
    print(*flatten(nested))


def exercise_fifteen():
    """
    Exercise 15: Batch Processing

    Problem: Write a generator that yields chunks of a given size from an iterable.

    Purpose: This exercise accumulates items into a batch and yields it when full,
    flushing any remainder at the end, a common pattern for paging large streams.

    Given Input: items = list(range(1, 11)), batch_size = 3
    Expected Output: [1, 2, 3] [4, 5, 6] [7, 8, 9] [10]
    """
    def batched(iterable: Iterable[int], size: int) -> Iterator[list[int]]:
        batch: list[int] = []
        for item in iterable:
            batch.append(item)
            if len(batch) == size:
                yield batch
                batch = []
        if batch:
            yield batch

    for chunk in batched(list(range(1, 11)), 3):
        print(chunk)


def exercise_sixteen():
    """
    Exercise 16: Prime Sieve

    Problem: Implement a generator yielding primes using Sieve of Eratosthenes logic.

    Purpose: This exercise marks composite multiples as they are found and yields each
    prime lazily.

    Given Input: limit = 30
    Expected Output: 2 3 5 7 11 13 17 19 23 29
    """
    def primes(limit: int) -> Iterator[int]:
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
        for num in range(2, limit + 1):
            if is_prime[num]:
                yield num
                for multiple in range(num * num, limit + 1, num):
                    is_prime[multiple] = False

    print(*primes(30))


def exercise_seventeen():
    """
    Exercise 17: Running Average

    Problem: Create a generator that yields the running average as numbers arrive.

    Purpose: This exercise keeps a running total and count across yields, dividing to
    produce the average after each new value.

    Given Input: numbers = [10, 20, 30, 40, 50]
    Expected Output: 10.0 15.0 20.0 25.0 30.0
    """
    def running_average(numbers: list[int]) -> Iterator[float]:
        total = 0
        for index, value in enumerate(numbers, start=1):
            total += value
            yield total / index

    print(*running_average([10, 20, 30, 40, 50]))


def exercise_eighteen():
    """
    Exercise 18: Sliding Window

    Problem: Write a generator yielding a sliding window of size n over a sequence.

    Purpose: This exercise yields successive overlapping slices, a staple of
    time-series and sequence analysis.

    Given Input: sequence = [1, 2, 3, 4, 5], n = 3
    Expected Output: (1, 2, 3) (2, 3, 4) (3, 4, 5)
    """
    def sliding_window(seq: list[int], n: int) -> Iterator[tuple[int, ...]]:
        for i in range(len(seq) - n + 1):
            yield tuple(seq[i:i + n])

    print(*sliding_window([1, 2, 3, 4, 5], 3))


def exercise_nineteen():
    """
    Exercise 19: Log Filter

    Problem: Create a generator parsing a log file, yielding only lines containing a
    keyword.

    Purpose: This exercise streams a file and yields only matching lines, never holding
    the whole log in memory. A temporary log file makes it self-contained.

    Given Input: a log with INFO, ERROR, and WARNING entries; keyword "ERROR"
    Expected Output: only the ERROR lines
    """
    def filter_lines(path: Path, keyword: str) -> Iterator[str]:
        with path.open() as file:
            for line in file:
                if keyword in line:
                    yield line.rstrip("\n")

    with tempfile.TemporaryDirectory() as tmp:
        log_file = Path(tmp) / "app.log"
        log_file.write_text(
            "INFO: started\n"
            "ERROR: disk full\n"
            "WARNING: low memory\n"
            "ERROR: timeout\n"
        )
        for line in filter_lines(log_file, "ERROR"):
            print(line)


def exercise_twenty():
    """
    Exercise 20: Unique Element Filter

    Problem: Write a generator yielding unique elements in order of first appearance.

    Purpose: This exercise keeps a `seen` set and yields each value only the first
    time it is encountered, preserving order (unlike a plain set).

    Given Input: items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    Expected Output: 3 1 4 5 9 2 6
    """
    def unique(items: list[int]) -> Iterator[int]:
        seen: set[int] = set()
        for item in items:
            if item not in seen:
                seen.add(item)
                yield item

    print(*unique([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]))


def exercise_twenty_one():
    """
    Exercise 21: The Accumulator (send)

    Problem: Create a coroutine using yield to receive values via send() and keep a
    running total.

    Purpose: This exercise introduces two-way generators. `value = yield total` both
    emits the current total AND pauses to receive the next value sent in. The
    generator must be primed with next() before the first send().

    Given Input: send 10, 20, 30 one at a time
    Expected Output: 10 30 60
    """
    def accumulator() -> Generator[int, int, None]:
        total = 0
        while True:
            value = yield total
            total += value

    acc = accumulator()
    next(acc)  # prime: run up to the first yield
    print(acc.send(10), acc.send(20), acc.send(30))


def exercise_twenty_two():
    """
    Exercise 22: Custom Zip

    Problem: Re-implement zip() using iter() and next().

    Purpose: This exercise shows how zip works internally: pull one item from each
    iterator per step, and stop as soon as any of them is exhausted.

    Given Input: a = [1, 2, 3], b = ["a", "b", "c"]
    Expected Output: (1, 'a') (2, 'b') (3, 'c')
    """
    def my_zip(a: list[int], b: list[str]) -> Iterator[tuple[int, str]]:
        it_a, it_b = iter(a), iter(b)
        while True:
            try:
                x = next(it_a)
                y = next(it_b)
            except StopIteration:
                return  # any iterator exhausted -> stop
            yield (x, y)

    print(*my_zip([1, 2, 3], ["a", "b", "c"]))


def exercise_twenty_three():
    """
    Exercise 23: Binary Tree Traversal

    Problem: Implement in-order traversal of a Binary Search Tree with a recursive
    generator.

    Purpose: This exercise combines recursion with `yield from`: in-order traversal
    visits left subtree, then the node, then the right subtree, which yields a BST's
    values in sorted order.

    Given Input: BST built from 5, 3, 7, 2, 4, 6, 8
    Expected Output: 2 3 4 5 6 7 8
    """
    class TreeNode:
        def __init__(self, value: int) -> None:
            self.value = value
            self.left: "TreeNode | None" = None
            self.right: "TreeNode | None" = None

    def insert(root: "TreeNode | None", value: int) -> "TreeNode":
        if root is None:
            return TreeNode(value)
        if value < root.value:
            root.left = insert(root.left, value)
        else:
            root.right = insert(root.right, value)
        return root

    def inorder(node: "TreeNode | None") -> Iterator[int]:
        if node is not None:
            yield from inorder(node.left)
            yield node.value
            yield from inorder(node.right)

    root: "TreeNode | None" = None
    for number in [5, 3, 7, 2, 4, 6, 8]:
        root = insert(root, number)
    print(*inorder(root))


def exercise_twenty_four():
    """
    Exercise 24: Data Throttler

    Problem: Create a generator yielding every n-th item of another iterable.

    Purpose: This exercise uses enumerate with a 1-based start and a modulo test to
    sample a stream at a fixed interval.

    Given Input: data = list(range(1, 21)), n = 4
    Expected Output: 4 8 12 16 20
    """
    def throttle(data: list[int], n: int) -> Iterator[int]:
        for index, item in enumerate(data, start=1):
            if index % n == 0:
                yield item

    print(*throttle(list(range(1, 21)), 4))


def exercise_twenty_five():
    """
    Exercise 25: Generator State Machine

    Problem: Use a generator to represent a Traffic Light cycling through its states.

    Purpose: This exercise models a state machine: an infinite generator that yields
    states in a fixed cycle, advanced one transition at a time.

    Given Input: advance through 6 transitions
    Expected Output: Green Yellow Red Green Yellow Red
    """
    def traffic_light() -> Iterator[str]:
        while True:
            yield "Green"
            yield "Yellow"
            yield "Red"

    print(*itertools.islice(traffic_light(), 6))


def exercise_twenty_six():
    """
    Exercise 26: Peekable Iterator

    Problem: Wrap an iterator so you can "peek" at the next value without consuming it.

    Purpose: This exercise caches one look-ahead value. peek() fills the cache without
    advancing; __next__ returns the cached value if present, otherwise pulls a fresh
    one.

    Given Input: data = [10, 20, 30, 40]
    Expected Output: interleaved peek and consume operations
    """
    class Peekable:
        def __init__(self, iterable: Iterable[int]) -> None:
            self._iterator = iter(iterable)
            self._cache: list[int] = []

        def __iter__(self) -> "Peekable":
            return self

        def peek(self) -> int:
            if not self._cache:
                self._cache.append(next(self._iterator))
            return self._cache[0]

        def __next__(self) -> int:
            if self._cache:
                return self._cache.pop(0)
            return next(self._iterator)

    peekable = Peekable([10, 20, 30, 40])
    print(f"peek: {peekable.peek()}")
    print(f"next: {next(peekable)}")
    print(f"peek: {peekable.peek()}")
    print(f"next: {next(peekable)}")
    print(f"next: {next(peekable)}")


def exercise_twenty_seven():
    """
    Exercise 27: Exception Handler

    Problem: Create a generator using throw() to handle a specific error during
    execution.

    Purpose: This exercise shows gen.throw(): an exception is injected at the paused
    yield. Because the yield is wrapped in try/except, the generator catches it and
    resumes with the next value instead of dying.

    Given Input: a sequence with a ValueError thrown after the second value
    Expected Output: values printed with the error caught and iteration continuing
    """
    def resilient() -> Generator[int, None, None]:
        for i in range(1, 6):
            try:
                yield i
            except ValueError:
                print(f"  caught ValueError at {i}, continuing")

    gen = resilient()
    print(next(gen))
    print(next(gen))
    print(gen.throw(ValueError))  # injected at the paused yield, caught inside
    print(next(gen))
    print(next(gen))


def exercise_twenty_eight():
    """
    Exercise 28: Recursive Directory Walker

    Problem: Write a generator yielding all file paths in a directory and its
    subdirectories.

    Purpose: This exercise recurses into subdirectories with `yield from`, streaming
    file paths one at a time. A temporary directory tree makes it self-contained;
    only file names are printed so the output is deterministic.

    Given Input: a directory tree with a file in the root and one in a subdirectory
    Expected Output: every file's name, in order
    """
    def walk(path: Path) -> Iterator[Path]:
        for entry in sorted(path.iterdir()):
            if entry.is_dir():
                yield from walk(entry)
            else:
                yield entry

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        (base / "a.txt").write_text("x")
        subdir = base / "sub"
        subdir.mkdir()
        (subdir / "b.txt").write_text("y")
        for file_path in walk(base):
            print(file_path.name)


def exercise_twenty_nine():
    """
    Exercise 29: Interleaved Streams

    Problem: Write a generator yielding elements from two iterables alternately, even
    when they differ in length.

    Purpose: This exercise uses itertools.zip_longest with a sentinel fill value so
    that, once the shorter iterable runs out, the remaining items of the longer one
    are still yielded. Mixed element types make the yield type Any.

    Given Input: a = [1, 2, 3], b = ["a", "b", "c", "d"]
    Expected Output: 1 a 2 b 3 c d
    """
    def interleave(a: list[int], b: list[str]) -> Iterator[Any]:
        sentinel = object()
        for x, y in itertools.zip_longest(a, b, fillvalue=sentinel):
            if x is not sentinel:
                yield x
            if y is not sentinel:
                yield y

    print(*interleave([1, 2, 3], ["a", "b", "c", "d"]))


def exercise_thirty():
    """
    Exercise 30: Generator Cleanup

    Problem: Use try...finally inside a generator to guarantee resource closure even
    if the generator is closed early.

    Purpose: This exercise shows that a generator's `finally` block runs when the
    generator is garbage-collected OR explicitly closed with .close(), making it the
    right place to release resources.

    Given Input: a simulated database whose generator is closed after the first row
    Expected Output: connection opened, first row, connection closed
    """
    def db_reader() -> Generator[str, None, None]:
        print("  connection opened")
        try:
            for row in ["row-1", "row-2", "row-3"]:
                yield row
        finally:
            print("  connection closed")

    reader = db_reader()
    print(next(reader))  # opens the connection, yields the first row
    reader.close()       # triggers the finally block early


if __name__ == "__main__":
    print("=== Exercise 1: The Square Generator ===")
    exercise_one()

    print("\n=== Exercise 2: Even Number Iterator ===")
    exercise_two()

    print("\n=== Exercise 3: Custom Range ===")
    exercise_three()

    print("\n=== Exercise 4: Reverse String Iterator ===")
    exercise_four()

    print("\n=== Exercise 5: Vowel Filter ===")
    exercise_five()

    print("\n=== Exercise 6: Power of Two ===")
    exercise_six()

    print("\n=== Exercise 7: Finite Fibonacci ===")
    exercise_seven()

    print("\n=== Exercise 8: Infinite Counter ===")
    exercise_eight()

    print("\n=== Exercise 9: Manual Iteration ===")
    exercise_nine()

    print("\n=== Exercise 10: Step Iterator ===")
    exercise_ten()

    print("\n=== Exercise 11: File Line Reader ===")
    exercise_eleven()

    print("\n=== Exercise 12: CSV Row Parser ===")
    exercise_twelve()

    print("\n=== Exercise 13: The Pipeline ===")
    exercise_thirteen()

    print("\n=== Exercise 14: List Flattener ===")
    exercise_fourteen()

    print("\n=== Exercise 15: Batch Processing ===")
    exercise_fifteen()

    print("\n=== Exercise 16: Prime Sieve ===")
    exercise_sixteen()

    print("\n=== Exercise 17: Running Average ===")
    exercise_seventeen()

    print("\n=== Exercise 18: Sliding Window ===")
    exercise_eighteen()

    print("\n=== Exercise 19: Log Filter ===")
    exercise_nineteen()

    print("\n=== Exercise 20: Unique Element Filter ===")
    exercise_twenty()

    print("\n=== Exercise 21: The Accumulator (send) ===")
    exercise_twenty_one()

    print("\n=== Exercise 22: Custom Zip ===")
    exercise_twenty_two()

    print("\n=== Exercise 23: Binary Tree Traversal ===")
    exercise_twenty_three()

    print("\n=== Exercise 24: Data Throttler ===")
    exercise_twenty_four()

    print("\n=== Exercise 25: Generator State Machine ===")
    exercise_twenty_five()

    print("\n=== Exercise 26: Peekable Iterator ===")
    exercise_twenty_six()

    print("\n=== Exercise 27: Exception Handler ===")
    exercise_twenty_seven()

    print("\n=== Exercise 28: Recursive Directory Walker ===")
    exercise_twenty_eight()

    print("\n=== Exercise 29: Interleaved Streams ===")
    exercise_twenty_nine()

    print("\n=== Exercise 30: Generator Cleanup ===")
    exercise_thirty()
