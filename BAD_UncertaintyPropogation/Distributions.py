from statistics import stdev

import numpy as np

from BAD_UncertaintyPropogation.Kernals import Kernal


class Distribution:
    def pdf(self, x):
        pass

    def cdf(self, x):
        pass

    def icdf(self, x):
        pass


class Uniform(Distribution):
    a: float
    b: float

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def pdf(self, x):
        return 1 / (self.a - self.b)

    def cdf(self, x):
        if x < self.a:
            return 0
        elif x > self.b:
            return 1
        else:
            return (x - self.a) / (self.b - self.a)

    def icdf(self, p):
        return p * (self.b - self.a) + self.a


class Normal(Distribution):
    mean: float
    std: float

    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def pdf(self, x):
        raise NotImplementedError

    def cdf(self, x):
        raise NotImplementedError


class FitDistribution(Distribution):
    kernel: Kernal
    points: list

    std: float | list[float]
    n: int
    h: float

    def __init__(self, kernel: Kernal, points: list):
        self.kernel = kernel
        self.points = points


        self.n = len(self.points)
        self.std = stdev(self.points)
        self.h = 1.06 * self.std * self.n ** -0.2

    def pdf(self, x):
        p_list = []
        for x_val in x.flatten():
            p = 0
            for point in self.points:
                p += self.kernel.f((x_val - point) / self.h)
            p_list.append(p / (self.n * self.h))
        return np.array(p_list)

    def cdf(self, x):
        p = 0
        for point in self.points:
            p += self.kernel.F((x - point) / self.h)
        return p / (self.n * self.h)

class KDE(Distribution):
    kernal: Kernal
    data: np.array

    d: int
    n: int
    std: np.array

    H: np.array
    H_inv_sqrt: np.array

    def __init__(self, kernal: Kernal, data: np.array):
        self.kernal = kernal
        self.data = data

        self.n, self.d = data.shape

        std = [None] * self.d
        for i in range(0, self.d):
            std[i] = stdev(data[:, i])
        self.std = np.array(std)
        self.H = np.diag(self.std) * 1.06 * self.n ** -0.2

        L = np.linalg.cholesky(self.H)
        self.H_inv_sqrt = np.linalg.inv(L).T

    def _altered_kernal(self, x):
        x = x.reshape(-1, 1)
        x_tilde = np.linalg.solve(self.H, x)
        return np.linalg.det(self.H) **-0.5 * self.kernal.f(x_tilde)

    def pdf(self, points):
        prob_list = []
        for point in points:
            p = 0
            for sample in self.data:
                point = point.reshape(-1, 1)
                sample = sample.reshape(-1, 1)
                p += self._altered_kernal(point - sample)
            prob_list.append(p / self.n)
            print(f"{p/self.n} <- {point.flatten()}")
        return np.array(prob_list)