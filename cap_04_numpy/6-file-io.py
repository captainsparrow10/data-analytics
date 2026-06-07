"""
File Input and Output with Arrays (Section 4.5)

NumPy can save and load data to and from disk in text or binary formats. This file
covers only NumPy's built-in binary format, since most users prefer pandas and
other tools for loading text or tabular data (see later chapters).

  * np.save / np.load   — the workhorse pair for a single array (.npy format).
  * np.savez            — store several arrays in one uncompressed .npz archive,
                          passed as keyword arguments and loaded lazily by name.
  * np.savez_compressed — same as savez, but compresses well-compressible data.

The examples below write to a temporary directory and clean it up automatically,
so the file stays runnable and leaves nothing behind in the repository.

Run:
    poetry run python cap_04_numpy/6-file-io.py
"""

import os
import tempfile

import numpy as np


def explain_file_io() -> None:
    """
    Problem: persist arrays to disk and load them back.
    Why: np.save/np.load use NumPy's binary .npy format; np.savez stores several
    arrays in one .npz archive, loaded lazily by name. We use a temporary
    directory and clean up so the example stays runnable and leaves no files.
    """
    print("== File input and output with arrays ==")

    arr = np.arange(10)
    with tempfile.TemporaryDirectory() as tmp:
        # np.save writes a single array; the .npy extension is appended if absent.
        single_path = os.path.join(tmp, "some_array")
        np.save(single_path, arr)
        print(np.load(single_path + ".npy"))

        # np.savez stores multiple arrays as keyword arguments in one archive.
        archive_path = os.path.join(tmp, "array_archive.npz")
        np.savez(archive_path, a=arr, b=arr)
        loaded = np.load(archive_path)
        print(loaded["b"])  # arrays are loaded lazily, accessed by their name

        # For data that compresses well, savez_compressed produces a smaller file.
        compressed_path = os.path.join(tmp, "arrays_compressed.npz")
        np.savez_compressed(compressed_path, a=arr, b=arr)
        print(os.path.exists(compressed_path))  # True


def main() -> None:
    explain_file_io()


main()
