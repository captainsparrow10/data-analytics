"""
Matplotlib: Practice Exercises

A set of hands-on, self-contained exercises that practice the core matplotlib
plotting skills: line plots, multiple series with legends, line styling, bar and
grouped/stacked bar charts, histograms, scatter plots with color/size mappings,
2x2 subplot grids, custom ticks and tick labels, text annotations, pie charts,
and saving at a chosen DPI. Each exercise generates its own small, deterministic
dataset with `np.random.default_rng(seed=...)`, draws one figure, and saves it.

These figures are written to a temporary directory (headless setup): the
non-interactive "Agg" backend is selected before importing pyplot, so nothing is
shown on screen and `plt.show()` is never called. Each exercise saves its figure
with `fig.savefig(...)`, prints a confirmation, and closes the figure. Nothing is
left behind in the repo.

Run:
    poetry run python cap_09_plotting/exercises.py
"""

import os
import tempfile
from pathlib import Path

import matplotlib

# HEADLESS: select the non-interactive Agg backend BEFORE importing pyplot so the
# file runs without a display and never opens a window. Never call plt.show().
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402


def _save(fig: Figure, outdir: str, name: str) -> None:
    """Save a figure into outdir, print a confirmation, then close it."""
    path = Path(outdir) / name
    fig.savefig(path)
    print(f"saved {os.path.basename(path)} -> exists={os.path.exists(path)}")
    plt.close(fig)  # drop the figure so figures never accumulate


def exercise_01(outdir: str) -> None:
    """
    Exercise 1: A Simple Line Plot

    Problem: Plot monthly sales (a single numeric series) against month numbers
    1..12 as a line, and label the chart with a title and both axis labels.

    The saved figure should show one rising line with a title ("Monthly Sales"),
    an x-axis labeled "Month" and a y-axis labeled "Units Sold".
    """
    rng = np.random.default_rng(seed=1)
    months = np.arange(1, 13)  # x values: months 1 through 12
    # A gently rising trend (50 per month) plus small random noise.
    sales = 50 * months + rng.normal(0, 20, size=12)

    fig, ax = plt.subplots()
    ax.plot(months, sales)  # one line: y vs x
    ax.set_title("Monthly Sales")  # chart title
    ax.set_xlabel("Month")  # x-axis label
    ax.set_ylabel("Units Sold")  # y-axis label
    _save(fig, outdir, "ex01_line.png")


def exercise_02(outdir: str) -> None:
    """
    Exercise 2: Multiple Lines With a Legend

    Problem: Plot three products' yearly revenue on the same axes (one line each)
    and add a legend so each line can be identified.

    The saved figure should show three lines over years 2018..2024, each with its
    own label ("Product A/B/C") visible in a legend.
    """
    rng = np.random.default_rng(seed=2)
    years = np.arange(2018, 2025)  # shared x axis: 7 years
    # Three independent random walks starting from different baselines.
    product_a = 100 + rng.normal(0, 10, size=7).cumsum()
    product_b = 120 + rng.normal(0, 10, size=7).cumsum()
    product_c = 90 + rng.normal(0, 10, size=7).cumsum()

    fig, ax = plt.subplots()
    # Pass label= to each line so legend() can pick them up.
    ax.plot(years, product_a, label="Product A")
    ax.plot(years, product_b, label="Product B")
    ax.plot(years, product_c, label="Product C")
    ax.set_title("Revenue by Product")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue")
    ax.legend()  # build the legend from the labels above
    _save(fig, outdir, "ex02_multiline.png")


def exercise_03(outdir: str) -> None:
    """
    Exercise 3: Customizing Line Style, Marker, and Color

    Problem: Plot one sine curve styled explicitly with a custom color, a dashed
    line style, and a circular marker on each sampled point.

    The saved figure should show a single dashed red sine wave with round markers
    at each of its sampled x positions.
    """
    x = np.linspace(0, 2 * np.pi, 20)  # 20 evenly spaced points over one period
    y = np.sin(x)

    fig, ax = plt.subplots()
    # color/linestyle/marker control appearance; linewidth/markersize fine-tune it.
    ax.plot(
        x,
        y,
        color="red",
        linestyle="--",
        marker="o",
        linewidth=2,
        markersize=6,
    )
    ax.set_title("Styled Sine Wave")
    ax.set_xlabel("x")
    ax.set_ylabel("sin(x)")
    _save(fig, outdir, "ex03_style.png")


def exercise_04(outdir: str) -> None:
    """
    Exercise 4: A Bar Chart

    Problem: Draw a vertical bar chart of how many tickets five support teams
    closed, with one labeled bar per team.

    The saved figure should show five vertical bars, one per team
    (Alpha..Echo), each height equal to that team's closed-ticket count.
    """
    rng = np.random.default_rng(seed=4)
    teams = ["Alpha", "Beta", "Gamma", "Delta", "Echo"]
    closed = rng.integers(20, 80, size=5)  # a count per team

    fig, ax = plt.subplots()
    ax.bar(teams, closed, color="steelblue")  # categorical x, numeric heights
    ax.set_title("Tickets Closed by Team")
    ax.set_xlabel("Team")
    ax.set_ylabel("Tickets Closed")
    _save(fig, outdir, "ex04_bar.png")


def exercise_05(outdir: str) -> None:
    """
    Exercise 5: A Grouped Bar Chart

    Problem: Compare two quarters (Q1 vs Q2) across four regions by drawing two
    bars side by side per region.

    The saved figure should show four region groups on the x axis, each with two
    adjacent bars (Q1 and Q2), distinguished in a legend.
    """
    rng = np.random.default_rng(seed=5)
    regions = ["North", "South", "East", "West"]
    q1 = rng.integers(40, 100, size=4)
    q2 = rng.integers(40, 100, size=4)

    x = np.arange(len(regions))  # one base position per region
    width = 0.35  # width of each bar within a group

    fig, ax = plt.subplots()
    # Shift Q1 left and Q2 right of each base position so they sit side by side.
    ax.bar(x - width / 2, q1, width, label="Q1")
    ax.bar(x + width / 2, q2, width, label="Q2")
    ax.set_title("Sales by Region and Quarter")
    ax.set_xlabel("Region")
    ax.set_ylabel("Sales")
    ax.set_xticks(x)  # center the tick under each group
    ax.set_xticklabels(regions)
    ax.legend()
    _save(fig, outdir, "ex05_grouped_bar.png")


def exercise_06(outdir: str) -> None:
    """
    Exercise 6: A Stacked Bar Chart

    Problem: Show each month's total energy use split into two sources (solar and
    wind) by stacking one source on top of the other in the same bar.

    The saved figure should show one bar per month, where each bar is split into a
    solar segment and a wind segment stacked on top, with a legend.
    """
    rng = np.random.default_rng(seed=6)
    months = ["Jan", "Feb", "Mar", "Apr", "May"]
    solar = rng.integers(20, 60, size=5)
    wind = rng.integers(20, 60, size=5)

    fig, ax = plt.subplots()
    ax.bar(months, solar, label="Solar")
    # bottom= stacks the wind segment directly on top of the solar segment.
    ax.bar(months, wind, bottom=solar, label="Wind")
    ax.set_title("Energy Production by Source")
    ax.set_xlabel("Month")
    ax.set_ylabel("Energy (MWh)")
    ax.legend()
    _save(fig, outdir, "ex06_stacked_bar.png")


def exercise_07(outdir: str) -> None:
    """
    Exercise 7: A Histogram

    Problem: Draw a histogram of 1000 samples from a normal distribution to show
    how the values are distributed across bins.

    The saved figure should show a roughly bell-shaped histogram with 30 bins.
    """
    rng = np.random.default_rng(seed=7)
    data = rng.normal(loc=0, scale=1, size=1000)  # 1000 normal samples

    fig, ax = plt.subplots()
    ax.hist(data, bins=30, color="seagreen", edgecolor="black")  # 30 bins
    ax.set_title("Distribution of Samples")
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    _save(fig, outdir, "ex07_hist.png")


def exercise_08(outdir: str) -> None:
    """
    Exercise 8: A Scatter Plot With Color and Size

    Problem: Plot 50 random (x, y) points where each point's COLOR encodes a third
    variable and its SIZE encodes a fourth, then add a colorbar.

    The saved figure should show a scattering of 50 dots of varying sizes and
    colors, with a colorbar mapping color to the third variable.
    """
    rng = np.random.default_rng(seed=8)
    x = rng.uniform(0, 10, size=50)
    y = rng.uniform(0, 10, size=50)
    colors = rng.uniform(0, 1, size=50)  # mapped to the colormap
    sizes = rng.uniform(20, 200, size=50)  # marker areas in points^2

    fig, ax = plt.subplots()
    # c= maps to a colormap; s= sets per-point size; alpha makes overlaps visible.
    scatter = ax.scatter(x, y, c=colors, s=sizes, cmap="viridis", alpha=0.7)
    ax.set_title("Scatter With Color and Size")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    fig.colorbar(scatter, ax=ax, label="Intensity")  # legend for the color scale
    _save(fig, outdir, "ex08_scatter.png")


def exercise_09(outdir: str) -> None:
    """
    Exercise 9: A 2x2 Grid of Subplots

    Problem: Create one figure with a 2x2 grid of subplots and draw a different
    chart type in each cell: a line, a scatter, a bar, and a histogram.

    The saved figure should show four panels arranged 2x2, each with its own
    small title.
    """
    rng = np.random.default_rng(seed=9)

    # plt.subplots returns a figure plus a 2-D array of Axes indexed like a matrix.
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))

    # Top-left: a simple line.
    axes[0, 0].plot(np.arange(10), rng.normal(0, 1, size=10).cumsum())
    axes[0, 0].set_title("Line")

    # Top-right: a scatter.
    axes[0, 1].scatter(rng.uniform(size=20), rng.uniform(size=20))
    axes[0, 1].set_title("Scatter")

    # Bottom-left: a bar chart.
    axes[1, 0].bar(["A", "B", "C"], rng.integers(1, 10, size=3))
    axes[1, 0].set_title("Bar")

    # Bottom-right: a histogram.
    axes[1, 1].hist(rng.normal(size=200), bins=15)
    axes[1, 1].set_title("Histogram")

    fig.suptitle("Four Chart Types")  # one overall figure title
    fig.tight_layout()  # keep titles/labels from overlapping
    _save(fig, outdir, "ex09_grid.png")


def exercise_10(outdir: str) -> None:
    """
    Exercise 10: Customizing Ticks and Tick Labels

    Problem: Plot weekday traffic and replace the numeric x ticks with the weekday
    names, rotated for readability.

    The saved figure should show a line whose x-axis ticks read Mon..Sun (rotated
    45 degrees) instead of 0..6.
    """
    rng = np.random.default_rng(seed=10)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    traffic = rng.integers(100, 500, size=7)
    x = np.arange(len(days))

    fig, ax = plt.subplots()
    ax.plot(x, traffic, marker="o")
    ax.set_xticks(x)  # tick at each weekday position
    ax.set_xticklabels(days, rotation=45)  # override numeric labels with names
    ax.set_title("Weekly Traffic")
    ax.set_xlabel("Day")
    ax.set_ylabel("Visitors")
    _save(fig, outdir, "ex10_ticks.png")


def exercise_11(outdir: str) -> None:
    """
    Exercise 11: Adding Text and an Annotation

    Problem: Plot a curve, mark its maximum point with an arrow annotation, and
    place a plain text label elsewhere on the axes.

    The saved figure should show a curve with an arrow pointing to its peak
    labeled "Peak", plus a free-floating text note.
    """
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.exp(-x / 10)  # a damped sine wave

    fig, ax = plt.subplots()
    ax.plot(x, y)

    # Locate the maximum point to annotate.
    peak_idx = int(np.argmax(y))
    peak_x = float(x[peak_idx])
    peak_y = float(y[peak_idx])

    # annotate draws text plus an arrow from xytext -> xy (the peak).
    ax.annotate(
        "Peak",
        xy=(peak_x, peak_y),
        xytext=(peak_x + 1.5, peak_y + 0.2),
        arrowprops=dict(facecolor="black", width=1.5, headwidth=8),
    )
    # text writes a plain label at data coordinates (no arrow).
    ax.text(6, -0.4, "Damped sine", style="italic")
    ax.set_title("Annotated Curve")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    _save(fig, outdir, "ex11_annotation.png")


def exercise_12(outdir: str) -> None:
    """
    Exercise 12: A Pie Chart

    Problem: Draw a pie chart of market share across four browsers, showing each
    slice's percentage and slightly exploding the largest slice.

    The saved figure should show a four-slice pie with percentage labels, a legend
    of browser names, and one slice pulled slightly out.
    """
    browsers = ["Chrome", "Safari", "Edge", "Firefox"]
    share = np.array([63.0, 20.0, 11.0, 6.0])  # percentages (sum to 100)

    # Pull the largest slice slightly outward for emphasis.
    explode = [0.1 if v == share.max() else 0.0 for v in share]

    fig, ax = plt.subplots()
    ax.pie(
        share,
        labels=browsers,
        autopct="%1.1f%%",  # show each slice's percentage
        explode=explode,
        startangle=90,
    )
    ax.set_title("Browser Market Share")
    ax.axis("equal")  # equal aspect keeps the pie circular
    _save(fig, outdir, "ex12_pie.png")


def exercise_13(outdir: str) -> None:
    """
    Exercise 13: Saving a Figure at a Given DPI

    Problem: Render a line plot and save it twice at two different DPI settings to
    see how resolution affects the output file.

    The saved figures should be the same plot written at 72 DPI (low resolution)
    and 300 DPI (print resolution); both files must exist on disk.
    """
    rng = np.random.default_rng(seed=13)
    x = np.arange(50)
    y = rng.normal(0, 1, size=50).cumsum()

    fig, ax = plt.subplots()
    ax.plot(x, y, color="purple")
    ax.set_title("Saved at Two Resolutions")
    ax.set_xlabel("Step")
    ax.set_ylabel("Value")

    # dpi controls dots-per-inch; higher DPI -> sharper raster, larger file.
    low_path = Path(outdir) / "ex13_low_dpi.png"
    high_path = Path(outdir) / "ex13_high_dpi.png"
    fig.savefig(low_path, dpi=72)
    fig.savefig(high_path, dpi=300)
    print(f"saved {low_path.name} -> exists={low_path.exists()} (72 dpi)")
    print(f"saved {high_path.name} -> exists={high_path.exists()} (300 dpi)")
    plt.close(fig)


def main() -> None:
    # One shared temp dir owns every figure; it is removed on exit so the repo
    # stays clean. Each exercise receives the dir path and saves into it.
    with tempfile.TemporaryDirectory() as outdir:
        print("=== Exercise 1: A Simple Line Plot ===")
        exercise_01(outdir)

        print("\n=== Exercise 2: Multiple Lines With a Legend ===")
        exercise_02(outdir)

        print("\n=== Exercise 3: Customizing Line Style, Marker, and Color ===")
        exercise_03(outdir)

        print("\n=== Exercise 4: A Bar Chart ===")
        exercise_04(outdir)

        print("\n=== Exercise 5: A Grouped Bar Chart ===")
        exercise_05(outdir)

        print("\n=== Exercise 6: A Stacked Bar Chart ===")
        exercise_06(outdir)

        print("\n=== Exercise 7: A Histogram ===")
        exercise_07(outdir)

        print("\n=== Exercise 8: A Scatter Plot With Color and Size ===")
        exercise_08(outdir)

        print("\n=== Exercise 9: A 2x2 Grid of Subplots ===")
        exercise_09(outdir)

        print("\n=== Exercise 10: Customizing Ticks and Tick Labels ===")
        exercise_10(outdir)

        print("\n=== Exercise 11: Adding Text and an Annotation ===")
        exercise_11(outdir)

        print("\n=== Exercise 12: A Pie Chart ===")
        exercise_12(outdir)

        print("\n=== Exercise 13: Saving a Figure at a Given DPI ===")
        exercise_13(outdir)


main()
