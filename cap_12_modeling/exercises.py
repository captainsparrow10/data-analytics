"""
Modeling Libraries: Practice Exercises

These exercises reinforce the chapter's core skill: moving data back and forth
between pandas data preparation and the two main Python modeling toolkits,
statsmodels (classical statistics) and scikit-learn (machine learning). Each
exercise builds its own SYNTHETIC dataset with a known "true" relationship using
np.random.default_rng so the models have genuine signal to recover and the
results are fully reproducible. You will turn DataFrames into model matrices,
one-hot encode categoricals, standardize features, fit OLS with both the array
and formula statsmodels APIs, split data, fit linear and logistic regressions in
scikit-learn, score them, and validate with cross-validation. Every problem is
original and self-contained — no files are read and nothing is fetched.

Run:
    poetry run python cap_12_modeling/exercises.py
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split


def exercise_01() -> None:
    """
    Exercise 1: Turn a DataFrame into a model matrix.

    Problem: build a DataFrame with three numeric predictors and one target, then
    extract the predictors-only NumPy design matrix the modeling libraries expect.

    Purpose: the contact point between pandas and a model is a NumPy array. You
    select just the predictor columns and call `to_numpy`, leaving the target out
    of the design matrix.

    Expected result: a (50, 3) float ndarray of predictors plus its column names.
    """
    rng = np.random.default_rng(seed=1)
    n = 50
    data = pd.DataFrame(
        {
            "size": rng.normal(100, 20, size=n),
            "age": rng.normal(10, 3, size=n),
            "rooms": rng.integers(1, 6, size=n).astype(float),
            "price": rng.normal(300, 50, size=n),
        }
    )

    # The target ('price') stays out of the design matrix; pick the predictors.
    predictors = ["size", "age", "rooms"]
    x_matrix = data[predictors].to_numpy()  # plain ndarray for the model

    print(f"design matrix shape: {x_matrix.shape}")
    print(f"feature names: {predictors}")
    print(x_matrix[:3])


def exercise_02() -> None:
    """
    Exercise 2: Encode a categorical column with pd.get_dummies.

    Problem: a DataFrame has a string 'city' column that a numeric model cannot
    consume. Replace it with one-hot indicator columns and join them back.

    Purpose: models need numbers, not category strings. `pd.get_dummies` expands
    a categorical into 0/1 indicator columns; pandas returns booleans by default,
    so `dtype=float` is requested to keep the design matrix numeric.

    Expected result: an all-numeric frame with one indicator column per city.
    """
    rng = np.random.default_rng(seed=2)
    n = 8
    data = pd.DataFrame(
        {
            "area": rng.normal(80, 10, size=n),
            "city": rng.choice(["lima", "cusco", "iquitos"], size=n),
        }
    )
    print(data)

    # One-hot encode 'city'; dtype=float keeps the result numeric (not boolean).
    dummies = pd.get_dummies(data["city"], prefix="city", dtype=float)
    encoded = data.drop("city", axis=1).join(dummies)

    print(encoded)
    print(f"dtypes:\n{encoded.dtypes}")


def exercise_03() -> None:
    """
    Exercise 3: Standardize (z-score) features.

    Problem: two predictors live on very different scales. Rescale each column to
    zero mean and unit standard deviation so no single feature dominates.

    Purpose: many estimators (and gradient-based solvers) behave better when
    features share a scale. Standardizing subtracts the column mean and divides by
    the column standard deviation.

    Expected result: scaled columns with mean ~0 and standard deviation ~1.
    """
    rng = np.random.default_rng(seed=3)
    n = 200
    data = pd.DataFrame(
        {
            "salary": rng.normal(50_000, 12_000, size=n),
            "years": rng.normal(8, 4, size=n),
        }
    )

    # z-score: (x - mean) / std, computed per column (ddof=0 = population std).
    means = data.mean()
    stds = data.std(ddof=0)
    scaled = (data - means) / stds

    print("before scaling (mean, std):")
    print(np.column_stack([means.to_numpy(), stds.to_numpy()]))
    print("after scaling (mean ~0, std ~1):")
    print(np.column_stack([scaled.mean().to_numpy(), scaled.std(ddof=0).to_numpy()]))


def exercise_04() -> None:
    """
    Exercise 4: Fit an OLS with statsmodels (array API) and read params.

    Problem: synthesize y from a known linear rule of two predictors plus noise,
    then recover the coefficients with the array-based OLS interface.

    Purpose: OLS needs an explicit intercept, so `sm.add_constant` prepends an
    all-ones column. `sm.OLS(y, X).fit()` returns a results object whose `params`
    should land near the true coefficients used to generate the data.

    Expected result: estimated params close to [intercept=2, b_size=1.5, b_age=-0.8].
    """
    rng = np.random.default_rng(seed=4)
    n = 300
    size = rng.normal(0, 1, size=n)
    age = rng.normal(0, 1, size=n)
    noise = rng.normal(0, 0.1, size=n)

    # The true model the data is generated from.
    y = 2.0 + 1.5 * size - 0.8 * age + noise

    x = np.column_stack([size, age])
    x_const = sm.add_constant(x)  # prepend the intercept column
    results = sm.OLS(y, x_const).fit()

    # params order: [const, x1, x2] -> should approximate [2.0, 1.5, -0.8].
    print(f"estimated params: {np.round(results.params, 3)}")
    print(f"R-squared: {results.rsquared:.4f}")


def exercise_05() -> None:
    """
    Exercise 5: Read the statsmodels summary table.

    Problem: fit an OLS and print the full diagnostic summary, then pull a couple
    of named quantities (R-squared and the t-statistics) out of the results.

    Purpose: `results.summary()` is the standard statsmodels report (coefficients,
    standard errors, t-values, confidence intervals, fit statistics). Individual
    pieces are also reachable as attributes for programmatic use.

    Expected result: a printed summary plus the R-squared and t-values.
    """
    rng = np.random.default_rng(seed=5)
    n = 150
    x1 = rng.normal(0, 1, size=n)
    x2 = rng.normal(0, 1, size=n)
    y = 1.0 + 3.0 * x1 + 0.5 * x2 + rng.normal(0, 0.5, size=n)

    x_const = sm.add_constant(np.column_stack([x1, x2]))
    results = sm.OLS(y, x_const).fit()

    print(results.summary())
    print(f"R-squared attribute: {results.rsquared:.4f}")
    print(f"t-values: {np.round(results.tvalues, 2)}")


def exercise_06() -> None:
    """
    Exercise 6: Fit OLS with the statsmodels formula API.

    Problem: fit the same kind of linear model directly from a DataFrame using a
    Patsy formula string instead of building arrays by hand.

    Purpose: `smf.ols('y ~ x1 + x2', data)` reads column names from the frame and
    adds the Intercept itself (no `add_constant` needed); `params` and `tvalues`
    come back as labeled Series carrying the feature names.

    Expected result: labeled params near Intercept=5, hours=2, reviews=0.3.
    """
    rng = np.random.default_rng(seed=6)
    n = 250
    hours = rng.normal(20, 5, size=n)
    reviews = rng.normal(50, 15, size=n)
    score = 5.0 + 2.0 * hours + 0.3 * reviews + rng.normal(0, 2, size=n)

    data = pd.DataFrame({"hours": hours, "reviews": reviews, "score": score})

    # Formula API: intercept is implicit, params are labeled by column name.
    results = smf.ols("score ~ hours + reviews", data=data).fit()

    print("params (labeled Series):")
    print(results.params.round(3))
    print("t-values:")
    print(results.tvalues.round(2))


def exercise_07() -> None:
    """
    Exercise 7: Train/test split with scikit-learn.

    Problem: split a synthetic regression dataset into training and test subsets
    so a model can be evaluated on data it never saw during fitting.

    Purpose: `train_test_split` holds out part of the data for honest evaluation.
    A fixed `random_state` makes the split reproducible; `test_size=0.25` keeps a
    quarter of the rows for testing.

    Expected result: row counts that sum back to the original n (75% / 25%).
    """
    rng = np.random.default_rng(seed=7)
    n = 400
    x = rng.normal(0, 1, size=(n, 3))
    y = x @ np.array([1.0, -2.0, 0.5]) + rng.normal(0, 0.2, size=n)

    # train_test_split is loosely typed (returns a list); narrow to ndarrays.
    splits = train_test_split(x, y, test_size=0.25, random_state=0)
    x_train, x_test, y_train, y_test = (np.asarray(part) for part in splits)

    print(f"total rows: {n}")
    print(f"train rows: {x_train.shape[0]}, test rows: {x_test.shape[0]}")
    print(f"train y mean: {y_train.mean():.3f}, test y mean: {y_test.mean():.3f}")


def exercise_08() -> None:
    """
    Exercise 8: Fit LinearRegression and report R-squared.

    Problem: train a scikit-learn LinearRegression on a held-out split and report
    the coefficient of determination (R-squared) on the test set.

    Purpose: scikit-learn's estimator API is `fit` then `score`. For a regressor,
    `score` returns R-squared on the supplied data — here the test set, the honest
    measure of generalization.

    Expected result: learned coefficients near [1.5, -3, 2] and a high test R-squared.
    """
    rng = np.random.default_rng(seed=8)
    n = 500
    x = rng.normal(0, 1, size=(n, 3))
    true_coef = np.array([1.5, -3.0, 2.0])
    y = x @ true_coef + 4.0 + rng.normal(0, 0.3, size=n)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=1
    )

    model = LinearRegression()
    model.fit(x_train, y_train)

    print(f"learned coefficients: {np.round(model.coef_, 3)}")
    print(f"learned intercept: {model.intercept_:.3f}")
    # score() on a regressor returns R-squared on the given data.
    print(f"test R-squared: {model.score(x_test, y_test):.4f}")


def exercise_09() -> None:
    """
    Exercise 9: Fit LogisticRegression on a 2-class problem and report accuracy.

    Problem: synthesize a binary target from a logistic rule of two features, then
    train a classifier and measure its accuracy on a held-out test set.

    Purpose: classification mirrors regression in scikit-learn (`fit`/`predict`).
    Features are standardized first so the default solver converges quickly without
    raising convergence warnings; accuracy is the share of correct predictions.

    Expected result: a 2-class label vector and an accuracy comfortably above 0.5.
    """
    rng = np.random.default_rng(seed=9)
    n = 600
    f1 = rng.normal(0, 1, size=n)
    f2 = rng.normal(0, 1, size=n)

    # Logistic rule: the linear combination drives the probability of class 1.
    logit = 1.0 + 2.5 * f1 - 1.5 * f2
    prob = 1.0 / (1.0 + np.exp(-logit))
    y = (rng.uniform(size=n) < prob).astype(int)

    x = np.column_stack([f1, f2])  # already on a common (standard normal) scale
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=2
    )

    # max_iter is generous so the solver fully converges under -W error.
    model = LogisticRegression(max_iter=1000)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = float(np.asarray(predictions == y_test).mean())

    print(f"first 10 predicted labels: {predictions[:10]}")
    print(f"test accuracy: {accuracy:.4f}")


def exercise_10() -> None:
    """
    Exercise 10: Validate a model with cross_val_score.

    Problem: instead of a single train/test split, estimate a classifier's
    performance with k-fold cross-validation and report the per-fold scores plus
    their mean.

    Purpose: a single split can be lucky or unlucky. `cross_val_score` rotates the
    held-out fold across the data and returns one score per fold, giving a more
    stable estimate of out-of-sample accuracy.

    Expected result: 5 fold accuracies and a mean clearly above chance (0.5).
    """
    rng = np.random.default_rng(seed=10)
    n = 800
    f1 = rng.normal(0, 1, size=n)
    f2 = rng.normal(0, 1, size=n)
    logit = 0.5 + 2.0 * f1 - 2.0 * f2
    prob = 1.0 / (1.0 + np.exp(-logit))
    y = (rng.uniform(size=n) < prob).astype(int)
    x = np.column_stack([f1, f2])

    model = LogisticRegression(max_iter=1000)
    # cv=5 -> five folds, one accuracy score each (default scoring for a classifier).
    scores = cross_val_score(model, x, y, cv=5)

    print(f"per-fold accuracies: {np.round(scores, 4)}")
    print(f"mean accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")


def main() -> None:
    print("########## DataFrame -> model matrix ##########")
    exercise_01()
    print("\n########## Encode a categorical (get_dummies) ##########")
    exercise_02()
    print("\n########## Standardize features ##########")
    exercise_03()
    print("\n########## OLS array API (sm.OLS) ##########")
    exercise_04()
    print("\n########## OLS summary / params ##########")
    exercise_05()
    print("\n########## OLS formula API (smf.ols) ##########")
    exercise_06()
    print("\n########## Train/test split ##########")
    exercise_07()
    print("\n########## LinearRegression + R-squared ##########")
    exercise_08()
    print("\n########## LogisticRegression + accuracy ##########")
    exercise_09()
    print("\n########## Cross-validation (cross_val_score) ##########")
    exercise_10()


main()
