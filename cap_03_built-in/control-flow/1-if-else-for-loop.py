"""
Control Flow: A Complete Guide to if/else and Loops in Python

Control flow decides which statements run and how often. Conditionals (if / elif /
else) branch on boolean tests; loops (for, while) repeat work; and break / continue /
the loop-else clause fine-tune iteration. This file contains 40 exercises covering
conditionals and loops.

NOTE ON NUMBERING: The source page labels its exercises inconsistently (it has two
"Exercise 4" entries and skips numbers). They are renumbered here 1..40 sequentially so
each function matches its docstring and runner header.

=== CONTROL FLOW CONCEPTS ===

1. IF / ELIF / ELSE
   Description: Run a block when a condition is true; chain alternatives
   Example: if x > 0: ... elif x == 0: ... else: ...

2. COMPARISON & LOGICAL OPERATORS (==, !=, <, >, and, or, not)
   Description: Build boolean conditions
   Example: if a > 0 and b > 0: ...

3. FOR LOOP (for x in iterable)
   Description: Iterate over a sequence or any iterable
   Example: for n in [1, 2, 3]: ...

4. WHILE LOOP (while condition)
   Description: Repeat as long as a condition stays true
   Example: while n > 0: n -= 1

5. RANGE (range(start, stop, step))
   Description: Generate arithmetic sequences for counting loops
   Example: range(1, 11) -> 1..10

6. BREAK / CONTINUE
   Description: break exits the loop; continue skips to the next iteration
   Example: if x > 500: break

7. NESTED LOOPS
   Description: A loop inside another, e.g. for grids and patterns
   Example: for i in range(n): for j in range(i): ...

8. ENUMERATE
   Description: Loop with both index and value
   Example: for i, v in enumerate(seq): ...

Run:
    poetry run python cap_03_built-in/control-flow/1-if-else-for-loop.py
"""


def exercise_one() -> None:
    """
    Exercise 1: First 10 Natural Numbers (while)

    Problem: Print the first 10 natural numbers using a while loop.

    Purpose: This exercise shows the anatomy of a while loop: initialize, test, act,
    and advance the counter so the loop eventually ends.

    Given Input: none (fixed range 1-10)
    Expected Output: 1 2 3 4 5 6 7 8 9 10
    """
    n = 1
    while n <= 10:
        print(n, end=" ")
        n += 1
    print()


def exercise_two() -> None:
    """
    Exercise 2: Numbers -10 to -1 (for)

    Problem: Display numbers from -10 to -1 using a for loop.

    Purpose: This exercise shows range() with negative bounds; the stop value 0 is
    excluded, so the last number printed is -1.

    Given Input: none
    Expected Output: -10 -9 ... -1
    """
    for n in range(-10, 0):
        print(n, end=" ")
    print()


def exercise_three() -> None:
    """
    Exercise 3: Print Numbers Then "Done!"

    Problem: Display "Done!" after a for loop iterating 0 to 4.

    Purpose: This exercise shows code running after a loop completes; here a plain
    statement, but conceptually similar to a loop-else.

    Given Input: none
    Expected Output: 0 1 2 3 4 then Done!
    """
    for n in range(5):
        print(n, end=" ")
    print()
    print("Done!")


def exercise_four() -> None:
    """
    Exercise 4: Sum from 1 to N

    Problem: Calculate the sum of all numbers from 1 to a given number.

    Purpose: This exercise accumulates a running total across a counting loop.

    Given Input: 10
    Expected Output: Sum is: 55
    """
    number = 10
    total = 0
    for n in range(1, number + 1):
        total += n
    print(f"Sum is: {total}")


def exercise_five() -> None:
    """
    Exercise 5: Multiplication Table

    Problem: Print the multiplication table of an integer from 1 to 10.

    Purpose: This exercise iterates a fixed range and computes a product each step.

    Given Input: 2
    Expected Output: 2 4 6 ... 20
    """
    number = 2
    for i in range(1, 11):
        print(number * i, end=" ")
    print()


def exercise_six() -> None:
    """
    Exercise 6: Cubes with Formatted Output

    Problem: Print the cube of every number from 1 to n with a formatted message.

    Purpose: This exercise combines a loop with an f-string message per iteration.

    Given Input: input_number = 6
    Expected Output: lines reporting each number and its cube (1..6, cube 1..216)
    """
    input_number = 6
    for n in range(1, input_number + 1):
        print(f"Current Number is : {n} and the cube is {n ** 3}")


def exercise_seven() -> None:
    """
    Exercise 7: Conditional Iteration with break/continue

    Problem: Print numbers divisible by 5; skip numbers above 150; stop above 500.

    Purpose: This exercise combines continue (skip this one) and break (stop entirely)
    with a divisibility test inside one loop.

    Given Input: [12, 75, 150, 180, 145, 525, 50]
    Expected Output: 75 150 145
    """
    numbers = [12, 75, 150, 180, 145, 525, 50]
    for n in numbers:
        if n > 500:
            break        # stop the whole loop
        if n > 150:
            continue     # skip this number
        if n % 5 == 0:
            print(n, end=" ")
    print()


def exercise_eight() -> None:
    """
    Exercise 8: Count Occurrences in a List

    Problem: Count how many times a specific number appears in a list.

    Purpose: This exercise increments a counter whenever the value matches the target.

    Given Input: list1 = [10, 20, 10, 30, 10, 40, 50], target = 10
    Expected Output: 10 appears 3 times
    """
    list1 = [10, 20, 10, 30, 10, 40, 50]
    target = 10
    count = 0
    for n in list1:
        if n == target:
            count += 1
    print(f"{target} appears {count} times")


def exercise_nine() -> None:
    """
    Exercise 9: Elements at Odd Index Positions

    Problem: Print the elements located at odd indices (1, 3, 5, ...).

    Purpose: This exercise uses range with a step of 2 starting at 1 to walk only the
    odd indices.

    Given Input: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    Expected Output: [20, 40, 60, 80, 100]
    """
    numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    result = [numbers[i] for i in range(1, len(numbers), 2)]
    print(result)


def exercise_ten() -> None:
    """
    Exercise 10: Iterate a List in Reverse

    Problem: Iterate through a list in reverse order and print each element.

    Purpose: This exercise shows reversed(), which yields items back to front without
    copying via a slice.

    Given Input: [10, 20, 30, 40, 50]
    Expected Output: 50 40 30 20 10
    """
    numbers = [10, 20, 30, 40, 50]
    for n in reversed(numbers):
        print(n, end=" ")
    print()


def exercise_eleven() -> None:
    """
    Exercise 11: Reverse a String with a Loop

    Problem: Reverse a string using a for loop, without slicing.

    Purpose: This exercise prepends each character to the result, which builds the
    reversed string one character at a time.

    Given Input: "Python"
    Expected Output: Original: Python, Reversed: nohtyP
    """
    text = "Python"
    reversed_text = ""
    for char in text:
        reversed_text = char + reversed_text
    print(f"Original: {text}, Reversed: {reversed_text}")


def exercise_twelve() -> None:
    """
    Exercise 12: Count Vowels and Consonants

    Problem: Count vowels and consonants in a sentence, ignoring non-letters.

    Purpose: This exercise classifies each alphabetic character as vowel or consonant
    and skips everything else.

    Given Input: "Loops are Fun!"
    Expected Output: Vowels: 5, Consonants: 7
    """
    sentence = "Loops are Fun!"
    vowels = consonants = 0
    for char in sentence.lower():
        if char.isalpha():
            if char in "aeiou":
                vowels += 1
            else:
                consonants += 1
    print(f"Vowels: {vowels}, Consonants: {consonants}")


def exercise_thirteen() -> None:
    """
    Exercise 13: Count Digits in an Integer (while)

    Problem: Count the total number of digits using a while loop.

    Purpose: This exercise repeatedly divides by 10, counting how many times until the
    number reaches 0.

    Given Input: 75869
    Expected Output: Total digits are: 5
    """
    number = 75869
    count = 0
    while number > 0:
        number //= 10
        count += 1
    print(f"Total digits are: {count}")


def exercise_fourteen() -> None:
    """
    Exercise 14: Reverse an Integer Mathematically

    Problem: Reverse a given integer using arithmetic, not strings.

    Purpose: This exercise peels off the last digit with % 10 and builds the reversed
    number by shifting the accumulator left (× 10) each step.

    Given Input: 76542
    Expected Output: 24567
    """
    number = 76542
    reversed_number = 0
    while number > 0:
        reversed_number = reversed_number * 10 + number % 10
        number //= 10
    print(reversed_number)


def exercise_fifteen() -> None:
    """
    Exercise 15: Largest and Smallest Digit

    Problem: Find the largest and smallest digit within an integer.

    Purpose: This exercise extracts the digits and applies max()/min() to them.

    Given Input: 75869
    Expected Output: Largest digit: 9, Smallest digit: 5
    """
    number = 75869
    digits = [int(d) for d in str(number)]
    print(f"Largest digit: {max(digits)}, Smallest digit: {min(digits)}")


def exercise_sixteen() -> None:
    """
    Exercise 16: Number Palindrome Check

    Problem: Check whether a number is a palindrome.

    Purpose: This exercise compares the number's digit string with its reverse.

    Given Input: 121
    Expected Output: Yes
    """
    number = 121
    text = str(number)
    print("Yes" if text == text[::-1] else "No")


def exercise_seventeen() -> None:
    """
    Exercise 17: Factorial with a Loop

    Problem: Find the factorial of a number using a loop.

    Purpose: This exercise multiplies a running product across 1..n, the iterative
    counterpart to recursive factorial.

    Given Input: 5
    Expected Output: 120
    """
    number = 5
    factorial = 1
    for n in range(1, number + 1):
        factorial *= n
    print(factorial)


def exercise_eighteen() -> None:
    """
    Exercise 18: Collatz Conjecture Sequence

    Problem: Generate the Collatz sequence until reaching 1.

    Purpose: This exercise shows a while loop whose length is not known in advance:
    halve even numbers, and do 3n+1 for odd ones, until it collapses to 1.

    Given Input: 6
    Expected Output: 6 3 10 5 16 8 4 2 1
    """
    n = 6
    sequence = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        sequence.append(n)
    print(*sequence)


def exercise_nineteen() -> None:
    """
    Exercise 19: Armstrong Number Check

    Problem: Check whether a number is an Armstrong number.

    Purpose: This exercise sums the cube of each digit (for a 3-digit number) and
    compares it to the original.

    Given Input: 153
    Expected Output: Yes
    """
    number = 153
    digits = [int(d) for d in str(number)]
    total = sum(d**3 for d in digits)
    print("Yes" if total == number else "No")


def exercise_twenty() -> None:
    """
    Exercise 20: Right-Angled Number Triangle

    Problem: Print a right-angled triangle with increasing numbers per row.

    Purpose: This exercise uses a nested loop: the outer controls rows, the inner
    prints 1..row.

    Given Input: height 5
    Expected Output: 1 / 1 2 / 1 2 3 / 1 2 3 4 / 1 2 3 4 5
    """
    height = 5
    for row in range(1, height + 1):
        for col in range(1, row + 1):
            print(col, end=" ")
        print()


def exercise_twenty_one() -> None:
    """
    Exercise 21: Reverse Number Pattern

    Problem: Print a decreasing number pattern.

    Purpose: This exercise nests a descending inner range inside a descending outer
    range.

    Given Input: 5
    Expected Output: 5 4 3 2 1 / 4 3 2 1 / 3 2 1 / 2 1 / 1
    """
    rows = 5
    for start in range(rows, 0, -1):
        for value in range(start, 0, -1):
            print(value, end=" ")
        print()


def exercise_twenty_two() -> None:
    """
    Exercise 22: Alternate Numbers 1 to 20

    Problem: Print alternate numbers from 1 to 20.

    Purpose: This exercise uses range with a step of 2 to emit every other number.

    Given Input: range 1-20
    Expected Output: 1 3 5 7 9 11 13 15 17 19
    """
    for n in range(1, 21, 2):
        print(n, end=" ")
    print()


def exercise_twenty_three() -> None:
    """
    Exercise 23: Alphabet Pyramid

    Problem: Print an alphabet pyramid (A, BB, CCC, ...).

    Purpose: This exercise maps a row index to a letter with chr(65 + i) and repeats
    it per row.

    Given Input: 5
    Expected Output: A / B B / C C C / D D D D / E E E E E
    """
    rows = 5
    for i in range(rows):
        letter = chr(65 + i)  # 65 is 'A'
        print(*([letter] * (i + 1)))


def exercise_twenty_four() -> None:
    """
    Exercise 24: Hollow Square

    Problem: Print a hollow 5x5 square of stars.

    Purpose: This exercise prints a star only on the border (first/last row or column)
    and a space inside, demonstrating positional conditions in a grid.

    Given Input: 5
    Expected Output: a 5x5 square outline
    """
    size = 5
    for row in range(size):
        for col in range(size):
            if row in (0, size - 1) or col in (0, size - 1):
                print("*", end="")
            else:
                print(" ", end="")
        print()


def exercise_twenty_five() -> None:
    """
    Exercise 25: Diamond-ish Star Pyramid

    Problem: Print a pyramid that grows then shrinks.

    Purpose: This exercise concatenates an ascending pass (1..n stars) with a
    descending pass (n-1..1 stars).

    Given Input: 5
    Expected Output: rows of 1..5 stars, then 4..1 stars
    """
    n = 5
    for count in range(1, n + 1):
        print("*" * count)
    for count in range(n - 1, 0, -1):
        print("*" * count)


def exercise_twenty_six() -> None:
    """
    Exercise 26: Full Multiplication Grid

    Problem: Print the multiplication table from 1 to 10 in a grid.

    Purpose: This exercise nests two loops and aligns each product in a fixed width so
    the columns line up.

    Given Input: none
    Expected Output: a 10x10 multiplication grid
    """
    for row in range(1, 11):
        for col in range(1, 11):
            print(f"{row * col:4}", end="")
        print()


def exercise_twenty_seven() -> None:
    """
    Exercise 27: Cumulative Sum List

    Problem: Build a list where each element is the sum of all previous elements.

    Purpose: This exercise carries a running total and appends it each step (a prefix
    sum).

    Given Input: [1, 2, 3, 4]
    Expected Output: [1, 3, 6, 10]
    """
    numbers = [1, 2, 3, 4]
    running = 0
    result: list[int] = []
    for n in numbers:
        running += n
        result.append(running)
    print(result)


def exercise_twenty_eight() -> None:
    """
    Exercise 28: Filter Dictionary by Threshold

    Problem: Extract dictionary pairs whose value exceeds a threshold.

    Purpose: This exercise loops over .items() and conditionally keeps pairs into a new
    dict.

    Given Input: {"Alice": 85, "Bob": 70, "Charlie": 95, "David": 60}, threshold = 75
    Expected Output: {'Alice': 85, 'Charlie': 95}
    """
    scores = {"Alice": 85, "Bob": 70, "Charlie": 95, "David": 60}
    threshold = 75
    result = {name: score for name, score in scores.items() if score > threshold}
    print(result)


def exercise_twenty_nine() -> None:
    """
    Exercise 29: Common Elements with a Loop

    Problem: Find common elements between two lists using a loop.

    Purpose: This exercise checks membership of each item of one list against the
    other, building the intersection by hand.

    Given Input: [1, 2, 3, 4, 5] and [4, 5, 6, 7, 8]
    Expected Output: [4, 5]
    """
    list1 = [1, 2, 3, 4, 5]
    list2 = [4, 5, 6, 7, 8]
    common = [n for n in list1 if n in list2]
    print(common)


def exercise_thirty() -> None:
    """
    Exercise 30: Remove Duplicates Preserving Order

    Problem: Remove duplicates from a list while maintaining order.

    Purpose: This exercise tracks seen values in a set and appends only first
    occurrences, which preserves order.

    Given Input: [1, 2, 2, 3, 4, 4, 4, 5]
    Expected Output: [1, 2, 3, 4, 5]
    """
    numbers = [1, 2, 2, 3, 4, 4, 4, 5]
    seen: set[int] = set()
    result: list[int] = []
    for n in numbers:
        if n not in seen:
            seen.add(n)
            result.append(n)
    print(result)


def exercise_thirty_one() -> None:
    """
    Exercise 31: Evens to Front, Odds to Back

    Problem: Move all even numbers to the front and odd numbers to the back.

    Purpose: This exercise partitions the list into two passes and concatenates them,
    preserving relative order within each group.

    Given Input: [1, 2, 3, 4, 5, 6]
    Expected Output: [2, 4, 6, 1, 3, 5]
    """
    numbers = [1, 2, 3, 4, 5, 6]
    evens = [n for n in numbers if n % 2 == 0]
    odds = [n for n in numbers if n % 2 != 0]
    print(evens + odds)


def exercise_thirty_two() -> None:
    """
    Exercise 32: Rotate List Left by K

    Problem: Rotate list elements left by k positions.

    Purpose: This exercise slices the list at k and swaps the two halves.

    Given Input: [1, 2, 3, 4, 5], k = 2
    Expected Output: [3, 4, 5, 1, 2]
    """
    numbers = [1, 2, 3, 4, 5]
    k = 2
    print(numbers[k:] + numbers[:k])


def exercise_thirty_three() -> None:
    """
    Exercise 33: Word Frequency

    Problem: Count the frequency of each word in a string.

    Purpose: This exercise applies the .get(word, 0) counter idiom while looping over
    the split words.

    Given Input: "apple banana apple orange banana apple"
    Expected Output: {'apple': 3, 'banana': 2, 'orange': 1}
    """
    text = "apple banana apple orange banana apple"
    counts: dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    print(counts)


def exercise_thirty_four() -> None:
    """
    Exercise 34: Fibonacci Sequence

    Problem: Display the Fibonacci sequence up to 10 terms.

    Purpose: This exercise keeps the two most recent terms and advances them with
    simultaneous assignment.

    Given Input: 10 terms
    Expected Output: 0 1 1 2 3 5 8 13 21 34
    """
    terms = 10
    a, b = 0, 1
    for _ in range(terms):
        print(a, end=" ")
        a, b = b, a + b
    print()


def exercise_thirty_five() -> None:
    """
    Exercise 35: Perfect Number Check

    Problem: Check whether a number equals the sum of its proper divisors.

    Purpose: This exercise sums every divisor below the number and compares it to the
    original.

    Given Input: 28
    Expected Output: 28 is a Perfect Number
    """
    number = 28
    divisors_sum = sum(d for d in range(1, number) if number % d == 0)
    if divisors_sum == number:
        print(f"{number} is a Perfect Number")
    else:
        print(f"{number} is not a Perfect Number")


def exercise_thirty_six() -> None:
    """
    Exercise 36: Binary String to Decimal

    Problem: Convert a binary string to decimal using a loop.

    Purpose: This exercise builds the value digit by digit: each step doubles the
    accumulator and adds the next bit (Horner's method for base 2).

    Given Input: "1101"
    Expected Output: Decimal value: 13
    """
    binary = "1101"
    decimal = 0
    for bit in binary:
        decimal = decimal * 2 + int(bit)
    print(f"Decimal value: {decimal}")


def exercise_thirty_seven() -> None:
    """
    Exercise 37: Primes in a Range

    Problem: Display all prime numbers within a range.

    Purpose: This exercise nests a divisibility test inside the range scan, using a
    loop-else (the else runs only if no divisor was found).

    Given Input: start = 25, end = 50
    Expected Output: 29 31 37 41 43 47
    """
    start, end = 25, 50
    for candidate in range(start, end + 1):
        if candidate < 2:
            continue
        for divisor in range(2, int(candidate**0.5) + 1):
            if candidate % divisor == 0:
                break
        else:
            print(candidate, end=" ")
    print()


def exercise_thirty_eight() -> None:
    """
    Exercise 38: Sum of Series 2 + 22 + 222 + ...

    Problem: Sum the series 2 + 22 + 222 + 2222 up to N terms.

    Purpose: This exercise grows each term from the previous one (term = term*10 + 2)
    while accumulating the total.

    Given Input: 5 terms
    Expected Output: 24690
    """
    terms = 5
    term = 2
    total = 0
    for _ in range(terms):
        total += term
        term = term * 10 + 2
    print(total)


def exercise_thirty_nine() -> None:
    """
    Exercise 39: Flatten a Nested List

    Problem: Flatten a nested list into a single-dimension list.

    Purpose: This exercise uses a nested loop (one level of nesting) to collect every
    inner element into a flat list.

    Given Input: [[10, 20], [30, 40], [50, 60]]
    Expected Output: [10, 20, 30, 40, 50, 60]
    """
    nested = [[10, 20], [30, 40], [50, 60]]
    flat = [item for sublist in nested for item in sublist]
    print(flat)


def exercise_forty() -> None:
    """
    Exercise 40: Find Position in a 2D Matrix

    Problem: Find the row and column index of a target value in a 2D matrix.

    Purpose: This exercise scans the grid with enumerate on both dimensions to report
    the coordinates of the first match.

    Given Input: [[10, 20], [30, 40], [50, 60]], target = 30
    Expected Output: Target 30 found at Row: 1, Column: 0
    """
    matrix = [[10, 20], [30, 40], [50, 60]]
    target = 30
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            if value == target:
                print(f"Target {target} found at Row: {row_index}, Column: {col_index}")


def main() -> None:
    print("=== Exercise 1: First 10 Natural Numbers (while) ===")
    exercise_one()

    print("\n=== Exercise 2: Numbers -10 to -1 (for) ===")
    exercise_two()

    print("\n=== Exercise 3: Print Numbers Then \"Done!\" ===")
    exercise_three()

    print("\n=== Exercise 4: Sum from 1 to N ===")
    exercise_four()

    print("\n=== Exercise 5: Multiplication Table ===")
    exercise_five()

    print("\n=== Exercise 6: Cubes with Formatted Output ===")
    exercise_six()

    print("\n=== Exercise 7: Conditional Iteration with break/continue ===")
    exercise_seven()

    print("\n=== Exercise 8: Count Occurrences in a List ===")
    exercise_eight()

    print("\n=== Exercise 9: Elements at Odd Index Positions ===")
    exercise_nine()

    print("\n=== Exercise 10: Iterate a List in Reverse ===")
    exercise_ten()

    print("\n=== Exercise 11: Reverse a String with a Loop ===")
    exercise_eleven()

    print("\n=== Exercise 12: Count Vowels and Consonants ===")
    exercise_twelve()

    print("\n=== Exercise 13: Count Digits in an Integer (while) ===")
    exercise_thirteen()

    print("\n=== Exercise 14: Reverse an Integer Mathematically ===")
    exercise_fourteen()

    print("\n=== Exercise 15: Largest and Smallest Digit ===")
    exercise_fifteen()

    print("\n=== Exercise 16: Number Palindrome Check ===")
    exercise_sixteen()

    print("\n=== Exercise 17: Factorial with a Loop ===")
    exercise_seventeen()

    print("\n=== Exercise 18: Collatz Conjecture Sequence ===")
    exercise_eighteen()

    print("\n=== Exercise 19: Armstrong Number Check ===")
    exercise_nineteen()

    print("\n=== Exercise 20: Right-Angled Number Triangle ===")
    exercise_twenty()

    print("\n=== Exercise 21: Reverse Number Pattern ===")
    exercise_twenty_one()

    print("\n=== Exercise 22: Alternate Numbers 1 to 20 ===")
    exercise_twenty_two()

    print("\n=== Exercise 23: Alphabet Pyramid ===")
    exercise_twenty_three()

    print("\n=== Exercise 24: Hollow Square ===")
    exercise_twenty_four()

    print("\n=== Exercise 25: Diamond-ish Star Pyramid ===")
    exercise_twenty_five()

    print("\n=== Exercise 26: Full Multiplication Grid ===")
    exercise_twenty_six()

    print("\n=== Exercise 27: Cumulative Sum List ===")
    exercise_twenty_seven()

    print("\n=== Exercise 28: Filter Dictionary by Threshold ===")
    exercise_twenty_eight()

    print("\n=== Exercise 29: Common Elements with a Loop ===")
    exercise_twenty_nine()

    print("\n=== Exercise 30: Remove Duplicates Preserving Order ===")
    exercise_thirty()

    print("\n=== Exercise 31: Evens to Front, Odds to Back ===")
    exercise_thirty_one()

    print("\n=== Exercise 32: Rotate List Left by K ===")
    exercise_thirty_two()

    print("\n=== Exercise 33: Word Frequency ===")
    exercise_thirty_three()

    print("\n=== Exercise 34: Fibonacci Sequence ===")
    exercise_thirty_four()

    print("\n=== Exercise 35: Perfect Number Check ===")
    exercise_thirty_five()

    print("\n=== Exercise 36: Binary String to Decimal ===")
    exercise_thirty_six()

    print("\n=== Exercise 37: Primes in a Range ===")
    exercise_thirty_seven()

    print("\n=== Exercise 38: Sum of Series 2 + 22 + 222 + ... ===")
    exercise_thirty_eight()

    print("\n=== Exercise 39: Flatten a Nested List ===")
    exercise_thirty_nine()

    print("\n=== Exercise 40: Find Position in a 2D Matrix ===")
    exercise_forty()


main()
