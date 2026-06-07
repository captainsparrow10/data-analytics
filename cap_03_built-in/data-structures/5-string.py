"""
Strings: A Complete Guide to Immutable Text Sequences in Python

A string is an immutable sequence of Unicode characters. Because it is immutable,
every "modifying" operation returns a NEW string rather than changing the original.
Strings support all sequence operations (indexing, slicing, iteration) plus a rich
set of text methods. This file contains 38 exercises covering string fundamentals
and common idioms.

=== STRING OPERATORS & METHODS ===

1. INDEXING / SLICING (s[i], s[a:b:step])
   Description: Access a character or a substring; step -1 reverses
   Example: "python"[0] = "p" ; "python"[::-1] = "nohtyp"

2. CONCATENATION / REPETITION (+, *)
   Description: Join strings or repeat them
   Example: "ab" + "cd" = "abcd" ; "ab" * 3 = "ababab"

3. LENGTH / MEMBERSHIP (len(), in)
   Description: Character count and substring containment
   Example: len("abc") = 3 ; "bc" in "abc" = True

4. CASE METHODS (lower, upper, swapcase, capitalize, title)
   Description: Return case-transformed copies
   Example: "PyThOn".swapcase() = "pYtHoN"

5. SEARCH (find, rfind, index, count, startswith, endswith)
   Description: Locate substrings or test prefixes/suffixes
   Example: "abab".rfind("a") = 2 ; "abab".count("a") = 2

6. SPLIT / JOIN / PARTITION (split, rsplit, join, partition)
   Description: Break a string into parts or assemble parts into a string
   Example: "a-b".split("-") = ["a", "b"] ; "-".join(["a", "b"]) = "a-b"

7. STRIP / REPLACE (strip, lstrip, rstrip, replace)
   Description: Trim whitespace or substitute substrings
   Example: "  hi  ".strip() = "hi" ; "aaa".replace("a", "b") = "bbb"

8. CHARACTER TESTS (isalpha, isdigit, isalnum, isspace, islower, isupper)
   Description: Boolean tests on the characters of a string
   Example: "abc".isalpha() = True ; "12".isdigit() = True

9. FORMATTING (f-strings, format, :.2f, alignment)
   Description: Interpolate and format values into text
   Example: f"{3.14159:.2f}" = "3.14"

10. ITERATION
    Description: A string is iterable character by character
    Example: [c for c in "ab"] = ["a", "b"]
"""


def exercise_one():
    """
    Exercise 1: First, Middle, Last Character

    Problem: Build a new string from an input string's first, middle, and last
    characters.

    Purpose: This exercise practices index arithmetic, including computing the
    middle position with integer division len // 2.

    Given Input: str1 = "James"
    Expected Output: Jms
    """
    str1 = "James"
    middle = len(str1) // 2
    result = str1[0] + str1[middle] + str1[-1]
    print(result)


def exercise_two():
    """
    Exercise 2: Middle Three Characters

    Problem: Build a new string from the middle three characters of an input string.

    Purpose: This exercise computes a centered slice: the start index is
    (len - 3) // 2, and the slice takes three characters from there.

    Given Input: str1 = "JhonDipPeta"
    Expected Output: Dip
    """
    str1 = "JhonDipPeta"
    start = (len(str1) - 3) // 2
    print(str1[start:start + 3])


def exercise_three():
    """
    Exercise 3: Append in Middle

    Problem: Insert one string into the middle of another.

    Purpose: This exercise slices the first string at its midpoint and concatenates
    the second string between the two halves.

    Given Input: s1 = "Ault", s2 = "Kelly"
    Expected Output: AuKellylt
    """
    s1 = "Ault"
    s2 = "Kelly"
    mid = len(s1) // 2
    print(s1[:mid] + s2 + s1[mid:])


def exercise_four():
    """
    Exercise 4: Extract from Two Strings

    Problem: Build a new string from the first, middle, and last characters of each
    of two input strings, interleaved.

    Purpose: This exercise combines index arithmetic on two strings, interleaving
    their first/middle/last characters in pairs.

    Given Input: s1 = "America", s2 = "Japan"
    Expected Output: AJrpan
    """
    s1 = "America"
    s2 = "Japan"
    m1, m2 = len(s1) // 2, len(s2) // 2
    result = s1[0] + s2[0] + s1[m1] + s2[m2] + s1[-1] + s2[-1]
    print(result)


def exercise_five():
    """
    Exercise 5: Reverse String

    Problem: Reverse a given string.

    Purpose: This exercise uses slice notation with a step of -1, the idiomatic way
    to reverse any sequence in Python.

    Given Input: str1 = "PYnative"
    Expected Output: evitanYP
    """
    str1 = "PYnative"
    print(str1[::-1])


def exercise_six():
    """
    Exercise 6: Last Substring Position

    Problem: Find the last index where the substring "Emma" begins.

    Purpose: This exercise uses .rfind(), which searches from the right and returns
    the highest matching index (or -1 if absent).

    Given Input: a sentence mentioning "Emma" twice
    Expected Output: Last occurrence of Emma starts at index 43
    """
    str1 = "Emma is a data scientist who knows Python. Emma works at google."
    print(f"Last occurrence of Emma starts at index {str1.rfind('Emma')}")


def exercise_seven():
    """
    Exercise 7: Split on Hyphens

    Problem: Split a string on hyphens and display each substring.

    Purpose: This exercise shows str.split(sep) breaking a string into a list on a
    chosen delimiter.

    Given Input: str1 = "Emma-is-a-data-scientist"
    Expected Output: each word on its own line
    """
    str1 = "Emma-is-a-data-scientist"
    for word in str1.split("-"):
        print(word)


def exercise_eight():
    """
    Exercise 8: Case-Insensitive Count

    Problem: Count occurrences of the substring "USA", ignoring case.

    Purpose: This exercise normalizes the whole string to lowercase first, so a
    single .count() catches every casing variant.

    Given Input: str1 = "Welcome to USA. usa awesome, isn't it?"
    Expected Output: The USA count is: 2
    """
    str1 = "Welcome to USA. usa awesome, isn't it?"
    print(f"The USA count is: {str1.lower().count('usa')}")


def exercise_nine():
    """
    Exercise 9: String Balance Check

    Problem: Check whether all characters of one string appear in another.

    Purpose: This exercise uses all() with a generator, returning True only if every
    character of s1 is found in s2.

    Given Input: ("yn", "PyNative") and ("ynf", "PyNative")
    Expected Output: True, then False
    """
    def is_balanced(s1: str, s2: str) -> bool:
        return all(char in s2 for char in s1)

    print(is_balanced("yn", "PyNative"))
    print(is_balanced("ynf", "PyNative"))


def exercise_ten():
    """
    Exercise 10: Vowel Counter

    Problem: Count the total number of vowels in a string.

    Purpose: This exercise sums a generator that yields 1 for each vowel, comparing
    against a lowercased copy so case does not matter.

    Given Input: str1 = "Hello World"
    Expected Output: Vowel Count: 3
    """
    str1 = "Hello World"
    count = sum(1 for char in str1.lower() if char in "aeiou")
    print(f"Vowel Count: {count}")


def exercise_eleven():
    """
    Exercise 11: Prefix/Suffix Validation

    Problem: Check whether a URL starts with "https" and ends with ".com".

    Purpose: This exercise combines .startswith() and .endswith() for simple
    prefix/suffix validation.

    Given Input: str1 = "https://google.com"
    Expected Output: Is valid URL: True
    """
    str1 = "https://google.com"
    valid = str1.startswith("https") and str1.endswith(".com")
    print(f"Is valid URL: {valid}")


def exercise_twelve():
    """
    Exercise 12: Case Swap

    Problem: Toggle the case of every character in a string.

    Purpose: This exercise shows .swapcase(), which flips lower to upper and vice
    versa in a single call.

    Given Input: str1 = "PyThOn"
    Expected Output: pYtHoN
    """
    str1 = "PyThOn"
    print(str1.swapcase())


def exercise_thirteen():
    """
    Exercise 13: Remove Whitespace

    Problem: Remove every space from a string.

    Purpose: This exercise uses .replace(" ", "") to strip ALL spaces, not just the
    leading/trailing ones that .strip() would remove.

    Given Input: str1 = " P y t h o n "
    Expected Output: Python
    """
    str1 = " P y t h o n "
    print(str1.replace(" ", ""))


def exercise_fourteen():
    """
    Exercise 14: Remove Character at Index

    Problem: Remove the character at index i from a string.

    Purpose: This exercise exploits string immutability: you cannot delete in place,
    so you slice around the index and concatenate the two halves.

    Given Input: str1 = "Python", i = 2
    Expected Output: Pyhon
    """
    str1 = "Python"
    i = 2
    print(str1[:i] + str1[i + 1:])


def exercise_fifteen():
    """
    Exercise 15: String Partitioning

    Problem: Split a string into three parts around the first separator.

    Purpose: This exercise shows .partition(), which always returns a 3-tuple
    (before, separator, after) even when the separator is missing.

    Given Input: str1 = "username@company.com", sep = "@"
    Expected Output: ('username', '@', 'company.com')
    """
    str1 = "username@company.com"
    print(str1.partition("@"))


def exercise_sixteen():
    """
    Exercise 16: Extract File Extension

    Problem: Extract only the file extension from a filename.

    Purpose: This exercise uses .rsplit(".", 1) so that only the LAST dot splits the
    name, correctly handling filenames that contain multiple dots.

    Given Input: file_name = "report_final_v2.pdf"
    Expected Output: pdf
    """
    file_name = "report_final_v2.pdf"
    print(file_name.rsplit(".", 1)[-1])


def exercise_seventeen():
    """
    Exercise 17: Lowercase First

    Problem: Rearrange characters so lowercase letters come first, then uppercase.

    Purpose: This exercise builds two filtered lists (lowercase then uppercase) and
    joins them, a stable reordering that preserves each group's internal order.

    Given Input: str1 = "PyNaTive"
    Expected Output: yaivePNT
    """
    str1 = "PyNaTive"
    lowers = [c for c in str1 if c.islower()]
    uppers = [c for c in str1 if c.isupper()]
    print("".join(lowers + uppers))


def exercise_eighteen():
    """
    Exercise 18: Count Character Categories

    Problem: Count letters, digits, and special symbols in a string.

    Purpose: This exercise classifies each character with .isalpha()/.isdigit(),
    treating everything else as a symbol.

    Given Input: str1 = "P@#yn26at^&i5ve"
    Expected Output: Chars = 8 Digits = 3 Symbol = 4
    """
    str1 = "P@#yn26at^&i5ve"
    chars = digits = symbols = 0
    for c in str1:
        if c.isalpha():
            chars += 1
        elif c.isdigit():
            digits += 1
        else:
            symbols += 1
    print(f"Chars = {chars} Digits = {digits} Symbol = {symbols}")


def exercise_nineteen():
    """
    Exercise 19: Alternating Characters

    Problem: Build a string by alternating characters from two strings, taking the
    second string in reverse.

    Purpose: This exercise pairs zip() with a reversed slice, interleaving s1
    forward with s2 backward.

    Given Input: s1 = "Abc", s2 = "Xyz"
    Expected Output: AzbycX
    """
    s1 = "Abc"
    s2 = "Xyz"
    result = "".join(a + b for a, b in zip(s1, s2[::-1]))
    print(result)


def exercise_twenty():
    """
    Exercise 20: Sum and Average of Digits

    Problem: Calculate the sum and average of the digits embedded in a string.

    Purpose: This exercise filters digit characters, converts them to ints, and
    formats the average to two decimal places with an f-string spec.

    Given Input: str1 = "PYnative29@#8496"
    Expected Output: Sum is: 38 Average is 6.33
    """
    str1 = "PYnative29@#8496"
    digits = [int(c) for c in str1 if c.isdigit()]
    total = sum(digits)
    average = total / len(digits)
    print(f"Sum is: {total} Average is {average:.2f}")


def exercise_twenty_one():
    """
    Exercise 21: Character Frequency Count

    Problem: Count the frequency of every character and store it in a dictionary.

    Purpose: This exercise applies the .get(char, 0) counter idiom over a string.

    Given Input: str1 = "apple"
    Expected Output: {'a': 1, 'p': 2, 'l': 1, 'e': 1}
    """
    str1 = "apple"
    freq: dict[str, int] = {}
    for char in str1:
        freq[char] = freq.get(char, 0) + 1
    print(freq)


def exercise_twenty_two():
    """
    Exercise 22: Remove Empty Strings

    Problem: Remove empty strings and None values from a list.

    Purpose: This exercise filters by truthiness, which drops both "" and None in a
    single pass. The list is annotated list[str | None] so the filter narrows the
    result to list[str] under strict typing.

    Given Input: str_list = ["Emma", "Jon", "", "Kelly", None, "Eric", ""]
    Expected Output: ['Emma', 'Jon', 'Kelly', 'Eric']
    """
    str_list: list[str | None] = ["Emma", "Jon", "", "Kelly", None, "Eric", ""]
    cleaned = [s for s in str_list if s]
    print(cleaned)


def exercise_twenty_three():
    """
    Exercise 23: Remove Punctuation

    Problem: Remove all special symbols and punctuation from a string.

    Purpose: This exercise keeps only alphanumeric characters and spaces, then
    collapses any runs of whitespace left behind by removed symbols via split/join.

    Given Input: str1 = "/*Jon is @developer & musician!!"
    Expected Output: Jon is developer musician
    """
    str1 = "/*Jon is @developer & musician!!"
    kept = "".join(c for c in str1 if c.isalnum() or c == " ")
    print(" ".join(kept.split()))


def exercise_twenty_four():
    """
    Exercise 24: Extract Only Digits

    Problem: Extract only the numeric digits from a mixed string.

    Purpose: This exercise filters with .isdigit() and joins the survivors into a
    single string of digits.

    Given Input: str1 = "I am 25 years and 10 months old"
    Expected Output: 2510
    """
    str1 = "I am 25 years and 10 months old"
    print("".join(c for c in str1 if c.isdigit()))


def exercise_twenty_five():
    """
    Exercise 25: Find Alphanumeric Words

    Problem: Find words that contain BOTH letters and numbers.

    Purpose: This exercise tests each word with two any() checks, keeping only those
    that mix alphabetic and numeric characters.

    Given Input: str1 = "Emma25 is Data scientist50 and AI Expert"
    Expected Output: Emma25, then scientist50
    """
    str1 = "Emma25 is Data scientist50 and AI Expert"
    for word in str1.split():
        has_letter = any(c.isalpha() for c in word)
        has_digit = any(c.isdigit() for c in word)
        if has_letter and has_digit:
            print(word)


def exercise_twenty_six():
    """
    Exercise 26: Replace Symbols with Hash

    Problem: Replace every special symbol with '#'.

    Purpose: This exercise rebuilds the string character by character, swapping any
    non-alphanumeric, non-space character for '#'.

    Given Input: str1 = "/*Jon is @developer & musician!!"
    Expected Output: ##Jon is #developer # musician##
    """
    str1 = "/*Jon is @developer & musician!!"
    result = "".join(c if c.isalnum() or c == " " else "#" for c in str1)
    print(result)


def exercise_twenty_seven():
    """
    Exercise 27: Palindrome Check

    Problem: Check whether a string reads the same forward and backward.

    Purpose: This exercise compares the string with its reversed slice.

    Given Input: str1 = "radar"
    Expected Output: Is Palindrome: True
    """
    str1 = "radar"
    print(f"Is Palindrome: {str1 == str1[::-1]}")


def exercise_twenty_eight():
    """
    Exercise 28: Anagram Detection

    Problem: Check whether two strings are anagrams of each other.

    Purpose: This exercise sorts both strings: two anagrams have identical sorted
    character sequences.

    Given Input: s1 = "listen", s2 = "silent"
    Expected Output: Are Anagrams: True
    """
    s1 = "listen"
    s2 = "silent"
    print(f"Are Anagrams: {sorted(s1) == sorted(s2)}")


def exercise_twenty_nine():
    """
    Exercise 29: Unique Character Check

    Problem: Determine whether a string has all unique characters.

    Purpose: This exercise compares len(set(s)) with len(s): if deduplicating shrank
    the count, a character repeated.

    Given Input: str1 = "python", str2 = "alphabet"
    Expected Output: 'python' unique: True, 'alphabet' unique: False
    """
    str1 = "python"
    str2 = "alphabet"
    print(f"'{str1}' unique: {len(set(str1)) == len(str1)}")
    print(f"'{str2}' unique: {len(set(str2)) == len(str2)}")


def exercise_thirty():
    """
    Exercise 30: Title Case Implementation

    Problem: Capitalize the first letter of every word WITHOUT using .title().

    Purpose: This exercise rebuilds title casing manually with .capitalize() per
    word, which also correctly lowercases the rest of each word.

    Given Input: str1 = "hello world from python"
    Expected Output: Hello World From Python
    """
    str1 = "hello world from python"
    print(" ".join(word.capitalize() for word in str1.split()))


def exercise_thirty_one():
    """
    Exercise 31: Remove Duplicate Characters

    Problem: Remove duplicate characters while preserving the original order.

    Purpose: This exercise uses dict.fromkeys(), which deduplicates AND keeps
    first-seen order (a plain set would lose order).

    Given Input: str1 = "google"
    Expected Output: gole
    """
    str1 = "google"
    print("".join(dict.fromkeys(str1)))


def exercise_thirty_two():
    """
    Exercise 32: Word Reversal

    Problem: Reverse the order of words but keep each word's characters unchanged.

    Purpose: This exercise splits into words, reverses the LIST of words, and rejoins
    (note: this differs from reversing the characters of the whole string).

    Given Input: str1 = "Python is fun"
    Expected Output: fun is Python
    """
    str1 = "Python is fun"
    print(" ".join(str1.split()[::-1]))


def exercise_thirty_three():
    """
    Exercise 33: Character Interleaving

    Problem: Merge two equal-length strings by alternating characters.

    Purpose: This exercise pairs zip() over both strings, concatenating one character
    from each per step.

    Given Input: s1 = "ABC", s2 = "xyz"
    Expected Output: AxByCz
    """
    s1 = "ABC"
    s2 = "xyz"
    print("".join(a + b for a, b in zip(s1, s2)))


def exercise_thirty_four():
    """
    Exercise 34: Longest Word

    Problem: Find the longest word in a sentence.

    Purpose: This exercise uses max() with key=len over the split words; on ties it
    returns the first longest word encountered.

    Given Input: str1 = "The quick brown fox jumps over the lazy dog"
    Expected Output: Longest word: quick
    """
    str1 = "The quick brown fox jumps over the lazy dog"
    print(f"Longest word: {max(str1.split(), key=len)}")


def exercise_thirty_five():
    """
    Exercise 35: Acronym Generator

    Problem: Generate an acronym from a phrase.

    Purpose: This exercise takes the first character of each word, uppercases it, and
    joins them.

    Given Input: str1 = "Random Access Memory"
    Expected Output: RAM
    """
    str1 = "Random Access Memory"
    print("".join(word[0].upper() for word in str1.split()))


def exercise_thirty_six():
    """
    Exercise 36: Word Frequency

    Problem: Count occurrences of each word and store them in a dictionary.

    Purpose: This exercise applies the .get(word, 0) counter idiom at the word level.

    Given Input: str1 = "apple banana apple cherry banana apple"
    Expected Output: {'apple': 3, 'banana': 2, 'cherry': 1}
    """
    str1 = "apple banana apple cherry banana apple"
    counts: dict[str, int] = {}
    for word in str1.split():
        counts[word] = counts.get(word, 0) + 1
    print(counts)


def exercise_thirty_seven():
    """
    Exercise 37: First Non-Repeating Character

    Problem: Find the first character that does not repeat in a string.

    Purpose: This exercise first builds a frequency table, then scans the string in
    order returning the first character whose count is exactly 1. Scanning the
    original string (not the dict) guarantees "first by position".

    Given Input: str1 = "swiss"
    Expected Output: w
    """
    str1 = "swiss"
    freq: dict[str, int] = {}
    for char in str1:
        freq[char] = freq.get(char, 0) + 1
    for char in str1:
        if freq[char] == 1:
            print(char)
            break


def exercise_thirty_eight():
    """
    Exercise 38: String Rotation Check

    Problem: Check whether one string is a rotation of another.

    Purpose: This exercise uses the classic trick: s2 is a rotation of s1 if and
    only if s2 is a substring of s1 + s1 (and they share the same length).

    Given Input: s1 = "waterbottle", s2 = "erbottlewat"
    Expected Output: Is Rotation: True
    """
    s1 = "waterbottle"
    s2 = "erbottlewat"
    is_rotation = len(s1) == len(s2) and s2 in (s1 + s1)
    print(f"Is Rotation: {is_rotation}")


if __name__ == "__main__":
    print("=== Exercise 1: First, Middle, Last Character ===")
    exercise_one()

    print("\n=== Exercise 2: Middle Three Characters ===")
    exercise_two()

    print("\n=== Exercise 3: Append in Middle ===")
    exercise_three()

    print("\n=== Exercise 4: Extract from Two Strings ===")
    exercise_four()

    print("\n=== Exercise 5: Reverse String ===")
    exercise_five()

    print("\n=== Exercise 6: Last Substring Position ===")
    exercise_six()

    print("\n=== Exercise 7: Split on Hyphens ===")
    exercise_seven()

    print("\n=== Exercise 8: Case-Insensitive Count ===")
    exercise_eight()

    print("\n=== Exercise 9: String Balance Check ===")
    exercise_nine()

    print("\n=== Exercise 10: Vowel Counter ===")
    exercise_ten()

    print("\n=== Exercise 11: Prefix/Suffix Validation ===")
    exercise_eleven()

    print("\n=== Exercise 12: Case Swap ===")
    exercise_twelve()

    print("\n=== Exercise 13: Remove Whitespace ===")
    exercise_thirteen()

    print("\n=== Exercise 14: Remove Character at Index ===")
    exercise_fourteen()

    print("\n=== Exercise 15: String Partitioning ===")
    exercise_fifteen()

    print("\n=== Exercise 16: Extract File Extension ===")
    exercise_sixteen()

    print("\n=== Exercise 17: Lowercase First ===")
    exercise_seventeen()

    print("\n=== Exercise 18: Count Character Categories ===")
    exercise_eighteen()

    print("\n=== Exercise 19: Alternating Characters ===")
    exercise_nineteen()

    print("\n=== Exercise 20: Sum and Average of Digits ===")
    exercise_twenty()

    print("\n=== Exercise 21: Character Frequency Count ===")
    exercise_twenty_one()

    print("\n=== Exercise 22: Remove Empty Strings ===")
    exercise_twenty_two()

    print("\n=== Exercise 23: Remove Punctuation ===")
    exercise_twenty_three()

    print("\n=== Exercise 24: Extract Only Digits ===")
    exercise_twenty_four()

    print("\n=== Exercise 25: Find Alphanumeric Words ===")
    exercise_twenty_five()

    print("\n=== Exercise 26: Replace Symbols with Hash ===")
    exercise_twenty_six()

    print("\n=== Exercise 27: Palindrome Check ===")
    exercise_twenty_seven()

    print("\n=== Exercise 28: Anagram Detection ===")
    exercise_twenty_eight()

    print("\n=== Exercise 29: Unique Character Check ===")
    exercise_twenty_nine()

    print("\n=== Exercise 30: Title Case Implementation ===")
    exercise_thirty()

    print("\n=== Exercise 31: Remove Duplicate Characters ===")
    exercise_thirty_one()

    print("\n=== Exercise 32: Word Reversal ===")
    exercise_thirty_two()

    print("\n=== Exercise 33: Character Interleaving ===")
    exercise_thirty_three()

    print("\n=== Exercise 34: Longest Word ===")
    exercise_thirty_four()

    print("\n=== Exercise 35: Acronym Generator ===")
    exercise_thirty_five()

    print("\n=== Exercise 36: Word Frequency ===")
    exercise_thirty_six()

    print("\n=== Exercise 37: First Non-Repeating Character ===")
    exercise_thirty_seven()

    print("\n=== Exercise 38: String Rotation Check ===")
    exercise_thirty_eight()
