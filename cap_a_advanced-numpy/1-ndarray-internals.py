"""
ndarray Object Internals (Appendix A.1)

The NumPy ndarray is a way to interpret a block of homogeneously typed data --
either contiguous or strided -- as a multidimensional array object. What makes
it flexible is that every array is a *strided view* on a block of memory: a view
like arr[::2, ::-1] does not copy any data, it only changes the striding
information. Internally an ndarray is more than a chunk of memory and a dtype;
it consists of:

  * A POINTER to data -- a block of memory in RAM or a memory-mapped file.
  * The DTYPE -- describing fixed-size value cells in the array.
  * A SHAPE tuple -- the size of each dimension.
  * A STRIDES tuple -- bytes to "step" to advance one element along a dimension.

This file also covers the NumPy data type hierarchy: dtypes have superclasses
(np.integer, np.floating, ...) that np.issubdtype can test against, and the
.mro() method shows the parent classes of a dtype.

NDARRAY INTERNAL COMPONENTS
COMPONENT    DESCRIPTION
data         Pointer to the block of memory holding the raw bytes
dtype        Data type describing each fixed-size value cell
shape        Tuple giving the size of each dimension
strides      Tuple of byte steps to advance one element along each dimension
flags        Memory-layout metadata (C/Fortran contiguity, ownership, ...)

Run:
    poetry run python cap_a_advanced-numpy/1-ndarray-internals.py
"""

import numpy as np


def explain_strides_and_layout() -> None:
    """
    Problem: see the striding information that turns a flat memory block into a
    multidimensional array.
    Why: shape says how big each dimension is, but strides say how many BYTES to
    jump to move one step along each axis. Understanding strides explains why
    zero-copy views (slices, transposes) are cheap.
    """
    print("== Strides and the strided memory model ==")

    # shape reports the size of each dimension: a 10 x 5 array.
    print(np.ones((10, 5)).shape)  # (10, 5)

    # A C-order (row-major) 3 x 4 x 5 array of 8-byte float64 values has strides
    # (160, 40, 8): step 8 bytes for the last axis, 40 (= 5 * 8) for the middle,
    # 160 (= 4 * 5 * 8) for the first. Larger strides on an axis mean traversing
    # that axis is more costly.
    print(np.ones((3, 4, 5), dtype=np.float64).strides)  # (160, 40, 8)

    # Negative strides power "backward" views like arr[::-1] -- still zero-copy.
    arr = np.arange(12).reshape((3, 4))
    print(arr.strides)            # (32, 8) -> int64 is 8 bytes
    print(arr[::-1].strides)      # (-32, 8) -> reversed rows via a negative stride


def explain_flags_and_contiguity() -> None:
    """
    Problem: tell whether an array's memory is laid out in C (row-major) or
    Fortran (column-major) contiguous order.
    Why: the flags attribute exposes that metadata. Contiguity affects
    performance (cache behavior) and which fast code paths NumPy can take.
    """
    print("== Flags and C vs Fortran contiguity ==")

    # By default NumPy arrays are created C-contiguous (row-major).
    arr_c = np.ones((100, 10000), order="C")
    # order="F" requests Fortran-contiguous (column-major) storage.
    arr_f = np.ones((100, 10000), order="F")

    # The flags object reports the layout. A C-contiguous array is NOT also
    # Fortran-contiguous (unless it is 1D), and vice versa.
    print(arr_c.flags["C_CONTIGUOUS"])  # True
    print(arr_c.flags["F_CONTIGUOUS"])  # False
    print(arr_f.flags["C_CONTIGUOUS"])  # False
    print(arr_f.flags["F_CONTIGUOUS"])  # True

    # Individual flags can also be read as attributes.
    print(arr_f.flags.f_contiguous)     # True

    # A view (slice) is NOT guaranteed to stay contiguous: skipping columns
    # breaks both C and Fortran contiguity.
    print(arr_c[:, :50].flags["C_CONTIGUOUS"])  # False

    # If you need a specific layout, copy and pass the desired order.
    print(arr_f.copy("C").flags["C_CONTIGUOUS"])  # True


def explain_dtype_hierarchy() -> None:
    """
    Problem: check whether an array holds integers, floats, etc. without listing
    every concrete dtype (int8, int16, ... float128).
    Why: NumPy dtypes have superclasses such as np.integer and np.floating.
    np.issubdtype tests membership against a superclass, and .mro() reveals the
    full parent chain.
    """
    print("== The NumPy data type hierarchy ==")

    ints = np.ones(10, dtype=np.uint16)
    floats = np.ones(10, dtype=np.float32)

    # issubdtype answers "is this dtype a kind of <superclass>?".
    print(np.issubdtype(ints.dtype, np.integer))    # True
    print(np.issubdtype(floats.dtype, np.floating))  # True

    # mro() (method resolution order) lists every parent class of a dtype, from
    # the concrete type up to object.
    print(np.float64.mro())

    # Both integers and floats descend from np.number, the numeric superclass.
    print(np.issubdtype(ints.dtype, np.number))     # True


def main() -> None:
    explain_strides_and_layout()
    explain_flags_and_contiguity()
    explain_dtype_hierarchy()


main()
