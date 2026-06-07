"""
Linear Algebra (Section 4.6)

Linear algebra operations — matrix multiplication, decompositions, determinants,
and other square-matrix math — are an important part of many array libraries.

A subtlety to remember: multiplying two 2D arrays with `*` is an ELEMENT-WISE
product, NOT matrix multiplication. For true matrix multiplication use the `dot`
function/method or the `@` infix operator. The numpy.linalg submodule provides
the standard decompositions, inverses, and determinants.

COMMONLY USED numpy.linalg FUNCTIONS
diag    Return the diagonal of a square matrix as a 1D array, or build a diagonal matrix from a 1D array
dot     Matrix multiplication
trace   Sum of the diagonal elements
det     Matrix determinant
eig     Eigenvalues and eigenvectors of a square matrix
inv     Inverse of a square matrix
pinv    Moore-Penrose pseudoinverse
qr      QR decomposition
svd     Singular value decomposition (SVD)
solve   Solve the linear system Ax = b for x (A square)
lstsq   Least-squares solution to Ax = b

Run:
    python3 cap_04_numpy/5-linear-algebra.py
"""

import numpy as np
from numpy.linalg import inv, qr


def explain_matrix_multiplication() -> None:
    """
    Problem: multiply matrices (as opposed to element-wise multiplication).
    Why: x.dot(y), np.dot(x, y), and x @ y all compute the matrix product. A 2D
    array times a suitably sized 1D array yields a 1D array.
    """
    print("== Matrix multiplication ==")

    x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    y = np.array([[6.0, 23.0], [-1.0, 7.0], [8.0, 9.0]])
    print(x.dot(y))         # method form
    print(np.dot(x, y))     # equivalent function form
    print(x @ y)            # equivalent @ operator

    # A 2D array times a 1D array of matching length gives a 1D array.
    print(x @ np.ones(3))   # [ 6. 15.]


def explain_linalg_functions() -> None:
    """
    Problem: compute an inverse and a decomposition of a matrix.
    Why: numpy.linalg offers inv (inverse), qr (QR decomposition), and more.
    A matrix times its inverse returns (approximately) the identity matrix.
    """
    print("== numpy.linalg: inverse and decompositions ==")

    rng = np.random.default_rng(seed=12345)
    X = rng.standard_normal((5, 5))
    # X.T @ X is symmetric positive-definite, so it is safely invertible.
    mat = X.T @ X
    print(inv(mat))
    # A matrix times its inverse is (up to floating-point error) the identity.
    print(mat @ inv(mat))

    # QR decomposition factors a matrix into Q (orthogonal) and R (upper-triangular).
    q, r = qr(mat)
    print(q.shape)  # (5, 5)
    print(r.shape)  # (5, 5)


def explain_diag_and_trace() -> None:
    """
    Problem: read the diagonal and the trace of a square matrix.
    Why: np.diag extracts (or builds) a diagonal, and np.trace sums the diagonal
    elements — both are common building blocks in linear algebra.
    """
    print("== diag and trace ==")

    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(np.diag(arr))   # the diagonal -> [1 5 9]
    print(np.trace(arr))  # sum of the diagonal -> 15


def main() -> None:
    explain_matrix_multiplication()
    explain_linalg_functions()
    explain_diag_and_trace()


main()
