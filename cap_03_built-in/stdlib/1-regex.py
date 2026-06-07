"""
Regular Expressions: A Complete Guide to Pattern Matching in Python

A regular expression (regex) is a compact language for describing text patterns. The
built-in `re` module compiles patterns and applies them to search, validate, extract,
and transform strings. Always write patterns as RAW strings (r"...") so backslashes
mean regex escapes, not Python escapes. This file contains 30 exercises covering regex.

NOTE: re.search / re.match / re.fullmatch return `Match | None`, so every result is
guarded with `if match:` before accessing groups/positions, which keeps the code
type-clean under strict checking.

=== REGEX CONCEPTS ===

1. FUNCTIONS (match, fullmatch, search, findall, finditer, sub)
   Description: match=at start, fullmatch=whole string, search=anywhere,
                findall=all matches, finditer=match objects, sub=replace
   Example: re.search(r"\\d+", "a12") finds "12"

2. CHARACTER CLASSES (\\d \\w \\s and [...])
   Description: \\d digit, \\w word char, \\s whitespace; [...] a custom set
   Example: [a-z] matches one lowercase letter

3. QUANTIFIERS (* + ? {m} {m,n})
   Description: * zero+, + one+, ? zero/one, {3} exactly, {2,3} a range
   Example: ab{2,3} matches abb or abbb

4. ANCHORS (^ $ \\b)
   Description: ^ start, $ end, \\b word boundary
   Example: ^Hello\\b

5. GROUPS ((...) and backreferences \\1)
   Description: Capture parts of a match; reuse them in replacements
   Example: re.sub(r"(\\d{4})-(\\d{2})", r"\\2-\\1", s)

6. ALTERNATION (|) and DOT (.)
   Description: | matches either side; . matches any character except newline
   Example: cat|dog

Run:
    poetry run python cap_03_built-in/stdlib/1-regex.py
"""

import re


def exercise_one() -> None:
    """
    Exercise 1: Check Allowed Characters

    Problem: Verify a string contains only alphanumeric characters.

    Purpose: This exercise uses fullmatch (the WHOLE string must match) with the class
    [a-zA-Z0-9] repeated one or more times.

    Given Input: text = "Hello123"
    Expected Output: Valid: contains only alphanumeric characters
    """
    text = "Hello123"
    if re.fullmatch(r"[a-zA-Z0-9]+", text):
        print("Valid: contains only alphanumeric characters")
    else:
        print("Invalid")


def exercise_two() -> None:
    """
    Exercise 2: Match Zero or More

    Problem: Match strings of `a` followed by zero or more `b`s.

    Purpose: This exercise demonstrates the * quantifier (zero or more).

    Given Input: ["a", "ab", "abb", "abbb", "b", "ba"]
    Expected Output: a, ab, abb, abbb match; b, ba do not
    """
    pattern = r"ab*"
    for candidate in ["a", "ab", "abb", "abbb", "b", "ba"]:
        print(f"{candidate!r}: {'match' if re.fullmatch(pattern, candidate) else 'no match'}")


def exercise_three() -> None:
    """
    Exercise 3: Match One or More

    Problem: Match strings of `a` followed by one or more `b`s.

    Purpose: This exercise demonstrates the + quantifier (one or more), so a bare "a"
    no longer matches.

    Given Input: ["a", "ab", "abb", "abbb", "b", "ba"]
    Expected Output: ab, abb, abbb match; others do not
    """
    pattern = r"ab+"
    for candidate in ["a", "ab", "abb", "abbb", "b", "ba"]:
        print(f"{candidate!r}: {'match' if re.fullmatch(pattern, candidate) else 'no match'}")


def exercise_four() -> None:
    """
    Exercise 4: Match Optional Characters

    Problem: Match strings of `a` followed by zero or one `b`.

    Purpose: This exercise demonstrates the ? quantifier (optional).

    Given Input: ["a", "ab", "abb", "abbb", "b", "ba"]
    Expected Output: a, ab match; others do not
    """
    pattern = r"ab?"
    for candidate in ["a", "ab", "abb", "abbb", "b", "ba"]:
        print(f"{candidate!r}: {'match' if re.fullmatch(pattern, candidate) else 'no match'}")


def exercise_five() -> None:
    """
    Exercise 5: Match Exact Occurrences

    Problem: Match strings of `a` followed by exactly three `b`s.

    Purpose: This exercise demonstrates the {n} quantifier (an exact count).

    Given Input: ["a", "ab", "abb", "abbb", "abbbb", "b"]
    Expected Output: only abbb matches
    """
    pattern = r"ab{3}"
    for candidate in ["a", "ab", "abb", "abbb", "abbbb", "b"]:
        print(f"{candidate!r}: {'match' if re.fullmatch(pattern, candidate) else 'no match'}")


def exercise_six() -> None:
    """
    Exercise 6: Match Range of Occurrences

    Problem: Match strings of `a` followed by two to three `b`s.

    Purpose: This exercise demonstrates the {m,n} quantifier (a range).

    Given Input: ["a", "ab", "abb", "abbb", "abbbb", "b"]
    Expected Output: abb, abbb match; others do not
    """
    pattern = r"ab{2,3}"
    for candidate in ["a", "ab", "abb", "abbb", "abbbb", "b"]:
        print(f"{candidate!r}: {'match' if re.fullmatch(pattern, candidate) else 'no match'}")


def exercise_seven() -> None:
    """
    Exercise 7: Find Underscore-Joined Lowercase

    Problem: Match lowercase words joined by underscores.

    Purpose: This exercise groups a repeated segment: a lowercase run, then one or more
    "_run" groups, requiring at least one underscore join.

    Given Input: several snake_case and non-snake_case strings
    Expected Output: hello_world, foo_bar match
    """
    pattern = r"[a-z]+(?:_[a-z]+)+"
    candidates = ["hello_world", "foo_bar", "hello", "hello_", "_world",
                  "Hello_world", "hello_World"]
    for candidate in candidates:
        if re.fullmatch(pattern, candidate):
            print(candidate)


def exercise_eight() -> None:
    """
    Exercise 8: PascalCase Match

    Problem: Match a single uppercase letter followed by lowercase letters.

    Purpose: This exercise combines a single-character class [A-Z] with a repeated
    [a-z]+, all under fullmatch so trailing digits disqualify a string.

    Given Input: ["Hello", "World", "python", "HELLO", "Hello123", "H", "Ha"]
    Expected Output: Hello, World, Ha match
    """
    pattern = r"[A-Z][a-z]+"
    for candidate in ["Hello", "World", "python", "HELLO", "Hello123", "H", "Ha"]:
        if re.fullmatch(pattern, candidate):
            print(candidate)


def exercise_nine() -> None:
    """
    Exercise 9: Match Start and End

    Problem: Match strings starting with `a`, ending with `b`, anything between.

    Purpose: This exercise uses . (any char) with * between literal anchors a...b,
    under fullmatch.

    Given Input: ["a123b", "axyzb", "ab", "a b", "ab ", "b123a", "a123"]
    Expected Output: first four match; last three do not
    """
    pattern = r"a.*b"
    for candidate in ["a123b", "axyzb", "ab", "a b", "ab ", "b123a", "a123"]:
        print(f"{candidate!r}: {'match' if re.fullmatch(pattern, candidate) else 'no match'}")


def exercise_ten() -> None:
    """
    Exercise 10: Match Word at Start

    Problem: Match if "Hello" appears at the very beginning as a whole word.

    Purpose: This exercise combines ^ (start) with \\b (word boundary) so "HelloWorld"
    is rejected (no boundary after "Hello").

    Given Input: ["Hello world", "Hello", "Say Hello", "hello world", "HelloWorld"]
    Expected Output: first two match
    """
    pattern = r"^Hello\b"
    for candidate in ["Hello world", "Hello", "Say Hello", "hello world", "HelloWorld"]:
        if re.search(pattern, candidate):
            print(candidate)


def exercise_eleven() -> None:
    """
    Exercise 11: Match Word at End

    Problem: Match if "Python" appears at the end, allowing optional punctuation.

    Purpose: This exercise anchors with $ and allows an optional [.!] before it.

    Given Input: ["I love Python", "Python is great", "I love Python!", "python", "I love Python."]
    Expected Output: first, third, and fifth match
    """
    pattern = r"Python[.!]?$"
    candidates = ["I love Python", "Python is great", "I love Python!",
                  "python", "I love Python."]
    for candidate in candidates:
        if re.search(pattern, candidate):
            print(candidate)


def exercise_twelve() -> None:
    """
    Exercise 12: Find Words Containing a Letter

    Problem: Find all words containing the letter `z`.

    Purpose: This exercise uses findall with \\w*z\\w* between word boundaries to grab
    whole words that include z.

    Given Input: "The pizza was amazing but the fizz and buzz were too loud"
    Expected Output: ['pizza', 'amazing', 'fizz', 'buzz']
    """
    text = "The pizza was amazing but the fizz and buzz were too loud"
    print(re.findall(r"\b\w*z\w*\b", text))


def exercise_thirteen() -> None:
    """
    Exercise 13: Find Letter in the Middle

    Problem: Find words where `z` is neither the first nor the last letter.

    Purpose: This exercise first grabs the z-words, then filters out any that start or
    end with z, which a single regex expresses less readably.

    Given Input: "The pizza was amazing but the fizz and buzz were too loud"
    Expected Output: ['pizza', 'amazing']
    """
    text = "The pizza was amazing but the fizz and buzz were too loud"
    z_words = re.findall(r"\b\w+\b", text)
    middle = [w for w in z_words if "z" in w and not w.startswith("z") and not w.endswith("z")]
    print(middle)


def exercise_fourteen() -> None:
    """
    Exercise 14: Match Adjacent Words

    Problem: Match two consecutive words both starting with `P`.

    Purpose: This exercise matches a P-word, whitespace, then another P-word, all
    case-sensitive.

    Given Input: several phrases
    Expected Output: Peter Parker, Pretty Please, Python Programming
    """
    pattern = r"\bP[a-zA-Z]*\s+P[a-zA-Z]*\b"
    phrases = ["Peter Parker is here", "Paul and Peter met", "Pretty Please",
               "Python Programming is fun", "No match here"]
    for phrase in phrases:
        match = re.search(pattern, phrase)
        if match:
            print(match.group())


def exercise_fifteen() -> None:
    """
    Exercise 15: Filter by Starting Letter

    Problem: Find all words starting with `a` or `e`.

    Purpose: This exercise anchors each word with \\b and uses the class [ae] for the
    first letter.

    Given Input: "an eagle soared above the endless empty arena every afternoon"
    Expected Output: ['an', 'eagle', 'above', 'endless', 'empty', 'arena', 'every', 'afternoon']
    """
    text = "an eagle soared above the endless empty arena every afternoon"
    print(re.findall(r"\b[ae]\w*", text))


def exercise_sixteen() -> None:
    """
    Exercise 16: Validate Alphanumeric ID

    Problem: Verify a string contains only letters, digits, and underscores.

    Purpose: This exercise uses \\w+ under fullmatch (\\w already covers letters, digits,
    and underscore), so any space or punctuation fails.

    Given Input: several candidate IDs
    Expected Output: user_123, User_Name, _leadingUnderscore, ALL_CAPS_99 are valid
    """
    candidates = ["user_123", "User_Name", "invalid id", "bad-char!",
                  "_leadingUnderscore", "ALL_CAPS_99"]
    for candidate in candidates:
        if re.fullmatch(r"\w+", candidate):
            print(f"{candidate}: valid")


def exercise_seventeen() -> None:
    """
    Exercise 17: Check Starting Number

    Problem: Verify if a string starts with the number 42 (as a whole token).

    Purpose: This exercise anchors with ^ and uses \\b so "420" is rejected.

    Given Input: ["42 is the answer", "42", "The answer is 42", "420 wide", "142 steps"]
    Expected Output: first two match
    """
    for candidate in ["42 is the answer", "42", "The answer is 42", "420 wide", "142 steps"]:
        if re.search(r"^42\b", candidate):
            print(candidate)


def exercise_eighteen() -> None:
    """
    Exercise 18: Number at End

    Problem: Check if a string ends with a digit.

    Purpose: This exercise anchors a single \\d to $.

    Given Input: ["version 2", "file_backup_3", "hello", "order 99b", "track5", "2024"]
    Expected Output: version 2, file_backup_3, track5, 2024
    """
    for candidate in ["version 2", "file_backup_3", "hello", "order 99b", "track5", "2024"]:
        if re.search(r"\d$", candidate):
            print(candidate)


def exercise_nineteen() -> None:
    """
    Exercise 19: Clean IP Addresses

    Problem: Remove leading zeros from each IP segment.

    Purpose: This exercise uses sub with a backreference: \\b0+(\\d) matches leading
    zeros before a digit, and \\1 keeps just that digit.

    Given Input: ["192.168.001.001", "010.000.000.001", "255.255.255.000", "192.168.1.1"]
    Expected Output: 192.168.1.1, 10.0.0.1, 255.255.255.0, 192.168.1.1
    """
    for ip in ["192.168.001.001", "010.000.000.001", "255.255.255.000", "192.168.1.1"]:
        print(re.sub(r"\b0+(\d)", r"\1", ip))


def exercise_twenty() -> None:
    """
    Exercise 20: Convert Date Format

    Problem: Convert dates from yyyy-mm-dd to dd-mm-yyyy.

    Purpose: This exercise captures three groups and reorders them in the replacement
    via backreferences \\3-\\2-\\1.

    Given Input: ["2024-01-15", "1999-12-31", "2000-07-04", "2024-11-05"]
    Expected Output: 15-01-2024, 31-12-1999, 04-07-2000, 05-11-2024
    """
    for date in ["2024-01-15", "1999-12-31", "2000-07-04", "2024-11-05"]:
        print(re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3-\2-\1", date))


def exercise_twenty_one() -> None:
    """
    Exercise 21: Extract 1-3 Digit Numbers

    Problem: Extract all numbers that are 1 to 3 digits long.

    Purpose: This exercise uses \\b\\d{1,3}\\b; the boundaries ensure a 4-digit number
    like 1000 is NOT captured as "100".

    Given Input: a sentence with numbers of varying lengths
    Expected Output: ['3', '12', '500', '42']
    """
    text = "There are 3 cats, 12 dogs, 500 fish, 1000 birds, and 42 turtles in the sanctuary"
    print(re.findall(r"\b\d{1,3}\b", text))


def exercise_twenty_two() -> None:
    """
    Exercise 22: Search Literal Strings

    Problem: Find multiple literal strings and report their positions.

    Purpose: This exercise uses search per target and reads .start()/.end() from the
    match object (guarded against None).

    Given Input: "The quick brown fox jumps over the lazy dog", targets fox and dog
    Expected Output: positions of "fox" and "dog"
    """
    text = "The quick brown fox jumps over the lazy dog"
    for target in ["fox", "dog"]:
        match = re.search(target, text)
        if match:
            print(f'Found "{target}" at {match.start()}-{match.end()}')


def exercise_twenty_three() -> None:
    """
    Exercise 23: Find Pattern Location

    Problem: Find a literal string and return its exact start/end positions.

    Purpose: This exercise shows that a match object carries the span of the match.

    Given Input: "The quick brown fox jumps over the lazy dog", target "brown fox"
    Expected Output: Found "brown fox" at start=10, end=19
    """
    text = "The quick brown fox jumps over the lazy dog"
    match = re.search(r"brown fox", text)
    if match:
        print(f'Found "brown fox" at start={match.start()}, end={match.end()}')


def exercise_twenty_four() -> None:
    """
    Exercise 24: Find All Substrings

    Problem: Find all occurrences of the substring "cat".

    Purpose: This exercise uses findall to collect every match and len() to count them.

    Given Input: "cat and cattle and catfish and catch and tomcat"
    Expected Output: ['cat', 'cat', 'cat', 'cat', 'cat'], Total count: 5
    """
    text = "cat and cattle and catfish and catch and tomcat"
    matches = re.findall(r"cat", text)
    print(matches)
    print(f"Total count: {len(matches)}")


def exercise_twenty_five() -> None:
    """
    Exercise 25: Iterate Matches

    Problem: Find all occurrences with their position information.

    Purpose: This exercise uses finditer, which yields match objects so you get both
    the text and its span.

    Given Input: "cat and cattle and catfish and catch and tomcat"
    Expected Output: five matches with their start-end positions
    """
    text = "cat and cattle and catfish and catch and tomcat"
    for match in re.finditer(r"cat", text):
        print(f"{match.group()} at {match.start()}-{match.end()}")


def exercise_twenty_six() -> None:
    """
    Exercise 26: Extract Date from URL

    Problem: Extract year, month, day from a URL of the form .../yyyy/mm/dd/slug.

    Purpose: This exercise captures three numeric groups from within a larger pattern
    and reads them by group number.

    Given Input: three blog/news URLs
    Expected Output: the (year, month, day) extracted from each
    """
    urls = [
        "https://example.com/2026/05/22/my-article",
        "https://news.site.org/2019/11/03/breaking-story",
        "https://blog.example.com/2023/07/30/summer-update",
    ]
    for url in urls:
        match = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", url)
        if match:
            print(f"year={match.group(1)} month={match.group(2)} day={match.group(3)}")


def exercise_twenty_seven() -> None:
    """
    Exercise 27: Extract All Numbers

    Problem: Extract all numeric values, including decimals.

    Purpose: This exercise uses \\d+(?:\\.\\d+)? so an optional fractional part is
    captured as part of the same number.

    Given Input: a sentence mixing integers and decimals
    Expected Output: ['2024', '1200', '3', '98.5', '76', '100']
    """
    text = "In 2024 there were 1200 participants across 3 events, with scores of 98.5, 76, and 100"
    print(re.findall(r"\d+(?:\.\d+)?", text))


def exercise_twenty_eight() -> None:
    """
    Exercise 28: Extract Email Addresses

    Problem: Extract valid email addresses from unstructured text.

    Purpose: This exercise uses a practical email pattern: a local part, @, a domain,
    and at least one dot-suffix.

    Given Input: multi-line text with valid and invalid emails
    Expected Output: the four valid email addresses
    """
    text = (
        "Contact support@example.com or admin.team@company.org today. "
        "Bad ones: not-an-email, @nope.com, missing@. "
        "Reach sales@shop.co.uk and billing_dept+invoices@finance.example.net."
    )
    print(re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text))


def exercise_twenty_nine() -> None:
    """
    Exercise 29: Swap Characters

    Problem: Replace spaces with underscores and underscores with spaces, at once.

    Purpose: This exercise uses sub with a callback function so each match is replaced
    based on what it is, enabling a simultaneous swap in a single pass.

    Given Input: ["hello world", "hello_world", "the quick_brown fox_jumps", "no_change"]
    Expected Output: each string with spaces and underscores swapped
    """
    def swap(match: re.Match[str]) -> str:
        return "_" if match.group() == " " else " "

    for text in ["hello world", "hello_world", "the quick_brown fox_jumps", "no_change"]:
        print(re.sub(r"[ _]", swap, text))


def exercise_thirty() -> None:
    """
    Exercise 30: Replace Multiple Delimiters

    Problem: Replace spaces, commas, and dots with colons.

    Purpose: This exercise uses a character class [ ,.] with + so a run of mixed
    delimiters collapses to a single colon.

    Given Input: several strings with different delimiters
    Expected Output: all converted to colon-separated values
    """
    for text in ["one two three", "one,two,three", "one.two.three",
                 "one, two. three", "no.delimiters,here today"]:
        print(re.sub(r"[ ,.]+", ":", text))


def main() -> None:
    print("=== Exercise 1: Check Allowed Characters ===")
    exercise_one()

    print("\n=== Exercise 2: Match Zero or More ===")
    exercise_two()

    print("\n=== Exercise 3: Match One or More ===")
    exercise_three()

    print("\n=== Exercise 4: Match Optional Characters ===")
    exercise_four()

    print("\n=== Exercise 5: Match Exact Occurrences ===")
    exercise_five()

    print("\n=== Exercise 6: Match Range of Occurrences ===")
    exercise_six()

    print("\n=== Exercise 7: Find Underscore-Joined Lowercase ===")
    exercise_seven()

    print("\n=== Exercise 8: PascalCase Match ===")
    exercise_eight()

    print("\n=== Exercise 9: Match Start and End ===")
    exercise_nine()

    print("\n=== Exercise 10: Match Word at Start ===")
    exercise_ten()

    print("\n=== Exercise 11: Match Word at End ===")
    exercise_eleven()

    print("\n=== Exercise 12: Find Words Containing a Letter ===")
    exercise_twelve()

    print("\n=== Exercise 13: Find Letter in the Middle ===")
    exercise_thirteen()

    print("\n=== Exercise 14: Match Adjacent Words ===")
    exercise_fourteen()

    print("\n=== Exercise 15: Filter by Starting Letter ===")
    exercise_fifteen()

    print("\n=== Exercise 16: Validate Alphanumeric ID ===")
    exercise_sixteen()

    print("\n=== Exercise 17: Check Starting Number ===")
    exercise_seventeen()

    print("\n=== Exercise 18: Number at End ===")
    exercise_eighteen()

    print("\n=== Exercise 19: Clean IP Addresses ===")
    exercise_nineteen()

    print("\n=== Exercise 20: Convert Date Format ===")
    exercise_twenty()

    print("\n=== Exercise 21: Extract 1-3 Digit Numbers ===")
    exercise_twenty_one()

    print("\n=== Exercise 22: Search Literal Strings ===")
    exercise_twenty_two()

    print("\n=== Exercise 23: Find Pattern Location ===")
    exercise_twenty_three()

    print("\n=== Exercise 24: Find All Substrings ===")
    exercise_twenty_four()

    print("\n=== Exercise 25: Iterate Matches ===")
    exercise_twenty_five()

    print("\n=== Exercise 26: Extract Date from URL ===")
    exercise_twenty_six()

    print("\n=== Exercise 27: Extract All Numbers ===")
    exercise_twenty_seven()

    print("\n=== Exercise 28: Extract Email Addresses ===")
    exercise_twenty_eight()

    print("\n=== Exercise 29: Swap Characters ===")
    exercise_twenty_nine()

    print("\n=== Exercise 30: Replace Multiple Delimiters ===")
    exercise_thirty()


main()
