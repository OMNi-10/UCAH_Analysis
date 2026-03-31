import numpy as np


class Kernal:
    def f(self, x):
        pass

    def F(self, x):
        pass

class Epanechnikov(Kernal):
    def f(self, x):
        if type(x) == np.ndarray:
            mag = np.linalg.norm(x)
            if mag > 1:
                return 0
            else:
                return 0.75 * (1 - x.transpose().dot(x)[0, 0])

        else:
            if x < -1 or x > 1:
                return 0
            else:
                return 0.75 * (1 - x ** 2)


    def F(self, x):
        if x < -1:
            return 0
        elif x > 1:
            return 1
        else:
            return 0.75*(x - x**3 /3)

class Normal(Kernal):
    def __init__(self, dims):
        self.dims = dims

    def f(self, x: np.array):
        x = x.reshape(-1, 1)
        d = x.shape[0]

        p = (2  * np.pi) ** (-d/2) * np.exp(-0.5 * x.transpose().dot(x))
        return p