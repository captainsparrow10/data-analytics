"""
MovieLens 1M Dataset (Section 13.2)

GroupLens Research collected one million movie ratings from six thousand users on
four thousand movies, spread across three "::"-separated tables: users (gender,
age, occupation, zip), ratings (user, movie, rating, timestamp), and movies
(title, genres). This file reproduces the book's analysis: load the three tables
with `read_table(sep="::", engine="python")`, merge them into one frame, build a
`pivot_table` of mean rating by title and gender, filter to titles with at least
250 ratings, find the top films among female viewers, and measure rating
DISAGREEMENT two ways — a male-minus-female `diff` column (most divisive by
gender) and the per-title standard deviation (most divisive overall).

The dataset is downloaded on demand into a git-ignored `datasets/` cache; every
function guards on availability so the file exits 0 offline.

WHAT THIS FILE COVERS
STEP                        TECHNIQUE
load three "::" tables      pd.read_table(sep="::", engine="python", names=...)
merge into one frame        pd.merge(pd.merge(ratings, users), movies)
mean rating by gender       DataFrame.pivot_table(index, columns, aggfunc)
filter active titles        groupby(...).size() + index Boolean mask + .loc
top films by audience       sort_values on a gender column
rating disagreement         diff column (M - F); std by title

Run:
    poetry run python cap_13_examples/2-movielens.py
"""

import os
import urllib.request

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "datasets")
RAW_BASE = "https://raw.githubusercontent.com/wesm/pydata-book/3rd-edition/datasets"


def ensure(rel_path: str, url: str) -> str | None:
    """Return a cached local path, downloading once; None (with a hint) on failure."""
    dest = os.path.join(DATA_DIR, rel_path)
    if os.path.exists(dest):
        return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        print(f"[download] fetching {rel_path} (one-time) ...")
        urllib.request.urlretrieve(url, dest)  # one-time cached download
        return dest
    except Exception as e:
        print(f"[skip] could not fetch {rel_path}: {e}")
        print(f"       download manually from {url} into {DATA_DIR}/")
        return None


def _load_merged() -> pd.DataFrame | None:
    """
    Load and merge the three MovieLens tables into a single DataFrame.

    Returns None if any of the three files cannot be downloaded so callers can
    guard and exit 0.
    """
    users_path = ensure("movielens/users.dat", f"{RAW_BASE}/movielens/users.dat")
    ratings_path = ensure("movielens/ratings.dat", f"{RAW_BASE}/movielens/ratings.dat")
    movies_path = ensure("movielens/movies.dat", f"{RAW_BASE}/movielens/movies.dat")
    if users_path is None or ratings_path is None or movies_path is None:
        return None

    # The tables use "::" as the separator; engine="python" is required for a
    # multi-character separator. Columns have no header row, so we name them.
    unames = ["user_id", "gender", "age", "occupation", "zip"]
    users = pd.read_table(
        users_path, sep="::", header=None, names=unames, engine="python"
    )
    rnames = ["user_id", "movie_id", "rating", "timestamp"]
    ratings = pd.read_table(
        ratings_path, sep="::", header=None, names=rnames, engine="python"
    )
    mnames = ["movie_id", "title", "genres"]
    movies = pd.read_table(
        movies_path, sep="::", header=None, names=mnames, engine="python"
    )

    # pandas infers the join keys from overlapping column names (user_id, movie_id).
    data = pd.merge(pd.merge(ratings, users), movies)
    return data


def explain_load_and_merge() -> None:
    """
    Problem: combine the three tables so every rating carries its user + movie info.
    Why: analyzing data spread across three tables is awkward; merging on the
    shared keys gives one wide frame where each row is a rating annotated with the
    rater's gender/age/occupation and the movie's title/genres.
    """
    print("== Loading and merging the three MovieLens tables ==")

    data = _load_merged()
    if data is None:
        print("[guard] MovieLens data not available; skipping.")
        return

    print(data.head())
    print(data.iloc[0])   # one fully merged rating record


def explain_mean_ratings_by_gender() -> None:
    """
    Problem: compute the mean rating of each film by gender, for popular films.
    Why: `pivot_table` aggregates rating with title as the row index and gender as
    columns. We then keep only titles with >= 250 ratings (a `groupby().size()`
    count turned into a Boolean index mask) so sparse films do not dominate, and
    sort by the F column to see the top films among female viewers.
    """
    print("== Mean ratings by title and gender; top films by audience ==")

    data = _load_merged()
    if data is None:
        print("[guard] MovieLens data not available; skipping.")
        return

    # Mean rating per title, split into F / M columns.
    mean_ratings = data.pivot_table(
        "rating", index="title", columns="gender", aggfunc="mean"
    )
    print(mean_ratings.head())

    # Count ratings per title and keep those with at least 250.
    ratings_by_title = data.groupby("title").size()
    # Boolean-indexing an Index is typed as Index | scalar; narrow to an Index.
    active_titles = ratings_by_title.index[ratings_by_title >= 250]
    assert isinstance(active_titles, pd.Index)
    print(active_titles[:10])

    # Restrict the mean-ratings table to the active titles.
    mean_ratings = mean_ratings.loc[active_titles]
    print(mean_ratings.head())

    # Top films among female viewers: sort by the F column, descending.
    top_female_ratings = mean_ratings.sort_values("F", ascending=False)
    print(top_female_ratings.head())


def explain_rating_disagreement() -> None:
    """
    Problem: find the films viewers disagree about most.
    Why: two complementary measures. A `diff = M - F` column ranks films by the
    GENDER gap (most preferred by women at the low end, by men at the high end).
    The per-title standard deviation of ratings ranks films by overall
    disagreement, regardless of gender. Both reuse the active-titles filter.
    """
    print("== Measuring rating disagreement ==")

    data = _load_merged()
    if data is None:
        print("[guard] MovieLens data not available; skipping.")
        return

    mean_ratings = data.pivot_table(
        "rating", index="title", columns="gender", aggfunc="mean"
    )
    ratings_by_title = data.groupby("title").size()
    # Boolean-indexing an Index is typed as Index | scalar; narrow to an Index.
    active_titles = ratings_by_title.index[ratings_by_title >= 250]
    assert isinstance(active_titles, pd.Index)
    mean_ratings = mean_ratings.loc[active_titles]

    # Gender gap: positive diff = men rated it higher; negative = women did.
    mean_ratings["diff"] = mean_ratings["M"] - mean_ratings["F"]
    sorted_by_diff = mean_ratings.sort_values("diff")
    print(sorted_by_diff.head())          # most preferred by women
    print(sorted_by_diff[::-1].head())    # reverse: most preferred by men

    # Disagreement independent of gender: standard deviation of ratings per title.
    rating_std_by_title = data.groupby("title")["rating"].std()
    rating_std_by_title = rating_std_by_title.loc[active_titles]
    print(rating_std_by_title.head())
    # The 10 most divisively rated films (highest std).
    print(rating_std_by_title.sort_values(ascending=False)[:10])


def main() -> None:
    explain_load_and_merge()
    explain_mean_ratings_by_gender()
    explain_rating_disagreement()


main()
