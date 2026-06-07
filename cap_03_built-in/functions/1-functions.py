"""
Functions: A Complete Guide to Reusable, Callable Blocks in Python

A function is a named, reusable block of code that optionally takes inputs
(parameters) and optionally returns a value. Functions are first-class objects in
Python: they can be assigned to variables, passed as arguments, and returned from
other functions. This file contains 18 exercises covering function fundamentals and
common idioms.

=== FUNCTION CONCEPTS ===

1. DEFINITION (def name(params): ...)
   Description: Declare a function; call it with name(args)
   Example: def greet(): print("hi")

2. PARAMETERS & ARGUMENTS (positional, keyword, default)
   Description: Inputs declared in the signature; passed by position or by name
   Example: def f(a, b=2): ... ; f(1) ; f(a=1, b=3)

3. *args (variadic positional)
   Description: Collect any number of positional arguments into a tuple
   Example: def f(*nums): ... ; f(1, 2, 3)

4. **kwargs (variadic keyword)
   Description: Collect any number of keyword arguments into a dict
   Example: def f(**opts): ... ; f(x=1, y=2)

5. RETURN (single or multiple values)
   Description: Hand a result back; returning several values builds a tuple
   Example: return a + b, a - b

6. SCOPE (local, global, nonlocal)
   Description: Where a name is visible; `global`/`nonlocal` rebind outer names
   Example: global counter

7. NESTED / INNER FUNCTIONS
   Description: A function defined inside another, capturing the enclosing scope
   Example: def outer(): def inner(): ...

8. RECURSION
   Description: A function that calls itself, with a base case to stop
   Example: def fact(n): return 1 if n == 0 else n * fact(n - 1)

9. FIRST-CLASS / HIGHER-ORDER FUNCTIONS
   Description: Functions stored in variables, passed around, or returned
   Example: g = greet ; apply(func, x)

10. LAMBDA (anonymous functions)
    Description: A small inline function; one expression, no name required
    Example: (lambda x: x * 2)(5) = 10

11. FUNCTIONAL TOOLS (map, filter, sorted with key=)
    Description: Apply a function across an iterable declaratively
    Example: list(map(lambda x: x + 1, [1, 2])) = [2, 3]

Run:
    poetry run python cap_03_built-in/functions/1-functions.py
"""

from typing import Any, Callable

# Module-level global used by Exercise 12 to demonstrate the `global` keyword.
global_var: int = 10


def exercise_one() -> None:
    """
    Exercise 1: Create a Function with Parameters

    Problem: Write demo(name, age) that prints both values.

    Purpose: This exercise introduces the most basic function: a named block that
    receives parameters and acts on them. Parameters are annotated so the function
    is fully typed under strict checking.

    Given Input: name = "Kelly", age = 25
    Expected Output: Kelly 25
    """
    def demo(name: str, age: int) -> None:
        print(name, age)

    demo("Kelly", 25)


def exercise_two() -> None:
    """
    Exercise 2: Variable Length of Arguments (*args)

    Problem: Write func1() that accepts any number of arguments and prints them all.

    Purpose: This exercise shows *args, which packs all extra positional arguments
    into a tuple so the function works with any arity.

    Given Input: func1(20, 40, 60) then func1(80, 100)
    Expected Output: each group's header followed by its values
    """
    def func1(*args: int) -> None:
        print("Printing values:")
        for value in args:
            print(value)

    func1(20, 40, 60)
    func1(80, 100)


def exercise_three() -> None:
    """
    Exercise 3: Return Multiple Values from a Function

    Problem: Write calculation(a, b) that returns both a + b and a - b in one return.

    Purpose: This exercise shows that returning several comma-separated values builds
    a tuple, which the caller can unpack into separate variables.

    Given Input: a = 40, b = 10
    Expected Output: 50, 30
    """
    def calculation(a: int, b: int) -> tuple[int, int]:
        return a + b, a - b

    addition, subtraction = calculation(40, 10)
    print(f"{addition}, {subtraction}")


def exercise_four() -> None:
    """
    Exercise 4: Function with Default Argument

    Problem: Write show_employee(name, salary) defaulting salary to 9000 when omitted.

    Purpose: This exercise shows default parameter values, which make an argument
    optional at the call site.

    Given Input: ("Ben", 12000) and ("Jessa") with salary omitted
    Expected Output: Name: Ben salary: 12000 / Name: Jessa salary: 9000
    """
    def show_employee(name: str, salary: int = 9000) -> None:
        print(f"Name: {name} salary: {salary}")

    show_employee("Ben", 12000)
    show_employee("Jessa")


def exercise_five() -> None:
    """
    Exercise 5: Create an Inner Function

    Problem: outer(a, b) defines an inner function that adds a and b; outer adds 5
    to that sum and returns the result.

    Purpose: This exercise introduces nested functions and closures: the inner
    function "sees" a and b from the enclosing scope without them being passed in.

    Given Input: a = 5, b = 10
    Expected Output: 20
    """
    def outer(a: int, b: int) -> int:
        def inner() -> int:
            return a + b  # captures a and b from the enclosing scope

        return inner() + 5

    print(outer(5, 10))


def exercise_six() -> None:
    """
    Exercise 6: Create a Recursive Function

    Problem: Write a recursive addition() that sums the numbers from 0 to n.

    Purpose: This exercise introduces recursion: a base case (n == 0) stops the
    descent, and each call reduces the problem toward it.

    Given Input: num = 10
    Expected Output: 55
    """
    def addition(n: int) -> int:
        if n == 0:
            return 0
        return n + addition(n - 1)

    print(addition(10))


def exercise_seven() -> None:
    """
    Exercise 7: Assign a Different Name to Function and Call It

    Problem: Bind display_student to a new name and call it through that name.

    Purpose: This exercise demonstrates that functions are first-class objects:
    assigning one to a new variable does not call it, it just creates another
    reference to the same function.

    Given Input: display_student("Emma", 26) via the alias show_student
    Expected Output: Emma 26
    """
    def display_student(name: str, age: int) -> None:
        print(name, age)

    show_student = display_student  # alias, not a call
    show_student("Emma", 26)


def exercise_eight() -> None:
    """
    Exercise 8: Generate a List of Even Numbers (Range Function)

    Problem: Return a list of all even numbers between 4 and 30.

    Purpose: This exercise uses range(start, stop, step) with a step of 2 to produce
    evens directly, without filtering.

    Given Input: implicit range 4..30
    Expected Output: [4, 6, 8, ..., 28]
    """
    def even_numbers() -> list[int]:
        return list(range(4, 30, 2))

    print(even_numbers())


def exercise_nine() -> None:
    """
    Exercise 9: Find the Largest Item in a List

    Problem: Return the largest item without using the built-in max().

    Purpose: This exercise implements a linear scan, tracking the running maximum,
    to reveal what max() does under the hood.

    Given Input: x = [4, 6, 8, 24, 12, 2]
    Expected Output: 24
    """
    def find_largest(numbers: list[int]) -> int:
        largest = numbers[0]
        for value in numbers[1:]:
            if value > largest:
                largest = value
        return largest

    print(find_largest([4, 6, 8, 24, 12, 2]))


def exercise_ten() -> None:
    """
    Exercise 10: Call Function using Positional and Keyword Arguments

    Problem: Define describe_pet(animal_type, pet_name) and call it both positionally
    and with keyword arguments.

    Purpose: This exercise contrasts positional calls (order matters) with keyword
    calls (order is irrelevant, names bind explicitly).

    Given Input: ("hamster", "Harry") positional and (animal_type="dog", pet_name="Willie")
    Expected Output: a two-line description per pet, separated by a blank line
    """
    def describe_pet(animal_type: str, pet_name: str) -> None:
        print(f"I have a {animal_type}.")
        print(f"My {animal_type}'s name is {pet_name}.\n")

    describe_pet("hamster", "Harry")            # positional
    describe_pet(animal_type="dog", pet_name="Willie")  # keyword


def exercise_eleven() -> None:
    """
    Exercise 11: Create a Function with Keyword Arguments

    Problem: Write print_info(**kwargs) that prints every key-value pair.

    Purpose: This exercise shows **kwargs, which packs arbitrary keyword arguments
    into a dict. The values can be anything, so they are typed Any.

    Given Input: print_info(name="Alice", age=30, city="New York")
    Expected Output: one "key: value" line per argument
    """
    def print_info(**kwargs: Any) -> None:
        for key, value in kwargs.items():
            print(f"{key}: {value}")

    print_info(name="Alice", age=30, city="New York")


def exercise_twelve() -> None:
    """
    Exercise 12: Modifying Global Variables

    Problem: Change the module-level global_var from 10 to 20 inside a function.

    Purpose: This exercise shows the `global` keyword. Without it, assigning to
    global_var inside the function would create a NEW local variable instead of
    rebinding the module-level one.

    Given Input: global_var = 10
    Expected Output: Initial: 10 / Modified: 20
    """
    def modify_global() -> None:
        global global_var
        global_var = 20

    print(f"Initial: {global_var}")
    modify_global()
    print(f"Modified: {global_var}")


def exercise_thirteen() -> None:
    """
    Exercise 13: Recursive Factorial (Non-Negative Integers)

    Problem: Compute the factorial of a non-negative integer recursively.

    Purpose: This exercise reinforces recursion with the classic factorial: the base
    case is 0! == 1, and each step multiplies n by (n-1)!.

    Given Input: number = 5
    Expected Output: The factorial of 5 is 120
    """
    def factorial(n: int) -> int:
        if n == 0:
            return 1
        return n * factorial(n - 1)

    number = 5
    print(f"The factorial of {number} is {factorial(number)}")


def exercise_fourteen() -> None:
    """
    Exercise 14: Create a Lambda Function to Square a Number

    Problem: Use lambda to create an anonymous function that squares its input.

    Purpose: This exercise shows a lambda used inline and called immediately. Its
    parameter type is inferred from the argument, so it stays type-clean without an
    intermediate named variable (which also avoids the E731 lint).

    Given Input: number = 5
    Expected Output: 25
    """
    number = 5
    print((lambda x: x**2)(number))


def exercise_fifteen() -> None:
    """
    Exercise 15: Filter a List Using Lambda and filter()

    Problem: Use filter() with a lambda to keep only the even numbers.

    Purpose: This exercise shows filter(predicate, iterable), which yields the items
    for which the predicate returns True. The lambda's parameter type is inferred
    from the list's element type.

    Given Input: numbers = [1..10]
    Expected Output: [2, 4, 6, 8, 10]
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(list(filter(lambda x: x % 2 == 0, numbers)))


def exercise_sixteen() -> None:
    """
    Exercise 16: Transform a List Using Lambda and map()

    Problem: Use map() with a lambda to double every element.

    Purpose: This exercise shows map(func, iterable), which applies func to each item
    and yields the transformed values.

    Given Input: numbers = [1, 2, 3, 4, 5]
    Expected Output: [2, 4, 6, 8, 10]
    """
    numbers = [1, 2, 3, 4, 5]
    print(list(map(lambda x: x * 2, numbers)))


def exercise_seventeen() -> None:
    """
    Exercise 17: Sort Complex Data with sorted() and Lambda

    Problem: Sort a list of (name, grade) tuples by grade ascending.

    Purpose: This exercise shows sorted(..., key=...), where the lambda selects which
    field drives the ordering (here the grade at index 1).

    Given Input: students = [("Alice", 88), ("Bob", 75), ("Charlie", 92)]
    Expected Output: [('Bob', 75), ('Alice', 88), ('Charlie', 92)]
    """
    students = [("Alice", 88), ("Bob", 75), ("Charlie", 92)]
    print(sorted(students, key=lambda student: student[1]))


def exercise_eighteen() -> None:
    """
    Exercise 18: Create a Higher-Order Function

    Problem: Write apply_operation(func, x, y) that returns func(x, y); demonstrate
    it with addition and multiplication.

    Purpose: This exercise shows a higher-order function: one that takes another
    function as an argument. The func parameter is typed Callable[[int, int], int]
    so callers and pyright both know its shape.

    Given Input: add and multiply applied to 5 and 3
    Expected Output: Addition Result: 8 / Multiplication Result: 15
    """
    def add(a: int, b: int) -> int:
        return a + b

    def multiply(a: int, b: int) -> int:
        return a * b

    def apply_operation(func: Callable[[int, int], int], x: int, y: int) -> int:
        return func(x, y)

    print(f"Addition Result: {apply_operation(add, 5, 3)}")
    print(f"Multiplication Result: {apply_operation(multiply, 5, 3)}")


def main() -> None:
    print("=== Exercise 1: Create a Function with Parameters ===")
    exercise_one()

    print("\n=== Exercise 2: Variable Length of Arguments (*args) ===")
    exercise_two()

    print("\n=== Exercise 3: Return Multiple Values from a Function ===")
    exercise_three()

    print("\n=== Exercise 4: Function with Default Argument ===")
    exercise_four()

    print("\n=== Exercise 5: Create an Inner Function ===")
    exercise_five()

    print("\n=== Exercise 6: Create a Recursive Function ===")
    exercise_six()

    print("\n=== Exercise 7: Assign a Different Name to Function and Call It ===")
    exercise_seven()

    print("\n=== Exercise 8: Generate a List of Even Numbers (Range Function) ===")
    exercise_eight()

    print("\n=== Exercise 9: Find the Largest Item in a List ===")
    exercise_nine()

    print("\n=== Exercise 10: Call Function using Positional and Keyword Arguments ===")
    exercise_ten()

    print("\n=== Exercise 11: Create a Function with Keyword Arguments ===")
    exercise_eleven()

    print("\n=== Exercise 12: Modifying Global Variables ===")
    exercise_twelve()

    print("\n=== Exercise 13: Recursive Factorial (Non-Negative Integers) ===")
    exercise_thirteen()

    print("\n=== Exercise 14: Create a Lambda Function to Square a Number ===")
    exercise_fourteen()

    print("\n=== Exercise 15: Filter a List Using Lambda and filter() ===")
    exercise_fifteen()

    print("\n=== Exercise 16: Transform a List Using Lambda and map() ===")
    exercise_sixteen()

    print("\n=== Exercise 17: Sort Complex Data with sorted() and Lambda ===")
    exercise_seventeen()

    print("\n=== Exercise 18: Create a Higher-Order Function ===")
    exercise_eighteen()


main()
