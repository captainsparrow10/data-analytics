"""
Broadcasting (Appendix A.3)

Broadcasting governs how operations behave between arrays of DIFFERENT shapes.
It is powerful but can be confusing even for experienced users. The simplest
case is combining a scalar with an array (the scalar is "broadcast" to every
element). The general rule is:

  THE BROADCASTING RULE
  Two arrays are compatible for broadcasting if, for each trailing dimension
  (starting from the end), the axis lengths match OR one of the lengths is 1.
  Broadcasting is then performed over the missing or length-1 dimensions.

This file covers broadcasting a scalar, broadcasting a lower-dimensional array
over a chosen axis (demeaning columns vs. rows), using reshape and np.newaxis to
insert length-1 axes, and setting array values by broadcasting.

Run:
    poetry run python cap_a_advanced-numpy/3-broadcasting.py
"""

import numpy as np
from numpy.typing import NDArray


def explain_scalar_and_column_broadcast() -> None:
    """
    Problem: combine an array with a scalar, then subtract a per-column value.
    Why: a scalar broadcasts to every element. A 1D array of column means has
    shape (3,), which matches the trailing dimension of a (4, 3) array, so it
    broadcasts cleanly across axis 0 -- demeaning each column.
    """
    print("== Scalar and column broadcasting ==")

    # The scalar 4 is broadcast to every element in the multiplication.
    arr = np.arange(5)
    print(arr * 4)  # [ 0  4  8 12 16]

    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal((4, 3))
    print(arr.mean(0))  # one mean per column -> shape (3,)

    # Subtracting the (3,) column means broadcasts across the 4 rows.
    demeaned = arr - arr.mean(0)
    print(demeaned)
    # Each column now has (numerically) zero mean.
    print(demeaned.mean(0))


def explain_row_broadcast() -> None:
    """
    Problem: demean each ROW instead of each column.
    Why: the row means have shape (4,), which does NOT match the trailing
    dimension (3), so subtracting directly fails. Reshaping to (4, 1) makes the
    trailing dimension 1, which broadcasts across the columns.
    """
    print("== Broadcasting over other axes (rows) ==")

    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal((4, 3))
    row_means = arr.mean(1)
    print(row_means.shape)  # (4,) -> incompatible trailing dim with (4, 3)

    # Reshape to (4, 1): a length-1 trailing axis broadcasts across columns.
    print(row_means.reshape((4, 1)))
    demeaned = arr - row_means.reshape((4, 1))
    print(demeaned)
    print(demeaned.mean(1))  # each row now has zero mean


def explain_newaxis() -> None:
    """
    Problem: insert a new length-1 axis for broadcasting without building a shape
    tuple by hand.
    Why: np.newaxis used inside indexing adds a length-1 dimension at that
    position, which is often clearer than reshape -- especially for higher-
    dimensional demeaning.
    """
    print("== Inserting axes with np.newaxis ==")

    # np.newaxis turns a (4, 4) array into (4, 1, 4) by inserting a middle axis.
    arr = np.zeros((4, 4))
    arr_3d = arr[:, np.newaxis, :]
    print(arr_3d.shape)  # (4, 1, 4)

    # On a 1D array it builds a column or a row vector depending on position.
    rng = np.random.default_rng(seed=12345)
    arr_1d = rng.standard_normal(3)
    print(arr_1d[:, np.newaxis])  # column vector, shape (3, 1)
    print(arr_1d[np.newaxis, :])  # row vector, shape (1, 3)

    # Demeaning a chosen axis of a 3D array: depth means have shape (3, 4); add a
    # trailing length-1 axis so they broadcast across axis 2.
    arr = rng.standard_normal((3, 4, 5))
    depth_means = arr.mean(2)
    print(depth_means.shape)  # (3, 4)
    demeaned = arr - depth_means[:, :, np.newaxis]
    print(demeaned.mean(2))   # all (numerically) zero


def demean_axis(arr: NDArray[np.float64], axis: int = 0) -> NDArray[np.float64]:
    """
    Problem: generalize "subtract the mean along an axis" to any axis of an
    N-dimensional array.
    Why: building the indexer with slice(None) (the programmatic form of ":")
    plus np.newaxis lets one function demean along any requested axis.
    """
    means = arr.mean(axis)
    # [:, :, np.newaxis, ...] generalized to N dimensions:
    indexer: list[slice | None] = [slice(None)] * arr.ndim
    indexer[axis] = np.newaxis
    return arr - means[tuple(indexer)]


def explain_demean_axis_helper() -> None:
    """
    Problem: show the generalized demeaning helper in action.
    Why: it demonstrates building a dynamic index tuple, the key trick for
    axis-agnostic broadcasting.
    """
    print("== Generalized demeaning over any axis ==")

    rng = np.random.default_rng(seed=12345)
    arr = rng.standard_normal((3, 4, 5))
    result = demean_axis(arr, axis=2)
    print(result.mean(2))  # all (numerically) zero


def explain_setting_by_broadcast() -> None:
    """
    Problem: assign values into an array using broadcasting.
    Why: the broadcasting rule applies to assignment too. A scalar fills
    everything; a compatible-shaped array (e.g. a column vector) fills along the
    broadcast axis.
    """
    print("== Setting array values by broadcasting ==")

    # A scalar fills the whole array.
    arr = np.zeros((4, 3))
    arr[:] = 5
    print(arr)

    # A 1D array of 4 values, reshaped to a column (4, 1), is broadcast across
    # the 3 columns: each row is set to one value.
    col = np.array([1.28, -0.42, 0.44, 1.6])
    arr[:] = col[:, np.newaxis]
    print(arr)

    # Assigning into a slice broadcasts within just those rows.
    arr[:2] = [[-1.37], [0.509]]
    print(arr)


def main() -> None:
    explain_scalar_and_column_broadcast()
    explain_row_broadcast()
    explain_newaxis()
    explain_demean_axis_helper()
    explain_setting_by_broadcast()


main()
