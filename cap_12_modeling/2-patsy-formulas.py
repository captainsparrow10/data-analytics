"""
Creating Model Descriptions with Patsy (Section 12.2)

Patsy is a Python library for describing statistical models (especially linear
models) with a string-based "formula syntax" inspired by the R and S languages.
A formula like `y ~ x0 + x1` does not mean "add x0 to x1"; the `+` separates
*terms* in the design matrix. `patsy.dmatrices` takes a formula and a dataset
(DataFrame or dict of arrays) and returns the response and predictor design
matrices, which are NumPy ndarrays carrying extra metadata (`design_info`,
column names) you can pass straight into `numpy.linalg.lstsq` or statsmodels.

This file covers: building design matrices from a formula, inspecting the
DesignMatrix objects and converting them with `np.asarray`, fitting via
`np.linalg.lstsq` and reattaching coefficient names through `design_info`,
in-formula transformations (Python functions, `standardize`/`center`, applying
saved stateful transforms to new data with `build_design_matrices`, and the `I()`
escape for real arithmetic), no-intercept formulas (`+ 0`), and categorical
data in formulas (default dummy coding, `C()` to force categorical, and
interaction terms with `:`).

PATSY FORMULA ESSENTIALS
SYNTAX                DESCRIPTION
y ~ x0 + x1           response y on terms x0 and x1 (Intercept added by default)
y ~ x0 + x1 + 0       same, but suppress the Intercept (also `- 1`)
standardize(x) center(x)  built-in stateful transforms (mean 0/var 1; mean 0)
I(x0 + x1)            escape: treat + as real arithmetic, not a term separator
C(col)                force a numeric column to be coded as categorical
a:b                   interaction term between a and b

Run:
    poetry run python cap_12_modeling/2-patsy-formulas.py
"""

import numpy as np
import pandas as pd

# patsy builds its package-level `__all__` dynamically, so pyright cannot see
# `patsy.dmatrices` / `patsy.build_design_matrices`. Import them from the
# defining submodules instead (the public names are re-exported at runtime).
from patsy.build import build_design_matrices
from patsy.design_info import DesignInfo
from patsy.highlevel import dmatrices


def _design_info(matrix: object) -> DesignInfo:
    """
    Return a DesignMatrix's `.design_info` (its column/term metadata).

    DesignMatrix is an np.ndarray subclass that attaches `design_info` in
    `__new__`, which pyright cannot see statically (and `dmatrices` is untyped,
    so the matrix is a broad union); we read the attribute via getattr and narrow
    back to DesignInfo with an assert (behavior-preserving, no cast).
    """
    info = getattr(matrix, "design_info")
    assert isinstance(info, DesignInfo)
    return info


def _data() -> pd.DataFrame:
    """The book's small numeric example frame, reused across the demos."""
    return pd.DataFrame(
        {
            "x0": [1, 2, 3, 4, 5],
            "x1": [0.01, -0.01, 0.25, -4.1, 0.0],
            "y": [-1.5, 0.0, 3.6, 1.3, -2.0],
        }
    )


def explain_dmatrices_basics() -> None:
    """
    Problem: turn a formula and a DataFrame into response/predictor matrices.
    Why: `patsy.dmatrices` parses the formula, adds an Intercept column by
    convention, and returns two DesignMatrix objects. They behave as ndarrays
    (so `np.asarray` exposes the raw values) but also remember the term names.
    """
    print("== patsy.dmatrices: design matrices from a formula ==")

    response, design = dmatrices("y ~ x0 + x1", _data())
    print(response)            # DesignMatrix shape (5, 1), term 'y'
    print(design)              # DesignMatrix shape (5, 3): Intercept, x0, x1
    print(np.asarray(response))  # the underlying ndarray values
    print(np.asarray(design))    # note the leading column of 1s (the Intercept)


def explain_no_intercept_and_lstsq() -> None:
    """
    Problem: drop the Intercept, and fit the matrices with least squares.
    Why: the Intercept is a convention you can suppress by adding `+ 0` (or
    `- 1`). The Patsy matrices feed straight into `numpy.linalg.lstsq`, an OLS
    solver; the retained `design_info.column_names` let you reattach the model's
    term names to the fitted coefficients as a labeled Series.
    """
    print("== Suppressing the Intercept and fitting with np.linalg.lstsq ==")

    # `+ 0` removes the Intercept: the matrix now has just x0 and x1.
    print(dmatrices("y ~ x0 + x1 + 0", _data())[1])

    # The intercept-bearing matrices fed into an OLS solver.
    response, design = dmatrices("y ~ x0 + x1", _data())
    coef, _resid, _, _ = np.linalg.lstsq(
        np.asarray(design), np.asarray(response), rcond=None
    )
    print(coef)
    # Reattach the model column names to the fitted coefficients.
    coef = pd.Series(coef.squeeze(), index=_design_info(design).column_names)
    print(coef)


def explain_in_formula_transformations() -> None:
    """
    Problem: apply Python and built-in transforms inside the formula itself.
    Why: Patsy resolves function calls in the formula against the enclosing
    scope, so `np.log(np.abs(x1) + 1)` is computed per row. `standardize` and
    `center` are built-in *stateful* transforms (mean 0/variance 1, and mean 0):
    they remember the in-sample statistics so the same shift/scale can be
    reapplied to new data.
    """
    print("== Data transformations in Patsy formulas ==")

    # Mix Python code into the formula: Patsy finds np in the enclosing scope.
    print(dmatrices("y ~ x0 + np.log(np.abs(x1) + 1)", _data())[1])

    # Built-in stateful transforms: standardize (mean 0, var 1) and center.
    print(dmatrices("y ~ standardize(x0) + center(x1)", _data())[1])


def explain_stateful_transform_on_new_data() -> None:
    """
    Problem: transform out-of-sample data with the original sample's statistics.
    Why: when you fit on one dataset and score another, stateful transforms like
    center/standardize MUST reuse the in-sample mean/std, not recompute them.
    `patsy.build_design_matrices` replays the saved `design_info` onto new data,
    guaranteeing consistent encoding.
    """
    print("== Applying stateful transforms to new data (build_design_matrices) ==")

    _response, design = dmatrices("y ~ standardize(x0) + center(x1)", _data())

    new_data = pd.DataFrame(
        {
            "x0": [6, 7, 8, 9],
            "x1": [3.1, -0.5, 0, 2.3],
            "y": [1, 2, 3, 4],
        }
    )
    # Reuse the in-sample design_info so the transforms match the original fit.
    new_design = build_design_matrices([_design_info(design)], new_data)
    print(new_design)


def explain_I_arithmetic() -> None:
    """
    Problem: actually add two columns together as one predictor.
    Why: because `+` separates terms, real arithmetic must be wrapped in the
    special `I()` function. `I(x0 + x1)` produces a single column that is the
    elementwise sum, rather than two separate terms.
    """
    print("== The I() escape for arithmetic inside a formula ==")

    print(dmatrices("y ~ I(x0 + x1)", _data())[1])


def explain_categorical_data() -> None:
    """
    Problem: encode categorical predictors, including interactions.
    Why: nonnumeric terms in a formula become dummy variables automatically; with
    an Intercept one level is dropped to avoid collinearity, and `+ 0` brings all
    levels back. `C()` forces a numeric column to be treated as categorical, and
    `key1:key2` adds an interaction term (used, e.g., in ANOVA models).
    """
    print("== Categorical data and Patsy ==")

    data = pd.DataFrame(
        {
            "key1": ["a", "a", "b", "b", "a", "b", "a", "b"],
            "key2": [0, 1, 0, 1, 0, 1, 0, 0],
            "v1": [1, 2, 3, 4, 5, 6, 7, 8],
            "v2": [-1, 0, 2.5, -0.5, 4.0, -1.2, 0.2, -1.7],
        }
    )
    # With an Intercept, the first level of key1 is absorbed; only key1[T.b] shows.
    print(dmatrices("v2 ~ key1", data)[1])

    # Omitting the Intercept (+ 0) includes a column for every category level.
    print(dmatrices("v2 ~ key1 + 0", data)[1])

    # C() interprets a numeric column as categorical.
    print(dmatrices("v2 ~ C(key2)", data)[1])

    # Map key2 to strings, then build a model with an interaction term key1:key2.
    # (map's typed signature expects a callable; a lambda over the dict keeps the
    # mapping while satisfying the type checker.)
    labels = {0: "zero", 1: "one"}
    data["key2"] = data["key2"].map(lambda code: labels[code])
    print(dmatrices("v2 ~ key1 + key2", data)[1])
    print(dmatrices("v2 ~ key1 + key2 + key1:key2", data)[1])


def main() -> None:
    explain_dmatrices_basics()
    explain_no_intercept_and_lstsq()
    explain_in_formula_transformations()
    explain_stateful_transform_on_new_data()
    explain_I_arithmetic()
    explain_categorical_data()


main()
