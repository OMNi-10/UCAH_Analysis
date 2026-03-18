import numpy as np
import numpy.typing as npt
from scipy.stats import norm

from Utils.functions import standardize

# TODO: Refactor to handle 2d arrays.
def invCDF(prob, mean = None, var = None) -> npt.NDArray:
    prob: npt.NDArray = standardize(prob)

    if prob.ndim == 1:
        prob = prob[np.newaxis, :]
    elif prob.ndim > 2:
        raise ValueError(f"Probability Array must be of dimension 1 or 2.")
    n = prob.shape[0]
    dims = prob.shape[1]

    if mean is None:
        mean = np.zeros(dims)
    mean: npt.NDArray = standardize(mean)

    if var is None:
        var = np.ones(dims)
    var: npt.NDArray = standardize(var)

    samp = np.zeros([n, dims])
    for i in range(0, n):
        for j in range(0, dims):
            samp[i, j] = norm.ppf(prob[i, j], loc=mean[j], scale=var[j])

    return samp

if __name__ == "__main__":
    M = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    V = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    P = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    invCDF(P, M, V)