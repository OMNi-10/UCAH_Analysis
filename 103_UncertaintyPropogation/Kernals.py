

class Kernal:
    def f(self, x):
        pass

    def F(self, x):
        pass

class Epanechnikov(Kernal):
    def f(self, x):
        if x < -1 or x > 1:
            return 0
        else:
            return 0.75*(1 - x^2)

    def F(self, x):
        if x < -1:
            return 0
        elif x > 1:
            return 1
        else:
            return 0.75*(x - x**3 /3)