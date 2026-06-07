"""
Random Data Generation: A Complete Guide to Randomness in Python

The `random` module produces pseudo-random numbers for simulations, sampling, and
games; it is reproducible via random.seed(). For anything security-sensitive (tokens,
passwords, OTPs) use the `secrets` module instead, which draws from a cryptographically
secure source and is intentionally NOT seedable. This file contains 10 exercises.

NOTE ON REPRODUCIBILITY: Exercises built on `random` call random.seed() so their output
is stable on every run (useful for a reference). Exercises built on `secrets` are
cryptographically random by design, so their output legitimately varies each run.

=== RANDOM CONCEPTS ===

1. FLOATS (random.random(), random.uniform(a, b))
   Description: random() in [0,1); uniform(a, b) in [a, b]
   Example: random.uniform(1, 5)

2. INTEGERS (random.randint(a, b), random.randrange(start, stop, step))
   Description: randint is inclusive; randrange follows range() semantics
   Example: random.randrange(100, 1000, 5)

3. SEQUENCES (choice, choices, sample, shuffle)
   Description: pick one, pick k with replacement, pick k unique, shuffle in place
   Example: random.sample(pool, 2)

4. SEED (random.seed(n))
   Description: Make the pseudo-random stream reproducible
   Example: random.seed(42)

5. SECRETS (secrets.choice, randbelow, token_hex, token_urlsafe)
   Description: Cryptographically secure randomness for tokens/passwords
   Example: secrets.token_hex(16)

6. STRING CONSTANTS (string.ascii_letters, digits, ...)
   Description: Ready-made character pools for building random strings
   Example: string.ascii_uppercase

Run:
    poetry run python cap_03_built-in/stdlib/2-random.py
"""

import datetime
import random
import secrets
import string


def exercise_one() -> None:
    """
    Exercise 1: Generate 3 Random Integers Divisible by 5

    Problem: Generate 3 random integers between 100 and 999 that are divisible by 5.

    Purpose: This exercise uses randrange with a step of 5, which guarantees
    divisibility by 5 without filtering.

    Given Input: range (100, 999), step 5
    Expected Output: three integers between 100 and 995, all divisible by 5
    """
    random.seed(1)
    numbers = [random.randrange(100, 1000, 5) for _ in range(3)]
    print(numbers)


def exercise_two() -> None:
    """
    Exercise 2: Random Lottery Pick

    Problem: Generate 100 unique lottery tickets and pick two winners.

    Purpose: This exercise uses random.sample twice: once to draw 100 unique tickets
    from a huge range, and once to pick 2 unique winners (sample guarantees no repeats).

    Given Input: 100 unique 10-digit numbers
    Expected Output: two winning ticket numbers
    """
    random.seed(2)
    tickets = random.sample(range(1_000_000_000, 10_000_000_000), 100)
    winners = random.sample(tickets, 2)
    print(f"Winning tickets: {winners}")


def exercise_three() -> None:
    """
    Exercise 3: Generate 6-Digit Secure OTP

    Problem: Create a secure one-time password with 6 digits.

    Purpose: This exercise uses secrets (not random) because an OTP is a security
    credential. secrets.randbelow(900000) + 100000 yields a value in 100000..999999.

    Given Input: range 100000-999999
    Expected Output: a 6-digit OTP (varies each run, since secrets is crypto-secure)
    """
    otp = secrets.randbelow(900_000) + 100_000
    print(f"Your OTP is: {otp}")


def exercise_four() -> None:
    """
    Exercise 4: Pick a Random Character

    Problem: Select a random character from the string "pynative".

    Purpose: This exercise uses random.choice, which picks one element from any
    non-empty sequence (a string is a sequence of characters).

    Given Input: name = "pynative"
    Expected Output: one randomly selected character
    """
    random.seed(4)
    name = "pynative"
    print(random.choice(name))


def exercise_five() -> None:
    """
    Exercise 5: Generate a Random String

    Problem: Create a random string of length 5 using letters only.

    Purpose: This exercise picks 5 letters from string.ascii_letters and joins them.
    random.choices draws WITH replacement, so repeats are allowed.

    Given Input: length 5
    Expected Output: a 5-character mixed-case letter string
    """
    random.seed(5)
    result = "".join(random.choices(string.ascii_letters, k=5))
    print(result)


def exercise_six() -> None:
    """
    Exercise 6: Generate a Random Password

    Problem: Generate a 10-character password with at least 2 uppercase letters, at
    least 1 digit, and at least 1 special symbol.

    Purpose: This exercise GUARANTEES the rules by building the required characters
    first, filling the rest, then shuffling so the mandatory characters are not always
    in the same positions.

    Given Input: the password rules above
    Expected Output: a compliant 10-character password
    """
    random.seed(6)
    chars: list[str] = (
        random.choices(string.ascii_uppercase, k=2)   # >= 2 uppercase
        + random.choices(string.digits, k=1)          # >= 1 digit
        + random.choices("!@#$%^&*", k=1)             # >= 1 special
        + random.choices(string.ascii_letters, k=6)   # fill to length 10
    )
    random.shuffle(chars)
    print("".join(chars))


def exercise_seven() -> None:
    """
    Exercise 7: Calculate Multiplication of Two Random Floats

    Problem: Multiply two random floats from specific ranges.

    Purpose: This exercise uses random.uniform, which returns a float anywhere in the
    given inclusive range.

    Given Input: first in [0.1, 1], second in [9.5, 99.5]
    Expected Output: the product of the two random floats
    """
    random.seed(7)
    first = random.uniform(0.1, 1)
    second = random.uniform(9.5, 99.5)
    print(f"{first:.3f} * {second:.3f} = {first * second:.3f}")


def exercise_eight() -> None:
    """
    Exercise 8: Generate Random Token and URL

    Problem: Create a secure token and a URL-safe token.

    Purpose: This exercise uses secrets.token_hex (hexadecimal) and
    secrets.token_urlsafe (URL-safe base64), the standard ways to mint API tokens.

    Given Input: token sizes in bytes
    Expected Output: a hex token and a URL-safe token (vary each run)
    """
    print(f"Hex token: {secrets.token_hex(16)}")
    print(f"URL-safe token: {secrets.token_urlsafe(16)}")


def exercise_nine() -> None:
    """
    Exercise 9: Dice Roll with a Fixed Seed

    Problem: Roll a die 5 times so that you get the SAME number every time.

    Purpose: This exercise demonstrates random.seed: re-seeding with the same value
    before each draw resets the generator, so it produces an identical result every
    time. This is exactly how reproducible "random" tests work.

    Given Input: dice = [1, 2, 3, 4, 5, 6]
    Expected Output: the same number printed five times
    """
    dice = [1, 2, 3, 4, 5, 6]
    for _ in range(5):
        random.seed(42)  # reset the stream -> identical pick every time
        print(random.choice(dice), end=" ")
    print()


def exercise_ten() -> None:
    """
    Exercise 10: Generate a Random Date

    Problem: Create a random date between two given dates.

    Purpose: This exercise converts the problem to numbers: take the day span between
    the bounds, pick a random offset in that span, and add it to the start date.

    Given Input: 2016-01-01 to 2018-12-12
    Expected Output: a random date within the range
    """
    random.seed(10)
    start = datetime.date(2016, 1, 1)
    end = datetime.date(2018, 12, 12)
    span_days = (end - start).days
    random_date = start + datetime.timedelta(days=random.randrange(span_days))
    print(random_date)


def main() -> None:
    print("=== Exercise 1: Generate 3 Random Integers Divisible by 5 ===")
    exercise_one()

    print("\n=== Exercise 2: Random Lottery Pick ===")
    exercise_two()

    print("\n=== Exercise 3: Generate 6-Digit Secure OTP ===")
    exercise_three()

    print("\n=== Exercise 4: Pick a Random Character ===")
    exercise_four()

    print("\n=== Exercise 5: Generate a Random String ===")
    exercise_five()

    print("\n=== Exercise 6: Generate a Random Password ===")
    exercise_six()

    print("\n=== Exercise 7: Calculate Multiplication of Two Random Floats ===")
    exercise_seven()

    print("\n=== Exercise 8: Generate Random Token and URL ===")
    exercise_eight()

    print("\n=== Exercise 9: Dice Roll with a Fixed Seed ===")
    exercise_nine()

    print("\n=== Exercise 10: Generate a Random Date ===")
    exercise_ten()


main()
