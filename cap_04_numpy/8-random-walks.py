"""
Example: Random Walks (Section 4.7)

The random walk is a classic application of array operations: a path that starts
at 0 and takes +1 / -1 steps with equal probability. Expressed with arrays, an
entire walk — or thousands of walks at once — is computed without Python loops.

The key insight: a walk is just the cumulative sum of its steps. So we draw coin
flips (0/1) with the numpy.random generator (see Section 4.2), turn them into
steps (-1/+1) with np.where, and accumulate them with cumsum.

Run:
    python3 cap_04_numpy/8-random-walks.py
"""

import numpy as np


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
    explain_single_random_walk()
    explain_many_random_walks()


main()
