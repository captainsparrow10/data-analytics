"""
2012 Federal Election Commission Database (Section 13.5)

The US FEC publishes campaign contributions: the 2012 presidential cycle is a
single ~150 MB CSV (`fec/P00000001-ALL.csv`) with donor name, occupation,
employer, city/state/zip, amount, and the candidate. This file reproduces the
book's full analysis: add a `party` column via a candidate->party dict, restrict
to positive donations, clean occupations/employers with mapping dicts (using
`dict.get` as a pass-through), aggregate donations by occupation and party with
`pivot_table`, find the top donor occupations/employers for Obama and Romney,
BUCKET donation amounts with `cut`, and break donations down by state.

Because the CSV is large, `ensure` STREAMS the download and SKIPS it (printing a
hint, returning None) if it fails or would exceed a sane size cap. The analysis
is fully guarded, so the file still exits 0 when the data is skipped — which is
the expected outcome in constrained environments. When the file IS present we
read only the columns we need with explicit dtypes to keep memory reasonable.

WHAT THIS FILE COVERS
STEP                        TECHNIQUE
streaming guarded download  urlopen + chunked copy with a max-size cap
party affiliation           Series.map with a candidate->party dict
clean occupation/employer   mapping dict + dict.get pass-through via Series.map
donations by occupation     pivot_table(index, columns=party) + sum filter
top donors per candidate    groupby(cand).apply(top via nlargest)
bucket donation amounts     pd.cut into size bins, groupby + unstack, normalize
donations by state          groupby([cand, state]), unstack, normalize rows

Run:
    poetry run python cap_13_examples/5-fec-campaign.py
"""

import os
import shutil
import tempfile
import urllib.request
from pathlib import Path

import matplotlib

# HEADLESS: pick the non-interactive Agg backend BEFORE importing pyplot.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

DATA_DIR = os.path.join(os.path.dirname(__file__), "datasets")
RAW_BASE = "https://raw.githubusercontent.com/wesm/pydata-book/3rd-edition/datasets"

# The CSV is ~150 MB; cap the streaming download so we never blow up disk/memory
# in a constrained environment. Raise this if you intentionally want the file.
MAX_DOWNLOAD_BYTES = 250 * 1024 * 1024  # 250 MB headroom over the ~150 MB file

# Candidate -> party mapping (the book's dict; Gary Johnson simplified to Republican).
PARTIES = {
    "Bachmann, Michelle": "Republican",
    "Cain, Herman": "Republican",
    "Gingrich, Newt": "Republican",
    "Huntsman, Jon": "Republican",
    "Johnson, Gary Earl": "Republican",
    "McCotter, Thaddeus G": "Republican",
    "Obama, Barack": "Democrat",
    "Paul, Ron": "Republican",
    "Pawlenty, Timothy": "Republican",
    "Perry, Rick": "Republican",
    "Roemer, Charles E. 'Buddy' III": "Republican",
    "Romney, Mitt": "Republican",
    "Santorum, Rick": "Republican",
}


def ensure_streaming(rel_path: str, url: str, max_bytes: int) -> str | None:
    """
    Stream-download a large file into the cache, capped at max_bytes.

    Unlike urlretrieve, this reads the response in chunks and aborts (deleting the
    partial file) if the download exceeds the cap, so a huge file can never fill
    the disk. Returns the local path on success, or None (with a hint) on any
    failure or if the cap is exceeded.
    """
    dest = os.path.join(DATA_DIR, rel_path)
    if os.path.exists(dest):
        return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp_dest = dest + ".part"
    try:
        print(f"[download] streaming {rel_path} (one-time, large file) ...")
        with urllib.request.urlopen(url) as resp:  # noqa: S310 (trusted raw URL)
            # If the server advertises a too-large size, bail out before reading.
            length = resp.headers.get("Content-Length")
            if length is not None and int(length) > max_bytes:
                print(f"[skip] {rel_path} is {int(length)} bytes (> {max_bytes} cap).")
                print(f"       download manually from {url} into {DATA_DIR}/")
                return None
            written = 0
            with open(tmp_dest, "wb") as out:
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    written += len(chunk)
                    if written > max_bytes:
                        print(f"[skip] {rel_path} exceeded the {max_bytes}-byte cap.")
                        print(f"       download manually from {url} into {DATA_DIR}/")
                        out.close()
                        os.remove(tmp_dest)
                        return None
                    out.write(chunk)
        shutil.move(tmp_dest, dest)  # atomically promote the completed file
        return dest
    except Exception as e:
        print(f"[skip] could not fetch {rel_path}: {e}")
        print(f"       download manually from {url} into {DATA_DIR}/")
        if os.path.exists(tmp_dest):
            os.remove(tmp_dest)
        return None


def _load_fec() -> pd.DataFrame | None:
    """
    Load the FEC CSV with only the needed columns and explicit dtypes.

    Returns None if the (large) file is unavailable so every analysis guards and
    the script exits 0. Adds the `party` column and restricts to positive
    (non-refund) contributions, matching the book's preparation.
    """
    path = ensure_streaming(
        "fec/P00000001-ALL.csv",
        f"{RAW_BASE}/fec/P00000001-ALL.csv",
        MAX_DOWNLOAD_BYTES,
    )
    if path is None:
        return None

    # Read only the columns the analyses use (usecols) to keep memory reasonable
    # on this large file; low_memory=False avoids mixed-type chunk inference.
    usecols = [
        "cand_nm",
        "contbr_occupation",
        "contbr_employer",
        "contbr_st",
        "contb_receipt_amt",
    ]
    fec = pd.read_csv(path, usecols=usecols, low_memory=False)

    # party from the candidate name (the stubs type map() to take a function, so
    # we wrap the dict lookup in a lambda); keep only positive contributions.
    fec["party"] = fec["cand_nm"].map(lambda name: PARTIES.get(name))
    fec = fec[fec["contb_receipt_amt"] > 0]
    assert isinstance(fec, pd.DataFrame)
    return fec


def explain_party_and_occupation() -> None:
    """
    Problem: clean occupations/employers and aggregate donations by party.
    Why: many occupations are variants of one job, so a mapping dict normalizes a
    few of them, using `dict.get(x, x)` so unmapped values pass through unchanged.
    A `pivot_table` (index=occupation, columns=party, sum of amount) then shows
    the partisan split, filtered to occupations that gave at least $2 million.
    """
    print("== Party affiliation + donations by occupation ==")

    fec = _load_fec()
    if fec is None:
        print("[guard] FEC data not available (large file skipped); skipping.")
        return

    print(fec["party"].value_counts())
    print(fec["contbr_occupation"].value_counts()[:10])

    # Normalize a few occupation variants; unmapped values pass through via get.
    occ_mapping = {
        "INFORMATION REQUESTED PER BEST EFFORTS": "NOT PROVIDED",
        "INFORMATION REQUESTED": "NOT PROVIDED",
        "INFORMATION REQUESTED (BEST EFFORTS)": "NOT PROVIDED",
        "C.E.O.": "CEO",
    }
    fec["contbr_occupation"] = fec["contbr_occupation"].map(
        lambda x: occ_mapping.get(x, x)
    )

    # The same idea for employers.
    emp_mapping = {
        "INFORMATION REQUESTED PER BEST EFFORTS": "NOT PROVIDED",
        "INFORMATION REQUESTED": "NOT PROVIDED",
        "SELF": "SELF-EMPLOYED",
        "SELF EMPLOYED": "SELF-EMPLOYED",
    }
    fec["contbr_employer"] = fec["contbr_employer"].map(
        lambda x: emp_mapping.get(x, x)
    )

    # Total donated by occupation and party; keep occupations >= $2M overall.
    by_occupation = fec.pivot_table(
        "contb_receipt_amt", index="contbr_occupation", columns="party", aggfunc="sum"
    )
    over_2mm = by_occupation[by_occupation.sum(axis="columns") > 2_000_000]
    print(over_2mm)

    with tempfile.TemporaryDirectory() as tmp:
        over_2mm.plot(kind="barh")
        path = Path(tmp) / "donations_by_occupation.png"
        plt.savefig(path, bbox_inches="tight")
        print(f"saved donations_by_occupation.png -> exists={path.exists()}")
        plt.close("all")


def explain_top_donors_for_candidates() -> None:
    """
    Problem: top donor occupations and employers for Obama and Romney.
    Why: restrict to the two main candidates, group by candidate, and apply a
    function that sums the amount by a key column and returns its `nlargest`.
    This reuses the split-apply-combine "top-N per group" pattern on real data.
    """
    print("== Top donor occupations and employers for Obama and Romney ==")

    fec = _load_fec()
    if fec is None:
        print("[guard] FEC data not available (large file skipped); skipping.")
        return

    fec_mrbo = fec[fec["cand_nm"].isin(["Obama, Barack", "Romney, Mitt"])]
    assert isinstance(fec_mrbo, pd.DataFrame)

    def get_top_amounts(group: pd.DataFrame, key: str, n: int = 5) -> pd.Series:
        # groupby-sum is typed as a broad union; narrow to a Series for nlargest.
        totals = group.groupby(key)["contb_receipt_amt"].sum()
        assert isinstance(totals, pd.Series)
        return totals.nlargest(n)

    print(fec_mrbo.groupby("cand_nm").apply(
        get_top_amounts, "contbr_occupation", n=7, include_groups=False
    ))
    print(fec_mrbo.groupby("cand_nm").apply(
        get_top_amounts, "contbr_employer", n=10, include_groups=False
    ))


def explain_bucketing_amounts() -> None:
    """
    Problem: group donations into size buckets and compare candidates by bucket.
    Why: `pd.cut` discretizes the donation amount into order-of-magnitude bins.
    Grouping (candidate, bucket) and counting shows Obama received far more small
    donations; summing and normalizing within each bucket gives each candidate's
    share of the dollars at every donation size.
    """
    print("== Bucketing donation amounts ==")

    fec = _load_fec()
    if fec is None:
        print("[guard] FEC data not available (large file skipped); skipping.")
        return

    fec_mrbo = fec[fec["cand_nm"].isin(["Obama, Barack", "Romney, Mitt"])]
    assert isinstance(fec_mrbo, pd.DataFrame)

    bins = np.array([0, 1, 10, 100, 1000, 10000, 100_000, 1_000_000, 10_000_000])
    labels = pd.cut(fec_mrbo["contb_receipt_amt"], bins)

    # Count of donations per (candidate, bucket).
    grouped = fec_mrbo.groupby(["cand_nm", labels], observed=True)
    print(grouped.size().unstack(level=0))

    # Each candidate's share of total dollars within each bucket. (groupby-sum is
    # typed as a broad union; narrow to a Series before unstacking.)
    bucket_totals = grouped["contb_receipt_amt"].sum()
    assert isinstance(bucket_totals, pd.Series)
    bucket_sums = bucket_totals.unstack(level=0)
    normed_sums = bucket_sums.div(bucket_sums.sum(axis="columns"), axis="index")
    print(normed_sums)

    with tempfile.TemporaryDirectory() as tmp:
        # Drop the two largest bins (not individual donations), as the book does.
        normed_sums[:-2].plot(kind="barh")
        path = Path(tmp) / "donation_buckets.png"
        plt.savefig(path, bbox_inches="tight")
        print(f"saved donation_buckets.png -> exists={path.exists()}")
        plt.close("all")


def explain_donations_by_state() -> None:
    """
    Problem: break donations down by candidate and state.
    Why: grouping (candidate, state) and summing, then unstacking and filling
    gaps, gives a candidate-by-state matrix. Filtering to states with > $100k and
    dividing each row by its total yields each candidate's share of the donations
    coming from every state.
    """
    print("== Donation statistics by state ==")

    fec = _load_fec()
    if fec is None:
        print("[guard] FEC data not available (large file skipped); skipping.")
        return

    fec_mrbo = fec[fec["cand_nm"].isin(["Obama, Barack", "Romney, Mitt"])]
    assert isinstance(fec_mrbo, pd.DataFrame)

    grouped = fec_mrbo.groupby(["cand_nm", "contbr_st"])
    # groupby-sum is typed as a broad union; narrow to a Series before unstacking.
    state_totals = grouped["contb_receipt_amt"].sum()
    assert isinstance(state_totals, pd.Series)
    totals = state_totals.unstack(level=0).fillna(0)
    totals = totals[totals.sum(axis="columns") > 100_000]
    assert isinstance(totals, pd.DataFrame)
    print(totals.head(10))

    # Each row (state) normalized to each candidate's share of that state's dollars.
    percent = totals.div(totals.sum(axis="columns"), axis="index")
    print(percent.head(10))


def main() -> None:
    explain_party_and_occupation()
    explain_top_donors_for_candidates()
    explain_bucketing_amounts()
    explain_donations_by_state()


main()
