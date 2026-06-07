"""
Input & Output: A Complete Guide to Reading Input and Formatting Output in Python

Programs talk to the outside world through input (reading values) and output (printing
results). input() reads a line of text from the user; print() writes to the console
with control over separators and line endings; and f-strings / str.format() format
values precisely (decimals, number bases, alignment, padding, thousands separators).
This file contains 23 exercises covering input and output.

NOTE ON RUNNABILITY: The original exercises use input() (and getpass for passwords).
Blocking on real input would stop the file from running unattended, so each exercise
uses a fixed value where input() would normally be called, with a comment showing the
real call. File-based exercises use tempfile so they are self-contained.

=== INPUT & OUTPUT CONCEPTS ===

1. INPUT (input(prompt))
   Description: Read a line as a string; convert with int()/float() as needed
   Example: n = int(input("n: "))

2. PRINT OPTIONS (sep=, end=)
   Description: Control what joins arguments and what terminates the line
   Example: print("a", "b", sep="-", end="!")

3. F-STRINGS / FORMAT SPECS
   Description: Inline formatting: :.2f decimals, :>10 align, :05 zero-pad, :, commas
   Example: f"{3.14159:.2f}" = "3.14"

4. NUMBER BASES (bin, oct, hex, format)
   Description: Convert ints to binary/octal/hex text
   Example: f"{255:x}" = "ff"

5. ALIGNMENT (<, >, ^ with a fill char)
   Description: Left, right, or center within a width, optionally padded
   Example: f"{'hi':*^6}" = "**hi**"

6. str.format()
   Description: Positional/keyword templating, the pre-f-string formatting method
   Example: "{} + {}".format(1, 2) = "1 + 2"

7. PASSWORD INPUT (getpass.getpass)
   Description: Read input without echoing it to the screen
   Example: pw = getpass.getpass()

Run:
    poetry run python cap_03_built-in/io/1-input-output.py
"""

import tempfile
from pathlib import Path


def exercise_one() -> None:
    """
    Exercise 1: Accept Numbers from User

    Problem: Take two integers and calculate their multiplication.

    Purpose: This exercise shows reading numbers (here fixed) and arithmetic output.

    Given Input: 10 and 20
    Expected Output: The multiplication is: 200
    """
    first = 10   # first = int(input("First: "))
    second = 20  # second = int(input("Second: "))
    print(f"The multiplication is: {first * second}")


def exercise_two() -> None:
    """
    Exercise 2: Display Variables with Separator

    Problem: Display three words with three asterisks between them.

    Purpose: This exercise uses print()'s sep= argument to control what joins the
    arguments, instead of building the string manually.

    Given Input: "Name", "Is", "James"
    Expected Output: Name***Is***James
    """
    print("Name", "Is", "James", sep="***")


def exercise_three() -> None:
    """
    Exercise 3: Convert Decimal to Octal

    Problem: Accept an integer and display its octal representation.

    Purpose: This exercise uses the :o format spec to render an int in base 8.

    Given Input: 8
    Expected Output: The octal number of decimal number 8 is 10
    """
    number = 8
    print(f"The octal number of decimal number {number} is {number:o}")


def exercise_four() -> None:
    """
    Exercise 4: Binary Representation

    Problem: Accept an integer and display its binary format.

    Purpose: This exercise uses the :b format spec to render an int in base 2.

    Given Input: 45
    Expected Output: The binary representation of 45 is 101101
    """
    number = 45
    print(f"The binary representation of {number} is {number:b}")


def exercise_five() -> None:
    """
    Exercise 5: Accept Three Strings from One Input

    Problem: Take three names in a single input and assign them to separate variables.

    Purpose: This exercise splits one input string on whitespace and unpacks the
    parts into three variables in a single assignment.

    Given Input: "Emma Jessa Kelly"
    Expected Output: Name1: Emma / Name2: Jessa / Name3: Kelly
    """
    raw = "Emma Jessa Kelly"  # raw = input("Enter three names: ")
    name1, name2, name3 = raw.split()
    print(f"Name1: {name1} / Name2: {name2} / Name3: {name3}")


def exercise_six() -> None:
    """
    Exercise 6: Hexadecimal Representation

    Problem: Accept an integer and display its hexadecimal value.

    Purpose: This exercise uses the :x format spec to render an int in base 16
    (lowercase letters).

    Given Input: 255
    Expected Output: The hexadecimal value is ff
    """
    number = 255
    print(f"The hexadecimal value is {number:x}")


def exercise_seven() -> None:
    """
    Exercise 7: Display Float with 2 Decimal Places

    Problem: Display a floating-point number rounded to exactly two decimals.

    Purpose: This exercise uses the :.2f format spec, which both rounds and pads to two
    decimal places.

    Given Input: 458.541315
    Expected Output: 458.54
    """
    number = 458.541315
    print(f"{number:.2f}")


def exercise_eight() -> None:
    """
    Exercise 8: Percentage Display

    Problem: Compute numerator/denominator * 100 and display it with two decimals and
    a percent sign.

    Purpose: This exercise combines arithmetic with a :.2f spec and a literal % sign.

    Given Input: numerator = 22, denominator = 29
    Expected Output: The result is: 75.86%
    """
    numerator = 22
    denominator = 29
    percentage = numerator / denominator * 100
    print(f"The result is: {percentage:.2f}%")


def exercise_nine() -> None:
    """
    Exercise 9: Right-Aligned Output

    Problem: Display a word right-aligned in a 20-character field, followed by a number.

    Purpose: This exercise uses the :>20 alignment spec, which pads on the left so the
    text ends at column 20.

    Given Input: word = "Python", number = 3.14
    Expected Output: 14 spaces then "Python 3.14"
    """
    word = "Python"
    number = 3.14
    print(f"{word:>20} {number}")


def exercise_ten() -> None:
    """
    Exercise 10: Center-Aligned Text

    Problem: Display a string centered in a 40-character field, padded with hyphens.

    Purpose: This exercise uses the :-^40 spec: ^ centers, and the leading '-' sets the
    fill character.

    Given Input: "REPORT SUMMARY"
    Expected Output: 13 hyphens, the text, 13 hyphens
    """
    text = "REPORT SUMMARY"
    print(f"{text:-^40}")


def exercise_eleven() -> None:
    """
    Exercise 11: Padding with Zeros

    Problem: Pad a number with leading zeros to a total width of 5.

    Purpose: This exercise uses the :05d spec, which left-pads an integer with zeros to
    the given width.

    Given Input: 42
    Expected Output: 00042
    """
    number = 42
    print(f"{number:05d}")


def exercise_twelve() -> None:
    """
    Exercise 12: Format Variables Using .format()

    Problem: Use str.format() to display three variables in a template sentence.

    Purpose: This exercise shows the .format() method with positional placeholders, the
    pre-f-string way to interpolate values.

    Given Input: quantity = 3, totalMoney = 450, price = 150
    Expected Output: I have 450 dollars so I can buy 3 football for 150.00 dollars.
    """
    quantity = 3
    total_money = 450
    price = 150
    print(
        "I have {} dollars so I can buy {} football for {:.2f} dollars.".format(
            total_money, quantity, price
        )
    )


def exercise_thirteen() -> None:
    """
    Exercise 13: Currency Formatting with Commas

    Problem: Display a large number as currency with a dollar sign, commas, and two
    decimals.

    Purpose: This exercise combines the , (thousands separator) and .2f specs in one
    format, the idiomatic way to print money.

    Given Input: 1250500.7
    Expected Output: Total Balance: $1,250,500.70
    """
    amount = 1250500.7
    print(f"Total Balance: ${amount:,.2f}")


def exercise_fourteen() -> None:
    """
    Exercise 14: Accept List of 5 Float Numbers

    Problem: Accept 5 float numbers and store them in a list.

    Purpose: This exercise shows building a list of floats (here fixed instead of read)
    and printing it.

    Given Input: 78.6, 78.6, 85.3, 1.2, 3.5
    Expected Output: [78.6, 78.6, 85.3, 1.2, 3.5]
    """
    # numbers = [float(input(f"Number {i + 1}: ")) for i in range(5)]
    numbers = [78.6, 78.6, 85.3, 1.2, 3.5]
    print(numbers)


def exercise_fifteen() -> None:
    """
    Exercise 15: Tabular Output from Lists

    Problem: Print two parallel lists (names and scores) as an aligned table.

    Purpose: This exercise uses alignment specs inside an f-string to line up columns,
    iterating both lists together with zip().

    Given Input: names = ["Alice", "Bob", "Charlie"], scores = [85, 92, 78]
    Expected Output: a table with aligned Name and Score columns
    """
    names = ["Alice", "Bob", "Charlie"]
    scores = [85, 92, 78]
    print(f"{'Name':<10}{'Score':>6}")
    for name, score in zip(names, scores):
        print(f"{name:<10}{score:>6}")


def exercise_sixteen() -> None:
    """
    Exercise 16: Interactive Menu

    Problem: Offer three options and act on the user's selection.

    Purpose: This exercise dispatches on a (fixed) choice value, showing how a menu
    routes to different actions.

    Given Input: choice = 2 (square), number = 5
    Expected Output: The square is: 25
    """
    choice = int("2")  # choice = int(input("Choose 1-3: "))
    number = 5         # number = int(input("Number: "))
    if choice == 1:
        print(f"The cube is: {number ** 3}")
    elif choice == 2:
        print(f"The square is: {number ** 2}")
    else:
        print(f"The double is: {number * 2}")


def exercise_seventeen() -> None:
    """
    Exercise 17: Masked Password Input

    Problem: Read a username normally and a password without echoing it.

    Purpose: This exercise shows where getpass.getpass() would be used to hide typed
    input. Fixed values stand in so the demo is non-interactive.

    Given Input: username = "admin", password = "SecretPassword123"
    Expected Output: Login successful for admin!
    """
    username = "admin"             # username = input("Username: ")
    password = "SecretPassword123"  # password = getpass.getpass("Password: ")
    if username == "admin" and password == "SecretPassword123":
        print(f"Login successful for {username}!")
    else:
        print("Login failed.")


def exercise_eighteen() -> None:
    """
    Exercise 18: Read File and Store in List

    Problem: Read a file and store each line as a list element.

    Purpose: This exercise reads lines and strips newlines so the list holds clean
    strings. A temporary file makes it self-contained.

    Given Input: a file with three lines
    Expected Output: ['Line 1', 'Line 2', 'Line 3']
    """
    with tempfile.TemporaryDirectory() as tmp:
        test_file = Path(tmp) / "test.txt"
        test_file.write_text("Line 1\nLine 2\nLine 3\n")
        lines = [line.rstrip("\n") for line in test_file.open()]
        print(lines)


def exercise_nineteen() -> None:
    """
    Exercise 19: Write List to File

    Problem: Save each fruit on its own line in a file.

    Purpose: This exercise writes a list to a file by joining with newlines, the
    inverse of reading lines into a list.

    Given Input: fruit_list = ["Apple", "Banana", "Cherry", "Date"]
    Expected Output: fruits.txt with one fruit per line
    """
    fruit_list = ["Apple", "Banana", "Cherry", "Date"]
    with tempfile.TemporaryDirectory() as tmp:
        fruits_file = Path(tmp) / "fruits.txt"
        fruits_file.write_text("\n".join(fruit_list) + "\n")
        print(fruits_file.read_text(), end="")


def exercise_twenty() -> None:
    """
    Exercise 20: Count Total Lines in File

    Problem: Determine the total number of lines in a file.

    Purpose: This exercise counts lines by reading them and measuring the list length.

    Given Input: a file with 12 lines
    Expected Output: 12
    """
    with tempfile.TemporaryDirectory() as tmp:
        sample = Path(tmp) / "sample.txt"
        sample.write_text("".join(f"Line {i}\n" for i in range(1, 13)))
        print(len(sample.read_text().splitlines()))


def exercise_twenty_one() -> None:
    """
    Exercise 21: Read Specific Line from File

    Problem: Display only the fourth line of a file.

    Purpose: This exercise reads all lines and indexes the one wanted (index 3 for the
    4th line, since indexing is 0-based).

    Given Input: a file with five lines
    Expected Output: Line 4
    """
    with tempfile.TemporaryDirectory() as tmp:
        test_file = Path(tmp) / "test.txt"
        test_file.write_text("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")
        print(test_file.read_text().splitlines()[3])


def exercise_twenty_two() -> None:
    """
    Exercise 22: Check if File is Empty

    Problem: Check whether a file's size is 0 bytes.

    Purpose: This exercise uses Path.stat().st_size to test emptiness without reading
    the content.

    Given Input: an empty file
    Expected Output: Status: File is empty.
    """
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp) / "empty_log.txt"
        empty.write_text("")
        if empty.stat().st_size == 0:
            print("Status: File is empty.")
        else:
            print("Status: File has content.")


def exercise_twenty_three() -> None:
    """
    Exercise 23: Delete a Specific File

    Problem: Delete a file given its name.

    Purpose: This exercise removes a file with Path.unlink(), guarded by an existence
    check so a missing file does not raise.

    Given Input: old_data.csv
    Expected Output: File 'old_data.csv' has been deleted.
    """
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "old_data.csv"
        target.write_text("data")
        if target.exists():
            target.unlink()
            print("File 'old_data.csv' has been deleted.")


def main() -> None:
    print("=== Exercise 1: Accept Numbers from User ===")
    exercise_one()

    print("\n=== Exercise 2: Display Variables with Separator ===")
    exercise_two()

    print("\n=== Exercise 3: Convert Decimal to Octal ===")
    exercise_three()

    print("\n=== Exercise 4: Binary Representation ===")
    exercise_four()

    print("\n=== Exercise 5: Accept Three Strings from One Input ===")
    exercise_five()

    print("\n=== Exercise 6: Hexadecimal Representation ===")
    exercise_six()

    print("\n=== Exercise 7: Display Float with 2 Decimal Places ===")
    exercise_seven()

    print("\n=== Exercise 8: Percentage Display ===")
    exercise_eight()

    print("\n=== Exercise 9: Right-Aligned Output ===")
    exercise_nine()

    print("\n=== Exercise 10: Center-Aligned Text ===")
    exercise_ten()

    print("\n=== Exercise 11: Padding with Zeros ===")
    exercise_eleven()

    print("\n=== Exercise 12: Format Variables Using .format() ===")
    exercise_twelve()

    print("\n=== Exercise 13: Currency Formatting with Commas ===")
    exercise_thirteen()

    print("\n=== Exercise 14: Accept List of 5 Float Numbers ===")
    exercise_fourteen()

    print("\n=== Exercise 15: Tabular Output from Lists ===")
    exercise_fifteen()

    print("\n=== Exercise 16: Interactive Menu ===")
    exercise_sixteen()

    print("\n=== Exercise 17: Masked Password Input ===")
    exercise_seventeen()

    print("\n=== Exercise 18: Read File and Store in List ===")
    exercise_eighteen()

    print("\n=== Exercise 19: Write List to File ===")
    exercise_nineteen()

    print("\n=== Exercise 20: Count Total Lines in File ===")
    exercise_twenty()

    print("\n=== Exercise 21: Read Specific Line from File ===")
    exercise_twenty_one()

    print("\n=== Exercise 22: Check if File is Empty ===")
    exercise_twenty_two()

    print("\n=== Exercise 23: Delete a Specific File ===")
    exercise_twenty_three()


main()
