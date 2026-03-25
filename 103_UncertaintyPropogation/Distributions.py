from statistics import stdev

from Kernals import Kernal


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

    std: float
    n: int
    h: float

    def __init__(self, kernel: Kernal, points: list):
        self.kernel = kernel
        self.points = points

        self.std = stdev(self.points)
        self.n = len(self.points)
        self.h = 1.06 * self.std * self.n ** -0.2

    def pdf(self, x):
        p = 0
        for point in self.points:
            p += self.kernel.f((x - point) / self.h)
        return p

    def cdf(self, x):
        p = 0
        for point in self.points:
            p += self.kernel.F((x - point) / self.h)
        return p / (self.n * self.h)