import numpy as np
from numpy import argmin
from numpy import asarray
from numpy.linalg import det
from numpy.linalg import multi_dot
from scipy.linalg import norm
from scipy.linalg import svd
from scipy.spatial.distance import cdist

from compas.geometry import pca_numpy
from compas.geometry import transform_points_numpy
from compas.linalg import normrow
from compas.tolerance import TOL


def bestfit_transform(A, B):
    n, m = A.shape
    Am = np.mean(A, axis=0)
    Bm = np.mean(B, axis=0)
    AA = A - Am
    BB = B - Bm
    # cross-covariance matrix
    C = np.dot(AA.T, BB)
    U, S, Vt = svd(C)
    # rigid rotation of the data frames
    R = np.dot(Vt.T, U.T)
    # check for RotoReflection
    if det(R) < 0:
        Vt[m - 1, :] *= -1
        R = np.dot(Vt.T, U.T)
    # translation that moves data set means to same location
    # this can be done differently (by applying three transformations (T1, R, T2))
    T = Bm.T - np.dot(R, Am.T)
    X = np.identity(m + 1)
    X[:m, :m] = R
    X[:m, m] = T
    return X


def icp_numpy_no_pca(source, target, tol=None, maxiter=100):
    """ICP without PCA-based initial alignment."""
    from compas.geometry import Transformation

    tol = tol or TOL.approximation

    A = asarray(source)
    B = asarray(target)

    # Skip PCA — use identity as initial transform
    X = Transformation()  # Identity transformation
    stack = [asarray(X.matrix)]

    for i in range(maxiter):
        D = cdist(A, B, "euclidean")
        closest = argmin(D, axis=1)
        residual = norm(normrow(A - B[closest]))

        if TOL.is_zero(residual, tol=tol):
            break

        X = bestfit_transform(A, B[closest])
        A = transform_points_numpy(A, X)

        stack.append(X)

    if len(stack) == 1:
        return stack[0]
    return A, multi_dot(stack[::-1])