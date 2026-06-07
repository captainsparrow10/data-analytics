"""
Universal Functions: Fast Element-Wise Array Functions (Section 4.3)

A universal function, or ufunc, performs element-wise operations on the data in
ndarrays. Think of them as fast, vectorized wrappers around simple functions that
take one or more scalar values and produce one or more scalar results.

  * Unary ufuncs   take one array         (e.g. np.sqrt, np.exp).
  * Binary ufuncs  take two arrays        (e.g. np.add, np.maximum).
  * Some ufuncs    return multiple arrays (e.g. np.modf).
  * All ufuncs accept an optional `out=` array to write results in place.

SOME UNARY UFUNCS
abs, fabs       Absolute value, element-wise
sqrt            Square root            (equivalent to arr ** 0.5)
square          Square                 (equivalent to arr ** 2)
exp             Exponent e**x
log, log10,
log2, log1p     Natural log, base 10, base 2, and log(1 + x)
sign            Sign of each element: 1 (positive), 0 (zero), -1 (negative)
ceil, floor     Round up / round down to the nearest integer
rint            Round to the nearest integer, preserving the dtype
modf            Return the fractional and integral parts as separate arrays
isnan           Boolean array: which values are NaN (Not a Number)
isfinite,
isinf           Boolean array: which values are finite / infinite
cos, sin, tan,
cosh, sinh,
tanh, arc*      Regular, hyperbolic, and inverse trigonometric functions
logical_not     Truth value of `not x`, element-wise (equivalent to ~arr)

SOME BINARY UFUNCS
add             Add corresponding elements
subtract        Subtract second array from first
multiply        Multiply array elements
divide,
floor_divide    Divide / floor-divide (truncating the remainder)
power           Raise elements in the first array to powers in the second
maximum, fmax   Element-wise maximum; fmax ignores NaN
minimum, fmin   Element-wise minimum; fmin ignores NaN
mod             Element-wise modulus (remainder of division)
copysign        Copy the sign of the second argument onto the first
greater, less,
equal, ...      Element-wise comparison, yielding a Boolean array (>, <, ==, ...)
logical_and,
logical_or,
logical_xor     Element-wise truth values of &, |, ^ logical operations

Run:
    poetry run python cap_04_numpy/4-universal-functions.py
"""

import numpy as np


def explain_unary_ufuncs() -> None:
    """
    Problem: apply a simple math function to every element of an array.
    Why: unary ufuncs are fast vectorized transformations — one call replaces an
    explicit loop over the elements.
    """
    print("== Unary ufuncs ==")

    arr = np.arange(10)
    print(arr)
    print(np.sqrt(arr))  # square root of each element
    print(np.exp(arr))   # e**x for each element


def explain_binary_ufuncs() -> None:
    """
    Problem: combine two arrays element-wise.
    Why: binary ufuncs take two arrays and return a single array; for example,
    np.maximum returns the element-wise maximum of its two inputs.
    """
    print("== Binary ufuncs ==")

    rng = np.random.default_rng(seed=12345)
    x = rng.standard_normal(8)
    y = rng.standard_normal(8)
    print(x)
    print(y)
    # Element-wise maximum: each output element is max(x[i], y[i]).
    print(np.maximum(x, y))


def explain_multiple_return_ufuncs() -> None:
    """
    Problem: split each value into its fractional and integral parts.
    Why: a few ufuncs return MULTIPLE arrays. np.modf is the vectorized version
    of Python's math.modf, returning (fractional_part, integral_part).
    """
    print("== Ufuncs that return multiple arrays ==")

    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal(7) * 5
    print(arr)
    remainder, whole_part = np.modf(arr)
    print(remainder)   # fractional parts
    print(whole_part)  # integral parts


def explain_out_argument() -> None:
    """
    Problem: write a ufunc's result into an existing array instead of a new one.
    Why: the optional `out=` argument avoids allocating a new array, which can
    matter for performance with large data.
    """
    print("== The out argument ==")

    arr = np.arange(5, dtype=np.float64)
    out = np.zeros_like(arr)
    # Without out=, np.add returns a brand-new array.
    print(np.add(arr, 1))
    # With out=, the result is written into `out` (and also returned).
    np.add(arr, 1, out=out)
    print(out)


def main() -> None:
    explain_unary_ufuncs()
    explain_binary_ufuncs()
    explain_multiple_return_ufuncs()
    explain_out_argument()


main()
