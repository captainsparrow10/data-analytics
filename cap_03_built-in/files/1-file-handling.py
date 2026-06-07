"""
File Handling: A Complete Guide to Reading and Writing Files in Python

File handling lets a program persist data to disk and read it back. The core tool is
open(path, mode), best used inside a `with` block so the file is closed automatically.
The os and pathlib modules add filesystem operations (existence checks, rename, delete,
listing directories). This file contains 34 exercises covering file handling.

NOTE ON RUNNABILITY: Every exercise is fully self-contained. Instead of touching real
files in the working directory (or blocking on input()), each one creates a temporary
directory with tempfile.TemporaryDirectory(), does its work there, and cleans up
automatically. Where the original problem asked for input(), a fixed value is used so
the file runs end to end without human interaction.

=== FILE HANDLING CONCEPTS ===

1. OPEN MODES
   Description: "r" read, "w" write/truncate, "a" append, "x" create, "+" read+write,
                "b" binary (e.g. "rb", "wb")
   Example: open("f.txt", "w")

2. WITH STATEMENT (context manager)
   Description: Guarantees the file is closed even if an error occurs
   Example: with open("f.txt") as file: ...

3. READING (read, readline, readlines, iteration)
   Description: Whole file, one line, list of lines, or lazy line-by-line looping
   Example: for line in file: ...

4. WRITING (write, writelines)
   Description: Write a string, or write an iterable of strings
   Example: file.write("hi")

5. PATHLIB (Path)
   Description: Object-oriented paths: .exists(), .read_text(), .write_text(), .iterdir()
   Example: Path("f.txt").read_text()

6. OS MODULE
   Description: os.rename, os.remove, os.listdir, os.path.getsize, os.path.exists
   Example: os.remove("f.txt")

7. EXCEPTIONS
   Description: FileNotFoundError when a file is missing; handle with try/except
   Example: except FileNotFoundError: ...

8. BINARY MODE
   Description: Read/write raw bytes for non-text files (images, etc.)
   Example: open("img.jpg", "rb").read()

Run:
    poetry run python cap_03_built-in/files/1-file-handling.py
"""

import os
import tempfile
from pathlib import Path


def exercise_one() -> None:
    """
    Exercise 1: Write User Name to File

    Problem: Accept a user's name and write it to user.txt.

    Purpose: This exercise shows the basic write workflow: open in "w" mode and write
    a string. input() is replaced with a fixed name so the demo is non-interactive.

    Given Input: name = "Alice" (would normally come from input())
    Expected Output: user.txt created containing the name
    """
    name = "Alice"  # would be: name = input("Enter your name: ")
    with tempfile.TemporaryDirectory() as tmp:
        user_file = Path(tmp) / "user.txt"
        user_file.write_text(name)
        print(f"Wrote to user.txt: {user_file.read_text()}")


def exercise_two() -> None:
    """
    Exercise 2: Read and Print Complete File

    Problem: Open data.txt and print its entire contents.

    Purpose: This exercise shows reading a whole file at once with .read().

    Given Input: data.txt containing "Hello, World!"
    Expected Output: Hello, World!
    """
    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "data.txt"
        data_file.write_text("Hello, World!")
        with data_file.open() as file:
            print(file.read())


def exercise_three() -> None:
    """
    Exercise 3: Read File Line by Line Using Loop

    Problem: Read lines.txt and print each line using a loop.

    Purpose: This exercise shows that iterating a file object yields one line at a
    time, lazily. rstrip removes the trailing newline so print does not double-space.

    Given Input: lines.txt with three lines
    Expected Output: each line on its own row
    """
    with tempfile.TemporaryDirectory() as tmp:
        lines_file = Path(tmp) / "lines.txt"
        lines_file.write_text("Line 1\nLine 2\nLine 3\n")
        with lines_file.open() as file:
            for line in file:
                print(line.rstrip("\n"))


def exercise_four() -> None:
    """
    Exercise 4: Read File Lines into a List

    Problem: Read all lines from items.txt into a list and print it.

    Purpose: This exercise shows .readlines(), which returns every line as a list
    element WITH its trailing newline preserved.

    Given Input: items.txt with apple, banana, cherry (one per line)
    Expected Output: ['apple\\n', 'banana\\n', 'cherry\\n']
    """
    with tempfile.TemporaryDirectory() as tmp:
        items_file = Path(tmp) / "items.txt"
        items_file.write_text("apple\nbanana\ncherry\n")
        with items_file.open() as file:
            print(file.readlines())


def exercise_five() -> None:
    """
    Exercise 5: Append New Sentence to Existing File

    Problem: Append "This is a new line." to notes.txt.

    Purpose: This exercise shows "a" (append) mode, which adds to the end of a file
    without erasing the existing content (unlike "w").

    Given Input: notes.txt containing "Original content."
    Expected Output: both the original and new lines
    """
    with tempfile.TemporaryDirectory() as tmp:
        notes_file = Path(tmp) / "notes.txt"
        notes_file.write_text("Original content.\n")
        with notes_file.open("a") as file:
            file.write("This is a new line.\n")
        print(notes_file.read_text(), end="")


def exercise_six() -> None:
    """
    Exercise 6: Clear All File Content

    Problem: Clear all content from temp.txt.

    Purpose: This exercise shows that opening a file in "w" mode truncates it to zero
    bytes immediately, even if you write nothing.

    Given Input: temp.txt with existing text
    Expected Output: file size becomes 0 bytes
    """
    with tempfile.TemporaryDirectory() as tmp:
        temp_file = Path(tmp) / "temp.txt"
        temp_file.write_text("some existing text")
        with temp_file.open("w"):
            pass  # opening in "w" truncates the file
        print(f"File size: {temp_file.stat().st_size} bytes")


def exercise_seven() -> None:
    """
    Exercise 7: Write Text to New File

    Problem: Create output.txt and write three lines to it.

    Purpose: This exercise shows .writelines(), which writes an iterable of strings
    (it does NOT add newlines for you, so they are included explicitly).

    Given Input: three predefined lines
    Expected Output: output.txt with three lines
    """
    with tempfile.TemporaryDirectory() as tmp:
        output_file = Path(tmp) / "output.txt"
        lines = ["First line\n", "Second line\n", "Third line\n"]
        with output_file.open("w") as file:
            file.writelines(lines)
        print(output_file.read_text(), end="")


def exercise_eight() -> None:
    """
    Exercise 8: Check If File Exists

    Problem: Check whether data.txt exists and print an appropriate message.

    Purpose: This exercise shows Path.exists(), the safe way to test for a file before
    operating on it.

    Given Input: a file that exists and one that does not
    Expected Output: "File exists." then "File does not exist."
    """
    with tempfile.TemporaryDirectory() as tmp:
        existing = Path(tmp) / "data.txt"
        existing.write_text("content")
        missing = Path(tmp) / "ghost.txt"
        for path in (existing, missing):
            print("File exists." if path.exists() else "File does not exist.")


def exercise_nine() -> None:
    """
    Exercise 9: Handle Missing File with Try-Except

    Problem: Attempt to open missing.txt and handle its absence gracefully.

    Purpose: This exercise shows catching FileNotFoundError, the right way to react to
    a file that may not exist rather than letting the program crash.

    Given Input: missing.txt (does not exist)
    Expected Output: Error: The file was not found.
    """
    with tempfile.TemporaryDirectory() as tmp:
        missing = Path(tmp) / "missing.txt"
        try:
            missing.open()
        except FileNotFoundError:
            print("Error: The file was not found.")


def exercise_ten() -> None:
    """
    Exercise 10: Count Total Lines in File

    Problem: Count the total number of lines in data.txt.

    Purpose: This exercise sums 1 per line while iterating, avoiding loading the whole
    file into a list.

    Given Input: data.txt with four lines
    Expected Output: Total lines: 4
    """
    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "data.txt"
        data_file.write_text("Hello\nWorld\nPython\nFile Handling\n")
        with data_file.open() as file:
            total = sum(1 for _ in file)
        print(f"Total lines: {total}")


def exercise_eleven() -> None:
    """
    Exercise 11: Count Total Words in File

    Problem: Count the total number of words in data.txt.

    Purpose: This exercise reads the text and uses .split() (which splits on any
    whitespace) to tokenize into words.

    Given Input: a file with three lines totaling 9 words
    Expected Output: Total words: 9
    """
    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "data.txt"
        data_file.write_text("one two three\nfour five six\nseven eight nine\n")
        total = len(data_file.read_text().split())
        print(f"Total words: {total}")


def exercise_twelve() -> None:
    """
    Exercise 12: Count Total Characters in File

    Problem: Count total characters including spaces.

    Purpose: This exercise uses len() on the read content. Here the text has no
    trailing newline, so the count is exactly the visible characters.

    Given Input: data.txt containing "Hello, World!"
    Expected Output: Total characters: 13
    """
    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "data.txt"
        data_file.write_text("Hello, World!")
        print(f"Total characters: {len(data_file.read_text())}")


def exercise_thirteen() -> None:
    """
    Exercise 13: Count Specific Word Occurrences in File

    Problem: Count how many times the word "Python" appears in data.txt.

    Purpose: This exercise tokenizes the text and counts a specific word with
    list.count().

    Given Input: a file where "Python" appears three times
    Expected Output: Occurrences of 'Python': 3
    """
    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "data.txt"
        data_file.write_text("Python is great\nI love Python\nPython rocks\n")
        count = data_file.read_text().split().count("Python")
        print(f"Occurrences of 'Python': {count}")


def exercise_fourteen() -> None:
    """
    Exercise 14: Read Only First N Lines

    Problem: Read and print only the first 3 lines from data.txt.

    Purpose: This exercise stops early using enumerate and a break, so it never reads
    more than necessary.

    Given Input: a file with five lines
    Expected Output: the first three lines
    """
    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "data.txt"
        data_file.write_text("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")
        with data_file.open() as file:
            for index, line in enumerate(file):
                if index == 3:
                    break
                print(line.rstrip("\n"))


def exercise_fifteen() -> None:
    """
    Exercise 15: Read Only Last N Lines

    Problem: Read and print only the last 3 lines from data.txt.

    Purpose: This exercise reads all lines into a list, then slices the last three
    with [-3:].

    Given Input: a file with five lines
    Expected Output: lines 3, 4, 5
    """
    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "data.txt"
        data_file.write_text("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")
        last_three = data_file.read_text().splitlines()[-3:]
        for line in last_three:
            print(line)


def exercise_sixteen() -> None:
    """
    Exercise 16: Read Specific Line Numbers from File

    Problem: Print only the lines at positions 1, 3, and 5 (1-based).

    Purpose: This exercise converts 1-based positions to 0-based list indices and
    selects them.

    Given Input: a file with five lines
    Expected Output: lines 1, 3, and 5
    """
    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "data.txt"
        data_file.write_text("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")
        lines = data_file.read_text().splitlines()
        for position in (1, 3, 5):
            print(lines[position - 1])


def exercise_seventeen() -> None:
    """
    Exercise 17: Find Longest Word in File

    Problem: Find the longest word in a text file.

    Purpose: This exercise tokenizes the text and uses max(..., key=len) to pick the
    longest word.

    Given Input: words.txt containing "Python is a powerful programming language"
    Expected Output: Longest word: programming
    """
    with tempfile.TemporaryDirectory() as tmp:
        words_file = Path(tmp) / "words.txt"
        words_file.write_text("Python is a powerful programming language")
        longest = max(words_file.read_text().split(), key=len)
        print(f"Longest word: {longest}")


def exercise_eighteen() -> None:
    """
    Exercise 18: Count Each Letter Frequency in File

    Problem: Count how many times each letter appears.

    Purpose: This exercise builds a frequency dict over the alphabetic characters of
    the file, lowercased so case does not split the counts.

    Given Input: sample.txt containing "Hello World"
    Expected Output: each letter with its count
    """
    with tempfile.TemporaryDirectory() as tmp:
        sample_file = Path(tmp) / "sample.txt"
        sample_file.write_text("Hello World")
        freq: dict[str, int] = {}
        for char in sample_file.read_text().lower():
            if char.isalpha():
                freq[char] = freq.get(char, 0) + 1
        print(freq)


def exercise_nineteen() -> None:
    """
    Exercise 19: Search Word and Print Matching Line Numbers

    Problem: Print the line numbers where a specific word appears.

    Purpose: This exercise uses enumerate(start=1) for human-friendly 1-based line
    numbering while scanning for the keyword.

    Given Input: notes.txt where "Python" appears on lines 1 and 3
    Expected Output: "Python" found on line 1, then line 3
    """
    with tempfile.TemporaryDirectory() as tmp:
        notes_file = Path(tmp) / "notes.txt"
        notes_file.write_text("Python rocks\nJava is ok\nlearning Python\n")
        with notes_file.open() as file:
            for number, line in enumerate(file, start=1):
                if "Python" in line:
                    print(f'"Python" found on line {number}')


def exercise_twenty() -> None:
    """
    Exercise 20: Strip Extra Whitespace and Save to New File

    Problem: Remove leading/trailing whitespace from each line and save the result.

    Purpose: This exercise reads, transforms with .strip() per line, and writes a new
    cleaned file, a typical read-process-write pipeline.

    Given Input: messy.txt with extra whitespace
    Expected Output: clean.txt with trimmed lines
    """
    with tempfile.TemporaryDirectory() as tmp:
        messy = Path(tmp) / "messy.txt"
        clean = Path(tmp) / "clean.txt"
        messy.write_text("   hello   \n\t world \n  python  \n")
        cleaned = [line.strip() for line in messy.read_text().splitlines()]
        clean.write_text("\n".join(cleaned) + "\n")
        print(clean.read_text(), end="")


def exercise_twenty_one() -> None:
    """
    Exercise 21: Convert Uppercase to Lowercase and Vice Versa

    Problem: Swap the case of every letter and save to a new file.

    Purpose: This exercise applies str.swapcase() to the whole content before writing
    it out.

    Given Input: input.txt containing "Hello World"
    Expected Output: swapped.txt containing "hELLO wORLD"
    """
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "input.txt"
        swapped = Path(tmp) / "swapped.txt"
        source.write_text("Hello World")
        swapped.write_text(source.read_text().swapcase())
        print(swapped.read_text())


def exercise_twenty_two() -> None:
    """
    Exercise 22: Find and Replace a Word Throughout File

    Problem: Replace every occurrence of a word and save the updated content.

    Purpose: This exercise reads the text, applies str.replace(), and writes it back,
    overwriting the original.

    Given Input: story.txt = "I love Java. Java is great.", replace "Java" with "Python"
    Expected Output: "I love Python. Python is great."
    """
    with tempfile.TemporaryDirectory() as tmp:
        story = Path(tmp) / "story.txt"
        story.write_text("I love Java. Java is great.")
        story.write_text(story.read_text().replace("Java", "Python"))
        print(story.read_text())


def exercise_twenty_three() -> None:
    """
    Exercise 23: Get File Size in Kilobytes

    Problem: Display the size of a file in kilobytes.

    Purpose: This exercise reads the byte size with os.path.getsize and divides by
    1024 to convert to KB.

    Given Input: data.txt with 2048 bytes
    Expected Output: File size: 2.0 KB
    """
    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / "data.txt"
        data_file.write_text("A" * 2048)
        size_kb = os.path.getsize(data_file) / 1024
        print(f"File size: {size_kb:.1f} KB")


def exercise_twenty_four() -> None:
    """
    Exercise 24: Copy File Using Binary Mode

    Problem: Copy one file to another using binary mode.

    Purpose: This exercise reads bytes ("rb") and writes bytes ("wb"), which works for
    any file type (text or binary) without worrying about encoding.

    Given Input: source.txt
    Expected Output: destination.txt with identical content
    """
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "source.txt"
        destination = Path(tmp) / "destination.txt"
        source.write_text("copy me byte for byte")
        with source.open("rb") as src, destination.open("wb") as dst:
            dst.write(src.read())
        print(f"Copied. destination.txt = {destination.read_text()}")


def exercise_twenty_five() -> None:
    """
    Exercise 25: Rename a Single File

    Problem: Rename a single file using the os module.

    Purpose: This exercise shows os.rename(old, new), which moves/renames a file on
    disk.

    Given Input: old_name.txt
    Expected Output: File renamed successfully.
    """
    with tempfile.TemporaryDirectory() as tmp:
        old_name = Path(tmp) / "old_name.txt"
        new_name = Path(tmp) / "new_name.txt"
        old_name.write_text("content")
        os.rename(old_name, new_name)
        print("File renamed successfully." if new_name.exists() else "Rename failed.")


def exercise_twenty_six() -> None:
    """
    Exercise 26: Rename Multiple Files with Prefix

    Problem: Add a prefix to all .txt files in a directory.

    Purpose: This exercise lists matching files and renames each, building the new
    name from a prefix plus the original.

    Given Input: notes.txt and data.txt, prefix "2024_"
    Expected Output: renamed files confirmed
    """
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        (base / "notes.txt").write_text("n")
        (base / "data.txt").write_text("d")
        for txt_file in sorted(base.glob("*.txt")):
            txt_file.rename(base / f"2024_{txt_file.name}")
        print(sorted(p.name for p in base.glob("*.txt")))


def exercise_twenty_seven() -> None:
    """
    Exercise 27: Delete a File from Disk

    Problem: Delete a file, checking that it exists first.

    Purpose: This exercise guards os.remove with an existence check so deleting a
    missing file does not raise.

    Given Input: temp.txt
    Expected Output: temp.txt has been deleted.
    """
    with tempfile.TemporaryDirectory() as tmp:
        temp_file = Path(tmp) / "temp.txt"
        temp_file.write_text("delete me")
        if temp_file.exists():
            os.remove(temp_file)
            print("temp.txt has been deleted.")


def exercise_twenty_eight() -> None:
    """
    Exercise 28: Merge Two Files into One

    Problem: Combine the contents of two files into a single file.

    Purpose: This exercise concatenates the text of both sources and writes it to a
    merged output.

    Given Input: file1.txt and file2.txt
    Expected Output: merged.txt with both contents
    """
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        file1 = base / "file1.txt"
        file2 = base / "file2.txt"
        merged = base / "merged.txt"
        file1.write_text("Hello from file 1.\n")
        file2.write_text("Hello from file 2.\n")
        merged.write_text(file1.read_text() + file2.read_text())
        print(merged.read_text(), end="")


def exercise_twenty_nine() -> None:
    """
    Exercise 29: Reverse Line Order and Save to New File

    Problem: Reverse the order of lines and save to a new file.

    Purpose: This exercise reads the lines, reverses the list with [::-1], and writes
    them out in the new order.

    Given Input: original.txt with three lines
    Expected Output: reversed.txt with the lines in reverse order
    """
    with tempfile.TemporaryDirectory() as tmp:
        original = Path(tmp) / "original.txt"
        reversed_file = Path(tmp) / "reversed.txt"
        original.write_text("Line 1\nLine 2\nLine 3\n")
        lines = original.read_text().splitlines()
        reversed_file.write_text("\n".join(lines[::-1]) + "\n")
        print(reversed_file.read_text(), end="")


def exercise_thirty() -> None:
    """
    Exercise 30: List All Files in Directory and Save

    Problem: List all files in a directory and save their names to a text file.

    Purpose: This exercise enumerates a directory with Path.iterdir() and writes one
    filename per line.

    Given Input: a folder with notes.txt, data.csv, report.pdf
    Expected Output: file_list.txt with one filename per line
    """
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp) / "my_folder"
        folder.mkdir()
        for name in ["notes.txt", "data.csv", "report.pdf"]:
            (folder / name).write_text("x")
        file_list = Path(tmp) / "file_list.txt"
        names = sorted(p.name for p in folder.iterdir())
        file_list.write_text("\n".join(names) + "\n")
        print(file_list.read_text(), end="")


def exercise_thirty_one() -> None:
    """
    Exercise 31: Read and Write Binary Image File

    Problem: Read a binary file and write its contents to a new file (duplication).

    Purpose: This exercise demonstrates binary I/O with raw bytes, which is what image
    duplication requires. A few bytes simulate a JPEG so the demo is self-contained.

    Given Input: photo.jpg (simulated bytes)
    Expected Output: photo_copy.jpg with identical bytes
    """
    with tempfile.TemporaryDirectory() as tmp:
        photo = Path(tmp) / "photo.jpg"
        copy = Path(tmp) / "photo_copy.jpg"
        photo.write_bytes(b"\xff\xd8\xff\xe0fake-jpeg-bytes\xff\xd9")
        copy.write_bytes(photo.read_bytes())
        print(f"Copy identical: {photo.read_bytes() == copy.read_bytes()}")


def exercise_thirty_two() -> None:
    """
    Exercise 32: Extract and Sort Unique Words from File

    Problem: Extract unique words, sort them alphabetically, and print them.

    Purpose: This exercise combines set() (to dedupe) with sorted() (to order),
    a compact way to produce a clean vocabulary list.

    Given Input: paragraph.txt = "the cat sat on the mat the cat"
    Expected Output: ['cat', 'mat', 'on', 'sat', 'the']
    """
    with tempfile.TemporaryDirectory() as tmp:
        paragraph = Path(tmp) / "paragraph.txt"
        paragraph.write_text("the cat sat on the mat the cat")
        unique_sorted = sorted(set(paragraph.read_text().split()))
        print(unique_sorted)


def exercise_thirty_three() -> None:
    """
    Exercise 33: Filter Log File Lines Containing ERROR Keyword

    Problem: Print only the lines containing the keyword "ERROR".

    Purpose: This exercise streams the file and prints matching lines, the everyday
    log-grepping pattern.

    Given Input: app.log with mixed log levels
    Expected Output: only the ERROR lines
    """
    with tempfile.TemporaryDirectory() as tmp:
        log_file = Path(tmp) / "app.log"
        log_file.write_text(
            "INFO: ok\nERROR: failed to connect\nWARNING: slow\nERROR: timeout\n"
        )
        with log_file.open() as file:
            for line in file:
                if "ERROR" in line:
                    print(line.rstrip("\n"))


def exercise_thirty_four() -> None:
    """
    Exercise 34: Split Large File into Smaller 10-Line Files

    Problem: Split a large file into smaller files of at most 10 lines each.

    Purpose: This exercise pages through the lines in fixed-size chunks, writing each
    chunk to a numbered part file, a common batching task.

    Given Input: large_file.txt with 25 lines
    Expected Output: part_1.txt (10), part_2.txt (10), part_3.txt (5)
    """
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        large = base / "large_file.txt"
        large.write_text("".join(f"Line {i}\n" for i in range(1, 26)))
        lines = large.read_text().splitlines(keepends=True)
        chunk_size = 10
        for part_index, start in enumerate(range(0, len(lines), chunk_size), start=1):
            part = base / f"part_{part_index}.txt"
            part.write_text("".join(lines[start:start + chunk_size]))
            print(f"{part.name}: {len(part.read_text().splitlines())} lines")


def main() -> None:
    print("=== Exercise 1: Write User Name to File ===")
    exercise_one()

    print("\n=== Exercise 2: Read and Print Complete File ===")
    exercise_two()

    print("\n=== Exercise 3: Read File Line by Line Using Loop ===")
    exercise_three()

    print("\n=== Exercise 4: Read File Lines into a List ===")
    exercise_four()

    print("\n=== Exercise 5: Append New Sentence to Existing File ===")
    exercise_five()

    print("\n=== Exercise 6: Clear All File Content ===")
    exercise_six()

    print("\n=== Exercise 7: Write Text to New File ===")
    exercise_seven()

    print("\n=== Exercise 8: Check If File Exists ===")
    exercise_eight()

    print("\n=== Exercise 9: Handle Missing File with Try-Except ===")
    exercise_nine()

    print("\n=== Exercise 10: Count Total Lines in File ===")
    exercise_ten()

    print("\n=== Exercise 11: Count Total Words in File ===")
    exercise_eleven()

    print("\n=== Exercise 12: Count Total Characters in File ===")
    exercise_twelve()

    print("\n=== Exercise 13: Count Specific Word Occurrences in File ===")
    exercise_thirteen()

    print("\n=== Exercise 14: Read Only First N Lines ===")
    exercise_fourteen()

    print("\n=== Exercise 15: Read Only Last N Lines ===")
    exercise_fifteen()

    print("\n=== Exercise 16: Read Specific Line Numbers from File ===")
    exercise_sixteen()

    print("\n=== Exercise 17: Find Longest Word in File ===")
    exercise_seventeen()

    print("\n=== Exercise 18: Count Each Letter Frequency in File ===")
    exercise_eighteen()

    print("\n=== Exercise 19: Search Word and Print Matching Line Numbers ===")
    exercise_nineteen()

    print("\n=== Exercise 20: Strip Extra Whitespace and Save to New File ===")
    exercise_twenty()

    print("\n=== Exercise 21: Convert Uppercase to Lowercase and Vice Versa ===")
    exercise_twenty_one()

    print("\n=== Exercise 22: Find and Replace a Word Throughout File ===")
    exercise_twenty_two()

    print("\n=== Exercise 23: Get File Size in Kilobytes ===")
    exercise_twenty_three()

    print("\n=== Exercise 24: Copy File Using Binary Mode ===")
    exercise_twenty_four()

    print("\n=== Exercise 25: Rename a Single File ===")
    exercise_twenty_five()

    print("\n=== Exercise 26: Rename Multiple Files with Prefix ===")
    exercise_twenty_six()

    print("\n=== Exercise 27: Delete a File from Disk ===")
    exercise_twenty_seven()

    print("\n=== Exercise 28: Merge Two Files into One ===")
    exercise_twenty_eight()

    print("\n=== Exercise 29: Reverse Line Order and Save to New File ===")
    exercise_twenty_nine()

    print("\n=== Exercise 30: List All Files in Directory and Save ===")
    exercise_thirty()

    print("\n=== Exercise 31: Read and Write Binary Image File ===")
    exercise_thirty_one()

    print("\n=== Exercise 32: Extract and Sort Unique Words from File ===")
    exercise_thirty_two()

    print("\n=== Exercise 33: Filter Log File Lines Containing ERROR Keyword ===")
    exercise_thirty_three()

    print("\n=== Exercise 34: Split Large File into Smaller 10-Line Files ===")
    exercise_thirty_four()


main()
