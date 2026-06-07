"""
Introduction to statsmodels (Section 12.3)

statsmodels is a Python library for fitting many kinds of "classical"
frequentist statistical models, running statistical tests, and exploring data.
This file uses two of its most common tools: estimating linear models (ordinary
least squares) through both the array-based API (`statsmodels.api as sm`) and the
formula-based API (`statsmodels.formula.api as smf`), and estimating a time
series autoregressive process.

For the linear model we synthesize data from a known "true" model so the fitted
coefficients can be compared against the parameters that generated them. We add
an intercept with `sm.add_constant`, fit with `sm.OLS(...).fit()`, and read off
`params`, `tvalues`, and the full `summary()`; then we reproduce the same fit
with `smf.ols` and a Patsy formula over a DataFrame (no manual intercept needed).
For the time series we simulate an AR(2) series and recover its parameters with
`AutoReg` (the modern replacement for the book's older `sm.tsa.AR`).

STATSMODELS ESSENTIALS
TOOL                          DESCRIPTION
sm.add_constant               Prepend an intercept (all-ones) column to a matrix
sm.OLS(y, X).fit()            Fit an ordinary least squares model -> results obj
results.params / .tvalues     Estimated coefficients and their t-statistics
results.summary()             Full diagnostic table for the fitted model
smf.ols('y ~ ...', data)      Formula API: fit OLS from a DataFrame + Patsy string
AutoReg(values, lags).fit()   Fit an autoregressive time series model

Run:
    poetry run python cap_12_modeling/3-statsmodels.py
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tsa.ar_model import AutoReg

# One generator shared by the helpers so the synthetic data is reproducible.
rng = np.random.default_rng(seed=12345)


def dnorm(mean: float, variance: float, size: int = 1) -> np.ndarray:
    """Generate normally distributed data with a given mean and variance."""
    return mean + np.sqrt(variance) * rng.standard_normal(size)


def explain_linear_model_array_api() -> None:
    """
    Problem: fit an OLS regression with the array-based statsmodels interface.
    Why: real models start from arrays. We build X from three predictors, write
    down a "true" coefficient vector `beta`, and form y with added noise. Because
    OLS needs an explicit intercept, `sm.add_constant` prepends a column of ones;
    `sm.OLS(y, X).fit()` then returns a results object exposing `params` and the
    full `summary()` diagnostic table.
    """
    print("== Estimating a linear model (array API: sm.OLS) ==")

    N = 100
    X = np.c_[
        dnorm(0, 0.4, size=N),
        dnorm(0, 0.6, size=N),
        dnorm(0, 0.2, size=N),
    ]
    eps = dnorm(0, 0.1, size=N)
    beta = [0.1, 0.3, 0.5]            # the "true" model parameters
    y = np.dot(X, beta) + eps
    print(X[:5])
    print(y[:5])

    # add_constant prepends an intercept (all-ones) column to the design matrix.
    X_model = sm.add_constant(X)
    print(X_model[:5])

    model = sm.OLS(y, X)             # fit without an explicit intercept here
    results = model.fit()
    print(results.params)           # estimated coefficients (~ beta)
    print(results.summary())        # full diagnostic output


def explain_linear_model_formula_api() -> None:
    """
    Problem: fit the same model from a DataFrame using formula syntax.
    Why: with named columns it is cleaner to use the formula API. `smf.ols`
    accepts a Patsy formula string and a DataFrame, adds the Intercept itself
    (no `add_constant` needed), and returns results as labeled Series — `params`
    and `tvalues` carry the column names. `predict` scores new/observed rows.
    """
    print("== Estimating a linear model (formula API: smf.ols) ==")

    N = 100
    X = np.c_[
        dnorm(0, 0.4, size=N),
        dnorm(0, 0.6, size=N),
        dnorm(0, 0.2, size=N),
    ]
    eps = dnorm(0, 0.1, size=N)
    beta = [0.1, 0.3, 0.5]
    y = np.dot(X, beta) + eps

    data = pd.DataFrame(X, columns=["col0", "col1", "col2"])
    data["y"] = y
    print(data[:5])

    results = smf.ols("y ~ col0 + col1 + col2", data=data).fit()
    print(results.params)           # Series indexed by Intercept, col0, col1, col2
    print(results.tvalues)          # t-statistics with the same labels

    # Predicted values for (here, the first five) rows of data.
    print(results.predict(data[:5]))


def explain_time_series_ar() -> None:
    """
    Problem: recover the parameters of an autoregressive time series.
    Why: statsmodels also fits time series processes. We simulate an AR(2) series
    (each value depends on its two predecessors with coefficients 0.8 and -0.4
    plus noise). Not knowing the true lag count, we fit with a larger MAXLAGS;
    `AutoReg(values, lags).fit().params` returns the intercept first, then the
    per-lag estimates. (The book used `sm.tsa.AR`, removed from statsmodels;
    `AutoReg` is the modern equivalent.)
    """
    print("== Estimating a time series process (AutoReg) ==")

    init_x = 4
    values = [init_x, init_x]
    N = 1000
    b0 = 0.8
    b1 = -0.4
    noise = dnorm(0, 0.1, N)
    for i in range(N):
        new_x = values[-1] * b0 + values[-2] * b1 + noise[i]
        values.append(new_x)

    # Fit an AR model with more lags than the true process has.
    MAXLAGS = 5
    model = AutoReg(values, MAXLAGS)
    results = model.fit()
    # Intercept first, then the estimates for each lag.
    print(results.params)


def main() -> None:
    explain_linear_model_array_api()
    explain_linear_model_formula_api()
    explain_time_series_ar()


main()
