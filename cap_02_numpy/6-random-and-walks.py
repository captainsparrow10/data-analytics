"""
Pseudorandom Number Generation & Random Walks (Sections 4.2 and 4.7)

The numpy.random module supplements Python's built-in `random` module with
functions for efficiently generating whole arrays of sample values from many
kinds of probability distributions. Because it fills entire arrays at once, it is
well over an order of magnitude faster than calling Python's `random` in a loop.

These numbers are not truly random but *pseudorandom*: a configurable generator
produces them deterministically from an internal state. Create an explicit
generator with np.random.default_rng(seed=...); the seed fixes the starting
state, so the same seed always yields the same sequence — handy for reproducible
examples. The generator is also isolated from other code using numpy.random.

The random walk is a classic application of these array operations: a path that
starts at 0 and takes +1 / -1 steps with equal probability. Expressed with
arrays, an entire walk (or thousands of walks) is computed without Python loops.

SOME numpy RANDOM GENERATOR METHODS
permutation     Random permutation of a sequence, or a permuted range
shuffle         Randomly permute a sequence in place
uniform         Draw samples from a uniform distribution
integers        Draw random integers from a low-to-high range
standard_normal Draw samples from a normal distribution (mean 0, std 1)
normal          Draw samples from a normal (Gaussian) distribution
binomial        Draw samples from a binomial distribution
beta            Draw samples from a beta distribution

Run:
    python3 cap_02_numpy/6-random-and-walks.py
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


def explain_single_random_walk() -> None:
    """
    Problem: simulate one random walk of 1,000 +1/-1 steps.
    Why: a walk is just the cumulative sum of its steps, so np.where turns coin
    flips (0/1) into steps (-1/+1) and cumsum builds the path — no Python loop.
    """
    print("== A single random walk ==")

    nsteps = 1000
    rng = np.random.default_rng(seed=12345)
    draws = rng.integers(0, 2, size=nsteps)      # 0 or 1
    steps = np.where(draws == 0, 1, -1)          # map to +1 or -1
    walk = steps.cumsum()                        # the walk is the running total

    # Simple statistics over the trajectory.
    print(walk.min())
    print(walk.max())

    # First crossing time: the first step index where |walk| reaches 10.
    # argmax returns the index of the first True in the Boolean array.
    print((np.abs(walk) >= 10).argmax())


def explain_many_random_walks() -> None:
    """
    Problem: simulate many random walks (e.g., 5,000) at once.
    Why: passing a 2-tuple size generates a 2D array of draws; computing the
    cumulative sum along axis 1 yields every walk in a single vectorized shot.
    """
    print("== Simulating many random walks at once ==")

    nwalks = 5000
    nsteps = 1000
    rng = np.random.default_rng(seed=12345)
    draws = rng.integers(0, 2, size=(nwalks, nsteps))  # one row per walk
    steps = np.where(draws > 0, 1, -1)
    walks = steps.cumsum(axis=1)                        # cumulative sum per row
    print(walks.max())
    print(walks.min())

    # Minimum crossing time to +/-30, but only for walks that actually reach it.
    hits30 = (np.abs(walks) >= 30).any(axis=1)
    print(hits30.sum())  # number of walks that hit 30 or -30
    crossing_times = (np.abs(walks[hits30]) >= 30).argmax(axis=1)
    print(crossing_times.mean())  # average minimum crossing time


def main() -> None:
    explain_pseudorandom()
    explain_single_random_walk()
    explain_many_random_walks()


main()
