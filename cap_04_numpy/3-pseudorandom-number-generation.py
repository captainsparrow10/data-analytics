"""
Pseudorandom Number Generation (Section 4.2)

The numpy.random module supplements Python's built-in `random` module with
functions for efficiently generating whole arrays of sample values from many
kinds of probability distributions. Because it fills entire arrays at once, it is
well over an order of magnitude faster than calling Python's `random` in a loop.

These numbers are not truly random but *pseudorandom*: a configurable generator
produces them deterministically from an internal state. Create an explicit
generator with np.random.default_rng(seed=...); the seed fixes the starting
state, so the same seed always yields the same sequence — handy for reproducible
examples. The generator object is also isolated from other code using numpy.random.

SOME numpy RANDOM GENERATOR METHODS
permutation     Random permutation of a sequence, or a permuted range
shuffle         Randomly permute a sequence in place
uniform         Draw samples from a uniform distribution
integers        Draw random integers from a low-to-high range
standard_normal Draw samples from a normal distribution (mean 0, std 1)
normal          Draw samples from a normal (Gaussian) distribution
binomial        Draw samples from a binomial distribution
beta            Draw samples from a beta distribution
chisquare       Draw samples from a chi-square distribution
gamma           Draw samples from a gamma distribution

Run:
    poetry run python cap_04_numpy/3-pseudorandom-number-generation.py
"""

import numpy as np


def explain_pseudorandom() -> None:
    """
    Problem: generate arrays of random samples reproducibly.
    Why: numpy.random fills whole arrays at once; using an explicit generator
    seeded with default_rng makes the output deterministic and reproducible.
    """
    print("== Pseudorandom number generation ==")

    # A 4x4 array of samples from the standard normal distribution.
    # Seeding the generator makes this output reproducible run to run.
    rng = np.random.default_rng(seed=12345)
    samples = rng.standard_normal(size=(4, 4))
    print(samples)
    print(type(rng))  # numpy.random._generator.Generator

    # Other distributions: uniform integers, and a uniform float draw.
    print(rng.integers(0, 10, size=5))
    print(rng.uniform(size=3))


def main() -> None:
    explain_pseudorandom()


main()
