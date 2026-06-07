"""
Plotting with pandas and seaborn (Section 9.2)

matplotlib is a low-level tool: you assemble a plot from its base components. pandas
ships higher-level `plot` methods on `Series`/`DataFrame` that turn labeled data into
visuals with one call, and seaborn adds a statistical-graphics layer on top of
matplotlib that handles aggregation, confidence intervals, and faceting. This file
covers all of section 9.2: line plots (`Series.plot`/`DataFrame.plot`), bar plots
(`plot.bar`/`barh`, stacked, and `seaborn.barplot`), histograms and density plots
(`plot.hist`/`plot.density`, `seaborn.histplot`), scatter/point plots
(`seaborn.regplot`, `seaborn.pairplot`), and facet grids / categorical data
(`seaborn.catplot`).

This is a headless study file: the "Agg" backend is selected before importing pyplot,
so nothing is shown and no display is needed. Every figure is written into a
`tempfile.TemporaryDirectory()` with a printed confirmation, and `plt.close("all")`
runs between examples so figures do not accumulate. The book's `tips.csv` /
`macrodata.csv` are replaced by small inline synthetic equivalents (no network), so
the file is fully self-contained and leaves nothing in the repo.

KEY ENTRY POINTS IN THIS FILE
METHOD / FUNCTION       DESCRIPTION
Series.plot / DataFrame.plot  Default line plot; index drives the x-axis
plot.bar / plot.barh    Vertical / horizontal bar plots (stacked=True to stack)
seaborn.barplot         Aggregating bar plot with confidence-interval error bars
plot.hist / plot.density  Histogram / kernel-density (KDE) estimate
seaborn.histplot        Histogram + optional density in one call
seaborn.regplot         Scatter plot with a fitted linear-regression line
seaborn.pairplot        Scatter-plot matrix (pairs plot) with diagonal densities
seaborn.catplot         Faceted categorical plots (kind="bar"/"box", row/col/hue)

Run:
    poetry run python cap_09_plotting/2-pandas-seaborn.py
"""

import os
import tempfile
from pathlib import Path

import matplotlib

# HEADLESS: select the non-interactive Agg backend BEFORE importing pyplot.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

# One reproducible generator for the whole file (modern replacement for np.random.*).
rng = np.random.default_rng(seed=12345)


def _save(name: str, tmp: str) -> None:
    """Save the CURRENT pyplot figure into the temp dir, confirm, and close it."""
    path = Path(tmp) / name
    plt.savefig(path)  # pandas/seaborn draw onto the active pyplot figure
    print(f"saved {os.path.basename(path)} -> exists={os.path.exists(path)}")
    plt.close("all")


def _make_tips() -> pd.DataFrame:
    """
    Build a tiny tips-like DataFrame (stand-in for the book's examples/tips.csv).

    Columns match the book (total_bill, tip, smoker, day, time, size) so the
    seaborn bar/scatter/catplot examples read exactly like the originals. Values
    are synthetic but plausible, generated reproducibly.
    """
    n = 200
    day = rng.choice(["Thur", "Fri", "Sat", "Sun"], size=n)
    time = np.where(np.isin(day, ["Thur", "Fri"]), "Lunch", "Dinner")
    # Lunch parties skew smaller; weekend dinners skew larger.
    size = rng.integers(2, 6, size=n)
    total_bill = np.round(10 + size * 4 + rng.standard_normal(n) * 5, 2)
    total_bill = np.clip(total_bill, 5.0, None)
    tip = np.round(total_bill * rng.uniform(0.1, 0.25, size=n), 2)
    smoker = rng.choice(["No", "Yes"], size=n)
    return pd.DataFrame(
        {
            "total_bill": total_bill,
            "tip": tip,
            "smoker": smoker,
            "day": day,
            "time": time,
            "size": size,
        }
    )


def explain_line_plots() -> None:
    """
    Problem: make a line plot straight from a Series or DataFrame.
    Why: both have a `plot` attribute that defaults to a line plot; the object's
    INDEX is passed to matplotlib as the x-axis (disable with `use_index=False`).
    For a DataFrame, each column becomes its own line on the same subplot and the
    column names form an automatic legend.
    """
    print("== Line plots (Series.plot / DataFrame.plot) ==")

    with tempfile.TemporaryDirectory() as tmp:
        # Series: a random walk indexed 0,10,...,90 -> index drives the x-axis.
        s = pd.Series(rng.standard_normal(10).cumsum(), index=np.arange(0, 100, 10))
        s.plot()
        _save("series_line.png", tmp)

        # DataFrame: four cumulative-sum columns plotted as four lines + legend.
        df = pd.DataFrame(
            rng.standard_normal((10, 4)).cumsum(0),
            columns=["A", "B", "C", "D"],
            index=np.arange(0, 100, 10),
        )
        # grayscale style is friendlier for black-and-white print, as in the book.
        plt.style.use("grayscale")
        df.plot()  # equivalent to df.plot.line()
        _save("dataframe_line.png", tmp)
        plt.style.use("default")  # restore so later examples are unaffected


def explain_bar_plots() -> None:
    """
    Problem: draw vertical/horizontal, grouped, and stacked bar plots.
    Why: `plot.bar()`/`plot.barh()` use the index as the category axis. With a
    DataFrame the columns are grouped side by side per row; `stacked=True` stacks
    them instead. The DataFrame's `columns.name` titles the legend automatically.
    """
    print("== Bar plots (plot.bar / plot.barh, grouped, stacked) ==")

    with tempfile.TemporaryDirectory() as tmp:
        # Series bar + barh on a shared 2x1 figure.
        _, axes = plt.subplots(2, 1)
        data = pd.Series(rng.uniform(size=16), index=list("abcdefghijklmnop"))
        data.plot.bar(ax=axes[0], color="black", alpha=0.7)
        data.plot.barh(ax=axes[1], color="black", alpha=0.7)
        _save("series_bars.png", tmp)

        # DataFrame grouped bars: each row -> a cluster of bars (one per column).
        df = pd.DataFrame(
            rng.uniform(size=(6, 4)),
            index=["one", "two", "three", "four", "five", "six"],
            columns=pd.Index(["A", "B", "C", "D"], name="Genus"),
        )
        df.plot.bar()  # legend titled "Genus" from columns.name
        _save("dataframe_bars.png", tmp)

        # Stacked horizontal bars: row values stacked end to end.
        df.plot.barh(stacked=True, alpha=0.5)
        _save("dataframe_stacked.png", tmp)


def explain_stacked_proportions_and_seaborn_bar() -> None:
    """
    Problem: visualize per-day party-size proportions, then aggregate with seaborn.
    Why: `pd.crosstab` builds a frequency table (day x size); dividing each row by
    its sum normalizes to proportions, which `plot.bar(stacked=True)` shows as
    100%-stacked bars. seaborn's `barplot` goes further — given the raw DataFrame
    it AGGREGATES (mean per category) and draws 95% confidence-interval error bars,
    with `hue=` splitting by a second categorical variable.
    """
    print("== Stacked proportions (crosstab) + seaborn.barplot ==")

    with tempfile.TemporaryDirectory() as tmp:
        tips = _make_tips()

        # Frequency table of party size by day, reindexed in weekday order.
        party_counts = pd.crosstab(tips["day"], tips["size"])
        party_counts = party_counts.reindex(index=["Thur", "Fri", "Sat", "Sun"])
        # Keep only the common 2-5 person parties.
        party_counts = party_counts.loc[:, 2:5]
        # Normalize each row to sum to 1 -> fraction of parties of each size per day.
        party_pcts = party_counts.div(party_counts.sum(axis="columns"), axis="index")
        party_pcts.plot.bar(stacked=True)
        _save("party_pcts.png", tmp)

        # Tipping percentage; seaborn aggregates the mean per day with error bars.
        tips["tip_pct"] = tips["tip"] / (tips["total_bill"] - tips["tip"])
        # seaborn 0.13 keyword API: x=/y=/data=.
        sns.barplot(x="tip_pct", y="day", data=tips, orient="h")
        _save("sns_barplot.png", tmp)

        # hue splits each bar by a second categorical value (time of day).
        sns.set_style("whitegrid")  # switch plot theme
        sns.barplot(x="tip_pct", y="day", hue="time", data=tips, orient="h")
        _save("sns_barplot_hue.png", tmp)
        sns.set_style("white")  # restore a neutral theme for later examples


def explain_histograms_and_density() -> None:
    """
    Problem: show a value-frequency distribution and a smooth density estimate.
    Why: `plot.hist(bins=...)` buckets values into bins and plots their counts;
    `plot.density()` draws a kernel-density estimate (KDE) — a smooth mixture-of-
    normals approximation of the underlying distribution (needs SciPy). seaborn's
    `histplot` combines a histogram with an optional density curve in one call; the
    old `seaborn.distplot` was removed, so `histplot`/`kdeplot` are the modern API.
    """
    print("== Histograms and density plots ==")

    with tempfile.TemporaryDirectory() as tmp:
        tips = _make_tips()
        tips["tip_pct"] = tips["tip"] / (tips["total_bill"] - tips["tip"])

        # Histogram of tip percentages.
        tips["tip_pct"].plot.hist(bins=50)
        _save("hist.png", tmp)

        # Kernel-density (KDE) estimate of the same data.
        tips["tip_pct"].plot.density()
        _save("density.png", tmp)

        # seaborn.histplot on a bimodal mixture of two normals.
        comp1 = rng.standard_normal(200)
        comp2 = 10 + 2 * rng.standard_normal(200)
        values = pd.Series(np.concatenate([comp1, comp2]))
        # Modern replacement for the removed distplot. Pass the Series as x= so the
        # data is mapped to a single axis (the stubs type the positional data slot
        # as a DataFrame; x= is the documented way to plot one vector).
        sns.histplot(x=values, bins=100, color="black")
        _save("sns_histplot.png", tmp)


def explain_scatter_and_pair_plots() -> None:
    """
    Problem: examine relationships between variables.
    Why: `seaborn.regplot` makes a scatter plot AND fits a linear-regression line
    (with a confidence band). `seaborn.pairplot` draws a scatter-plot matrix (a
    "pairs plot") of every variable against every other, with a density/histogram
    on the diagonal. We replace the book's macrodata.csv with a small synthetic
    macro-style DataFrame and apply the same log-difference transform.
    """
    print("== Scatter / point plots (regplot, pairplot) ==")

    with tempfile.TemporaryDirectory() as tmp:
        # Synthetic stand-in for examples/macrodata.csv: positive, drifting series.
        n = 200
        macro = pd.DataFrame(
            {
                "cpi": 100 + rng.standard_normal(n).cumsum() * 0.5 + np.arange(n) * 0.1,
                "m1": 500 + rng.standard_normal(n).cumsum() * 2 + np.arange(n) * 0.5,
                "tbilrate": 5 + rng.standard_normal(n).cumsum() * 0.05,
                "unemp": 6 + rng.standard_normal(n).cumsum() * 0.05,
            }
        )
        # Keep series positive so log is well-defined.
        macro = macro.clip(lower=0.01)
        data = macro[["cpi", "m1", "tbilrate", "unemp"]]
        # Log differences: a common stationarity transform; dropna drops the first
        # NaN. np.log on a DataFrame works at runtime, but the NumPy stubs return a
        # bare ndarray (no .diff); apply keeps the result a DataFrame for pyright.
        trans_data = data.apply(np.log).diff().dropna()
        # apply is typed as possibly returning a Series; it is a DataFrame here
        # (np.log is element-wise over all columns). Assert it for the seaborn calls.
        assert isinstance(trans_data, pd.DataFrame)
        print(trans_data.tail())

        # regplot: scatter + fitted regression line.
        ax = sns.regplot(x="m1", y="unemp", data=trans_data)
        ax.set_title("Changes in log(m1) versus log(unemp)")
        _save("sns_regplot.png", tmp)

        # pairplot returns its own figure; KDE on the diagonal, alpha on the points.
        grid = sns.pairplot(trans_data, diag_kind="kde", plot_kws={"alpha": 0.2})
        grid.savefig(Path(tmp) / "sns_pairplot.png")
        print(f"saved sns_pairplot.png -> exists={(Path(tmp) / 'sns_pairplot.png').exists()}")
        plt.close("all")


def explain_facet_grids() -> None:
    """
    Problem: split a categorical plot across a grid of subplots.
    Why: `seaborn.catplot` makes a facet grid — a 2-D layout where the data is split
    by the values of `col`/`row` variables, with `hue` adding a within-facet split.
    `kind=` chooses the plot type ("bar", "box", ...). We filter outliers as the
    book does (tips.tip_pct < 1) before faceting by day/time/smoker.
    """
    print("== Facet grids and categorical data (catplot) ==")

    with tempfile.TemporaryDirectory() as tmp:
        tips = _make_tips()
        tips["tip_pct"] = tips["tip"] / (tips["total_bill"] - tips["tip"])

        # Boolean row-filters to drop tip_pct outliers, as the book does. Boolean
        # indexing is typed as Series | DataFrame by the stubs; assert it is a
        # DataFrame (which it always is when the mask is a Series) so catplot's
        # data= parameter type-checks.
        no_outliers = tips[tips["tip_pct"] < 1]
        assert isinstance(no_outliers, pd.DataFrame)
        tight = tips[tips["tip_pct"] < 0.5]
        assert isinstance(tight, pd.DataFrame)

        # Facet by smoker (columns), hue by time, bar plot of tip_pct per day.
        g1 = sns.catplot(
            x="day",
            y="tip_pct",
            hue="time",
            col="smoker",
            kind="bar",
            data=no_outliers,
        )
        g1.savefig(Path(tmp) / "catplot_bar.png")  # catplot returns a FacetGrid
        print(f"saved catplot_bar.png -> exists={(Path(tmp) / 'catplot_bar.png').exists()}")
        plt.close("all")

        # Expand the grid: one row per time value, columns by smoker.
        g2 = sns.catplot(
            x="day",
            y="tip_pct",
            row="time",
            col="smoker",
            kind="bar",
            data=no_outliers,
        )
        g2.savefig(Path(tmp) / "catplot_grid.png")
        print(f"saved catplot_grid.png -> exists={(Path(tmp) / 'catplot_grid.png').exists()}")
        plt.close("all")

        # catplot supports other kinds, e.g. box plots (median, quartiles, outliers).
        g3 = sns.catplot(x="tip_pct", y="day", kind="box", data=tight)
        g3.savefig(Path(tmp) / "catplot_box.png")
        print(f"saved catplot_box.png -> exists={(Path(tmp) / 'catplot_box.png').exists()}")
        plt.close("all")


def main() -> None:
    explain_line_plots()
    explain_bar_plots()
    explain_stacked_proportions_and_seaborn_bar()
    explain_histograms_and_density()
    explain_scatter_and_pair_plots()
    explain_facet_grids()


main()
