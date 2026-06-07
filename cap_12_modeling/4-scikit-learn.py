"""
Introduction to scikit-learn (Section 12.4)

scikit-learn is one of the most widely used general-purpose Python machine
learning toolkits, with a broad selection of supervised/unsupervised methods and
tools for model selection, evaluation, and persistence. This file reproduces the
book's Titanic survival example end to end: impute a column's missing values,
encode a categorical feature, build train/test design matrices with `to_numpy`,
fit a `LogisticRegression`, form predictions with `predict`, use the built-in
cross-validated estimator `LogisticRegressionCV`, and validate by hand with
`cross_val_score`.

The book reads `datasets/titanic/train.csv` and `test.csv`. To stay
self-contained and offline, we SYNTHESIZE a small Titanic-like pair of frames
with `np.random.default_rng` — the same columns the example uses (`Pclass`,
`Sex`, `Age`, `Survived`) and some injected missing `Age` values — with survival
generated from a logistic rule of the features so the classifier has real signal
to fit.

SCIKIT-LEARN ESSENTIALS
TOOL                          DESCRIPTION
Series.fillna(median)         Simple missing-value imputation (train median)
DataFrame.to_numpy            Build the X_train / X_test design matrices
LogisticRegression().fit      Fit a logistic classifier on the training data
model.predict                 Predict class labels for the test design matrix
LogisticRegressionCV(Cs=...)  Logistic regression with built-in CV over C
cross_val_score(model, X, y, cv)  Hand-rolled k-fold cross-validation scores

Run:
    poetry run python cap_12_modeling/4-scikit-learn.py
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import cross_val_score


def _titanic_like() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build small Titanic-like train/test frames (the book loads CSV files).

    Survival is drawn from a logistic rule of Pclass, Sex, and Age so the model
    has genuine signal; some Age values are set missing to exercise imputation.
    """
    rng = np.random.default_rng(seed=12345)

    def make(n: int, with_target: bool) -> pd.DataFrame:
        pclass = rng.choice([1, 2, 3], size=n, p=[0.24, 0.21, 0.55])
        sex = rng.choice(["male", "female"], size=n, p=[0.65, 0.35])
        age = np.round(rng.normal(29, 13, size=n).clip(1, 80), 1)

        # A logistic survival rule: women and higher classes survive more often.
        is_female = (sex == "female").astype(float)
        logit = -1.0 + 1.3 * (3 - pclass) + 2.5 * is_female - 0.02 * age
        prob = 1.0 / (1.0 + np.exp(-logit))

        frame = pd.DataFrame({"Pclass": pclass, "Sex": sex, "Age": age})
        if with_target:
            frame["Survived"] = (rng.uniform(size=n) < prob).astype(int)

        # Inject missing Age values, as in the real Titanic dataset.
        missing = rng.choice(n, size=n // 5, replace=False)
        frame.loc[missing, "Age"] = np.nan
        return frame

    train = make(700, with_target=True)
    test = make(300, with_target=True)  # keep the target to score predictions
    return train, test


def explain_inspect_missing() -> None:
    """
    Problem: see which columns contain missing data before modeling.
    Why: statsmodels and scikit-learn generally cannot be fed missing values, so
    the first step is to count NAs per column with `isna().sum()` and decide how
    to handle them.
    """
    print("== Inspecting missing data ==")

    train, test = _titanic_like()
    print(train.head(4))
    print(train.isna().sum())
    print(test.isna().sum())


def explain_impute_and_encode() -> None:
    """
    Problem: fill missing Age and encode Sex into a numeric feature.
    Why: a simple imputation strategy fills both frames' Age NAs with the TRAIN
    median (never the test median — that would leak test information). The string
    `Sex` column is turned into a 0/1 `IsFemale` indicator so it can enter a
    numeric design matrix.
    """
    print("== Imputation and encoding ==")

    train, test = _titanic_like()

    # Impute Age with the median of the TRAINING set in both frames.
    impute_value = train["Age"].median()
    train["Age"] = train["Age"].fillna(impute_value)
    test["Age"] = test["Age"].fillna(impute_value)

    # Encode Sex as an integer IsFemale column.
    train["IsFemale"] = (train["Sex"] == "female").astype(int)
    test["IsFemale"] = (test["Sex"] == "female").astype(int)
    print(train[["Pclass", "Sex", "IsFemale", "Age", "Survived"]].head())


def _prepare() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Impute, encode, and build the NumPy train/test matrices used by the models."""
    train, test = _titanic_like()
    impute_value = train["Age"].median()
    train["Age"] = train["Age"].fillna(impute_value)
    test["Age"] = test["Age"].fillna(impute_value)
    train["IsFemale"] = (train["Sex"] == "female").astype(int)
    test["IsFemale"] = (test["Sex"] == "female").astype(int)

    predictors = ["Pclass", "IsFemale", "Age"]
    X_train = train[predictors].to_numpy()
    X_test = test[predictors].to_numpy()
    y_train = train["Survived"].to_numpy()
    y_test = test["Survived"].to_numpy()
    return X_train, X_test, y_train, y_test


def explain_build_matrices_and_fit() -> None:
    """
    Problem: build the design matrices and fit a logistic regression.
    Why: choosing the model variables and calling `to_numpy` yields the X/y
    arrays scikit-learn expects. `LogisticRegression().fit(X_train, y_train)`
    trains the classifier; `predict` then produces class labels for the test set,
    and comparing them to the true labels gives an accuracy score.
    """
    print("== Build matrices, fit LogisticRegression, predict ==")

    X_train, X_test, y_train, y_test = _prepare()
    print(X_train[:5])
    print(y_train[:5])

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_predict = model.predict(X_test)
    print(y_predict[:10])
    # With the true test labels we can compute an accuracy percentage.
    accuracy = float((y_test == y_predict).mean())
    print(f"accuracy: {accuracy:.4f}")


def explain_cross_validation() -> None:
    """
    Problem: tune/validate the model with cross-validation instead of one split.
    Why: cross-validation simulates out-of-sample prediction to avoid overfitting.
    `LogisticRegressionCV(Cs=...)` searches over the regularization strength C
    internally, while `cross_val_score(model, X, y, cv=k)` does k-fold CV by hand,
    returning one score per fold.
    """
    print("== Cross-validation (LogisticRegressionCV and cross_val_score) ==")

    X_train, _, y_train, _ = _prepare()

    # An estimator with built-in cross-validation over the C parameter.
    # scoring='accuracy' keeps the book's accuracy-based selection.
    model_cv = LogisticRegressionCV(Cs=10, scoring="accuracy")
    # l1_ratios and use_legacy_attributes also have defaults that change in newer
    # sklearn; we opt into the upcoming behavior via set_params (which accepts
    # arbitrary parameter values), because sklearn types these constructor params
    # with sentinel-string defaults ("warn") that would otherwise reject the real
    # tuple/bool values without changing runtime behavior.
    model_cv.set_params(l1_ratios=(0.0,), use_legacy_attributes=False)
    model_cv.fit(X_train, y_train)
    print(type(model_cv).__name__, "fitted")

    # Hand-rolled k-fold cross-validation: one accuracy score per fold.
    model = LogisticRegression(C=10)
    scores = cross_val_score(model, X_train, y_train, cv=4)
    print(scores)


def main() -> None:
    explain_inspect_missing()
    explain_impute_and_encode()
    explain_build_matrices_and_fit()
    explain_cross_validation()


main()
