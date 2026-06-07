"""
Challenge Template — copy me to start a new challenge

A scratch space for harder, integrative problems you design yourself to test what
you learned across the book. Copy this file, rename it, and fill in each
`challenge_NN()` with a clear problem statement (in the docstring) and your own
solution below it. Keep the same shape as the rest of the repo: a module
docstring, `challenge_NN() -> None` functions, a `main()` runner, and a bare
`main()` call so the file runs end to end.

How to use:
    cp challenges/_template.py challenges/01-<topic>.py
    # 1) write the PROBLEM in each docstring
    # 2) solve it below the comment
    # 3) run it:        poetry run python challenges/01-<topic>.py
    # 4) type-check it: poetry run pyright challenges/01-<topic>.py

Run:
    poetry run python challenges/_template.py
"""

import numpy as np
import pandas as pd


def challenge_01() -> None:
    """
    Problem: <describe the challenge — what to compute or build>.
    Expected: <what the printed output should look like>.
    """
    print("== Challenge 01 ==")

    # --- your solution starts here ---
    rng = np.random.default_rng(seed=0)
    sample = pd.Series(rng.integers(0, 100, size=5))
    print(sample)  # replace with your own work
    # --- your solution ends here ---


def main() -> None:
    challenge_01()


main()
