"""
A Brief matplotlib API Primer (Section 9.1)

matplotlib is a desktop plotting package designed for creating publication-quality
figures. Plots live inside a `Figure` object; you draw on one or more `Axes`
(subplots) created via `fig.add_subplot` or the convenience `plt.subplots`. The
axes methods (`plot`, `hist`, `scatter`, ...) are preferred over the top-level
`plt.*` functions because they make the target subplot explicit. This file walks
the whole of section 9.1: figures and subplots, spacing, colors/markers/line
styles, ticks/labels/legends, annotations and shapes, saving to disk, and global
configuration via `plt.rc`.

This is a headless study file: the "Agg" backend is selected before importing
pyplot, so NOTHING is shown on screen and no display is required. Every figure is
written into a `tempfile.TemporaryDirectory()` and we print a confirmation, then
`plt.close("all")` is called between examples so figures do not accumulate. The
file runs to completion and leaves nothing behind in the repo.

KEY ENTRY POINTS IN THIS FILE
FUNCTION / METHOD       DESCRIPTION
plt.figure              Create a new, empty Figure object
Figure.add_subplot      Add one Axes (subplot) to a figure grid
plt.subplots            Create a figure plus a NumPy array of Axes at once
Figure.subplots_adjust  Control padding/spacing between subplots
Axes.plot               Line plot with color/linestyle/marker/drawstyle options
set_xticks/xticklabels  Place tick locations and override their labels
set_title/set_xlabel    Title and axis-label decorations on an Axes
Axes.legend             Build a legend from the plotted labels
Axes.annotate / text    Draw arrows+text / plain text at data coordinates
add_patch (Rectangle..) Draw shapes ("patches") onto an Axes
Figure.savefig          Write the figure to a file (format from the extension)
plt.rc                  Set global configuration defaults (rcParams)

Run:
    poetry run python cap_09_plotting/1-matplotlib-primer.py
"""

import os
import tempfile
from datetime import datetime
from pathlib import Path

import matplotlib

# HEADLESS: select the non-interactive Agg backend BEFORE importing pyplot, so the
# file runs without a display and never opens a window. Never call plt.show().
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.dates import date2num  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

# One reproducible random generator for the whole file (the book uses the legacy
# np.random.* functions; np.random.default_rng is the modern, seedable equivalent).
rng = np.random.default_rng(seed=12345)


def _save(fig: Figure, tmp: str, name: str) -> None:
    """Save a figure into the temp dir and print a confirmation, then close it."""
    path = Path(tmp) / name
    fig.savefig(path)
    print(f"saved {os.path.basename(path)} -> exists={os.path.exists(path)}")
    plt.close("all")  # drop the figure so figures never accumulate


def explain_figures_and_subplots() -> None:
    """
    Problem: lay out several plots inside one figure.
    Why: every plot lives in a Figure, but a blank figure draws nothing — you must
    add one or more subplots. `add_subplot(nrows, ncols, index)` carves the figure
    into a grid (here 2x2) and returns the Axes for the 1-based `index`. The axes
    methods (plot/hist/scatter) are preferred over plt.* because they target a
    specific subplot.
    """
    print("== Figures and subplots (add_subplot) ==")

    with tempfile.TemporaryDirectory() as tmp:
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)  # top-left of a 2x2 grid
        ax2 = fig.add_subplot(2, 2, 2)  # top-right
        ax3 = fig.add_subplot(2, 2, 3)  # bottom-left

        # A line plot on ax3: a random walk via cumulative sum, black dashed.
        ax3.plot(rng.standard_normal(50).cumsum(), color="black", linestyle="dashed")
        # A histogram on ax1 and a scatter on ax2, drawn by each Axes directly.
        ax1.hist(rng.standard_normal(100), bins=20, color="black", alpha=0.3)
        ax2.scatter(np.arange(30), np.arange(30) + 3 * rng.standard_normal(30))

        _save(fig, tmp, "subplots.png")


def explain_plt_subplots() -> None:
    """
    Problem: create a whole grid of subplots in one call.
    Why: `plt.subplots` builds the figure AND returns a NumPy array of Axes you can
    index like a 2-D array (axes[0, 1]). `sharex`/`sharey` make the subplots share
    ticks/limits, useful when comparing data on the same scale.
    """
    print("== plt.subplots (grid + array of Axes) ==")

    with tempfile.TemporaryDirectory() as tmp:
        fig, axes = plt.subplots(2, 3)
        # axes is a 2-D ndarray of AxesSubplot; index it like a matrix.
        print(type(axes), axes.shape)
        axes[0, 1].plot(rng.standard_normal(20).cumsum())
        _save(fig, tmp, "grid.png")


def explain_subplots_adjust() -> None:
    """
    Problem: control the padding/spacing between subplots.
    Why: matplotlib leaves default padding around and between subplots; `wspace`
    and `hspace` (fractions of the figure width/height) tune the gaps. Here we set
    both to zero so the histograms touch, exactly as the book demonstrates.
    """
    print("== subplots_adjust (inter-subplot spacing) ==")

    with tempfile.TemporaryDirectory() as tmp:
        fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
        for i in range(2):
            for j in range(2):
                axes[i, j].hist(
                    rng.standard_normal(500), bins=50, color="black", alpha=0.5
                )
        # Shrink the spacing between subplots all the way to zero.
        fig.subplots_adjust(wspace=0, hspace=0)
        _save(fig, tmp, "no_spacing.png")


def explain_colors_markers_linestyles() -> None:
    """
    Problem: style a line's color, dash pattern, point markers, and interpolation.
    Why: `plot` accepts color (a name or a "#RRGGBB" hex code), linestyle ("--",
    "dashed", ...), marker ("o" to highlight the actual data points), and drawstyle
    (how points are connected — "steps-post" makes a step plot instead of straight
    interpolation). Passing `label=` here lets `legend` identify each line later.
    """
    print("== Colors, markers, line styles, drawstyle ==")

    with tempfile.TemporaryDirectory() as tmp:
        fig = plt.figure()
        ax = fig.add_subplot()

        # Dashed black line WITH circular markers on each data point.
        ax.plot(
            rng.standard_normal(30).cumsum(),
            color="black",
            linestyle="dashed",
            marker="o",
        )
        _save(fig, tmp, "markers.png")

        # drawstyle changes how successive points are connected.
        fig = plt.figure()
        ax = fig.add_subplot()
        data = rng.standard_normal(30).cumsum()
        ax.plot(data, color="black", linestyle="dashed", label="Default")
        ax.plot(
            data,
            color="black",
            linestyle="dashed",
            drawstyle="steps-post",
            label="steps-post",
        )
        ax.legend()  # legend() is required even when labels were passed to plot
        _save(fig, tmp, "drawstyle.png")


def explain_ticks_labels_legends() -> None:
    """
    Problem: customize the plot range, tick positions, tick text, title, and legend.
    Why: most decorations are Axes methods. `set_xticks` places ticks along the data
    range; `set_xticklabels` overrides their text (with rotation/fontsize);
    `set_xlabel` names the axis and `set_title` titles the subplot. For legends,
    pass `label=` to each plot call, then call `legend()` (with `loc="best"` to let
    matplotlib pick an out-of-the-way spot).
    """
    print("== Ticks, labels, title, and legends ==")

    with tempfile.TemporaryDirectory() as tmp:
        fig, ax = plt.subplots()
        ax.plot(rng.standard_normal(1000).cumsum())

        # Place ticks, then give them custom rotated labels.
        ax.set_xticks([0, 250, 500, 750, 1000])
        ax.set_xticklabels(
            ["one", "two", "three", "four", "five"], rotation=30, fontsize=8
        )
        ax.set_xlabel("Stages")
        ax.set_title("My first matplotlib plot")
        # The Axes `set` method batches several properties in one call.
        ax.set(title="My first matplotlib plot", xlabel="Stages")
        _save(fig, tmp, "ticks.png")

        # Three labeled random walks + an automatic legend.
        fig, ax = plt.subplots()
        ax.plot(rng.standard_normal(1000).cumsum(), color="black", label="one")
        ax.plot(
            rng.standard_normal(1000).cumsum(),
            color="black",
            linestyle="dashed",
            label="two",
        )
        ax.plot(
            rng.standard_normal(1000).cumsum(),
            color="black",
            linestyle="dotted",
            label="three",
        )
        ax.legend(loc="best")  # default "best" avoids overlapping the data
        _save(fig, tmp, "legend.png")


def explain_annotations_and_shapes() -> None:
    """
    Problem: draw your own text, arrows, and shapes on a subplot.
    Why: `ax.text` writes text at data coordinates; `ax.annotate` draws an arrow
    pointing from `xytext` to `xy` with `arrowprops`. Shapes are "patches" objects
    (Rectangle, Circle, Polygon) added with `ax.add_patch`. We rebuild the book's
    S&P 500 crisis-annotation example with an inline synthetic price series (no
    network, no spx.csv): a positive random walk indexed by business days.
    """
    print("== Annotations and drawing shapes (patches) ==")

    with tempfile.TemporaryDirectory() as tmp:
        # --- Synthetic stand-in for the book's examples/spx.csv close prices. ---
        dates = pd.date_range("2007-01-01", "2011-01-01", freq="B")
        # A drifting, always-positive series so annotation y-values make sense.
        walk = 1400 + rng.standard_normal(len(dates)).cumsum() * 5
        spx = pd.Series(walk, index=dates)

        fig, ax = plt.subplots()
        spx.plot(ax=ax, color="black")

        crisis_data = [
            (datetime(2007, 10, 11), "Peak of bull market"),
            (datetime(2008, 3, 12), "Bear Stearns Fails"),
            (datetime(2008, 9, 15), "Lehman Bankruptcy"),
        ]
        # annotate draws label text plus an arrow at each crisis date. matplotlib
        # plots dates internally as float "date numbers"; date2num converts our
        # datetimes to that scale so the float-typed annotate/text/limit APIs accept
        # them (the runtime behavior is identical to passing the datetime directly).
        for date, label in crisis_data:
            x = date2num(date)
            # asof returns the last value at or before the timestamp. The stubs type
            # the result as a broad scalar union (incl. complex); narrow to a real
            # number so float() type-checks.
            value = spx.asof(date)
            assert isinstance(value, (int, float, np.floating))
            y = float(value)
            ax.annotate(
                label,
                xy=(x, y + 75),
                xytext=(x, y + 225),
                arrowprops=dict(facecolor="black", headwidth=4, width=2, headlength=4),
                horizontalalignment="left",
                verticalalignment="top",
            )

        # Zoom into 2007-2010 by setting explicit axis limits.
        ax.set_xlim((date2num(datetime(2007, 1, 1)), date2num(datetime(2011, 1, 1))))
        ax.set_ylim((600.0, 1800.0))
        ax.set_title("Important dates in the 2008-2009 financial crisis")

        # ax.text writes plain text at data coordinates with custom styling.
        ax.text(
            date2num(datetime(2009, 1, 1)),
            1700,
            "Hello world!",
            family="monospace",
            fontsize=10,
        )
        _save(fig, tmp, "annotations.png")

        # --- Shapes: Rectangle, Circle, Polygon added as patches. ---
        fig, ax = plt.subplots()
        # The shape classes (patches) live in matplotlib.patches; plt re-exports
        # them at runtime but the stubs hide that, so we import from the real module.
        rect = Rectangle((0.2, 0.75), 0.4, 0.15, color="black", alpha=0.3)
        circ = Circle((0.7, 0.2), 0.15, color="blue", alpha=0.3)
        pgon = Polygon(
            [[0.15, 0.15], [0.35, 0.4], [0.2, 0.6]], color="green", alpha=0.5
        )
        ax.add_patch(rect)
        ax.add_patch(circ)
        ax.add_patch(pgon)
        _save(fig, tmp, "patches.png")


def explain_saving_plots() -> None:
    """
    Problem: write a figure to disk in a chosen format and resolution.
    Why: `savefig` infers the file type from the extension (.png, .pdf, .svg, ...),
    and `dpi` controls the dots-per-inch resolution for raster formats. Everything
    happens inside a temp dir so the repo stays clean.
    """
    print("== Saving plots to file (savefig) ==")

    with tempfile.TemporaryDirectory() as tmp:
        fig, ax = plt.subplots()
        ax.plot(rng.standard_normal(100).cumsum(), color="black")

        # Format from extension; SVG is vector, PNG is raster.
        svg_path = Path(tmp) / "figpath.svg"
        png_path = Path(tmp) / "figpath.png"
        fig.savefig(svg_path)
        fig.savefig(png_path, dpi=400)  # 400 DPI raster for publishing
        print(f"saved {svg_path.name} -> exists={svg_path.exists()}")
        print(f"saved {png_path.name} -> exists={png_path.exists()}")
        plt.close("all")


def explain_configuration() -> None:
    """
    Problem: change matplotlib's global defaults from Python.
    Why: `plt.rc(component, **kwargs)` sets defaults for a whole component group
    ("figure", "font", "axes", ...). Settings live in the `plt.rcParams` dict and
    can be reverted with `plt.rcdefaults()`. We change a couple of defaults, render
    a figure to prove they took effect, then restore the defaults so the change does
    not leak into later examples.
    """
    print("== matplotlib configuration (plt.rc / rcParams) ==")

    with tempfile.TemporaryDirectory() as tmp:
        # Set a global default figure size and font.
        plt.rc("figure", figsize=(10, 10))
        plt.rc("font", family="monospace", weight="bold", size=8)
        print("figure.figsize default ->", plt.rcParams["figure.figsize"])

        fig, ax = plt.subplots()
        ax.plot(rng.standard_normal(50).cumsum(), color="black")
        _save(fig, tmp, "configured.png")

        # Restore matplotlib's stock defaults so nothing leaks downstream.
        plt.rcdefaults()


def main() -> None:
    explain_figures_and_subplots()
    explain_plt_subplots()
    explain_subplots_adjust()
    explain_colors_markers_linestyles()
    explain_ticks_labels_legends()
    explain_annotations_and_shapes()
    explain_saving_plots()
    explain_configuration()


main()
