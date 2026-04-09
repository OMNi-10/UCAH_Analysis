
from typing import Callable
import numpy as np
from matplotlib import pyplot as plt

class Optimizer:
    obj_func: Callable[[type[np.array]], float]
    input_size: int

    _max_iterations: int = 1e5
    _stop_stddev: float = 1e-9
    _verbose: bool = False

class FuncPoint():
    position: type[np.array]
    value: float

    def __init__(self, position: type[np.array], value: float):
        self.position = position
        self.value = value

class NelderMead(Optimizer):
    alpha: float = 1.0
    gamma: float = 2.0
    rho:   float = 0.5
    sigma: float = 0.5

    def __init__(self, obj_func: Callable[[type[np.array]], float], input_size):
        self.obj_func = obj_func
        self.input_size = input_size

    def _sorted(self, points: list[FuncPoint]) -> type[np.array]:
        vals = [point.value for point in points]
        return [point for _, point in sorted(zip(vals, points), key=lambda p: p[0])]

    def minimize(self, guess: type[np.array]) -> type[np.array]:
        assert guess.size == self.input_size, f"Shape {guess.shape} does not match input size {input.shape}"

        # Create initial vertices
        origin = np.zeros(self.input_size)
        points: list[FuncPoint] = [FuncPoint(origin, self.obj_func(origin))]
        for i in range(self.input_size):
            point = np.zeros(self.input_size)
            point[i] = 1
            points.append(FuncPoint(point, self.obj_func(point)))

        iter = 0
        while iter < self._max_iterations:
            iter += 1
            vals = [point.value for point in points]
            if np.std(vals) < self._stop_stddev:
                break

            if self._verbose:
                print(f"Iteration {iter}", end=" ... ")
            points = self._sorted(points)
            points = self._step(points)
        if self._verbose:
            print(f"Min value {points[0].value} found at {points[0].position} in {iter} iterations.")
        return points[0].position

    def _step(self, points: list[FuncPoint]) -> list[FuncPoint]:
        assert(len(points) == self.input_size + 1)
        # Centroid Position (ignoring the largest point)
        centroid_pos = np.zeros(self.input_size)
        for point in points[0:-1]:
            centroid_pos += point.position
        centroid_pos /= self.input_size
        centroid = FuncPoint(centroid_pos, self.obj_func(centroid_pos))

        # Reflected Position
        reflected_pos = centroid_pos + self.alpha * (centroid_pos - points[-1].position)
        reflected = FuncPoint(reflected_pos, self.obj_func(reflected_pos))
        if (points[0].value <= reflected.value) and (reflected.value < points[-1].value):
            points[-1] = reflected
            if self._verbose:
                print("reflected.")
            return points

        # Expanded Position
        if (reflected.value < points[0].value):
            expanded_pos = centroid_pos + self.gamma * (reflected_pos - centroid_pos)
            expanded = FuncPoint(expanded_pos, self.obj_func(expanded_pos))
            if (expanded.value < reflected.value):
                points[-1] = expanded
                if self._verbose:
                    print("expanded.")
                return points
            else:
                points[-1] = reflected
                if self._verbose:
                    print("reflected.")
                return points

        # Contraction
        if (reflected.value < points[-1].value):
            contracted_pos = centroid_pos + self.rho * (reflected_pos - centroid_pos)
            contracted = FuncPoint(contracted_pos, self.obj_func(contracted_pos))
            if (contracted.value < reflected.value):
                points[-1] = contracted
                if self._verbose:
                    print("contracted.")
                return points
        elif (reflected.value > points[-1].value):
            contracted_pos = centroid_pos + self.rho * (points[-1].position - centroid_pos)
            contracted = FuncPoint(contracted_pos, self.obj_func(contracted_pos))
            if (contracted.value < points[-1].value):
                points[-1] = contracted
                if self._verbose:
                    print("contracted.")
                return points

        # Shrink
        for i in range(1, len(points)):
            point = points[0].position + self.sigma * (points[i].position - points[0].position)
            points[i] = FuncPoint(point, self.obj_func(point))
        if self._verbose:
            print("shrunk.")
        return points

if __name__ == "__main__":
    def rosenbrock_func(x: type[np.array]) -> float:
        a = 1
        b = 100
        return (a - x[0])**2 + b*(x[1] - x[0]**2)**2

    def danny_func(x: type[np.array]) -> float:
        return 1.031 * x[0]**2 + 2.031 * x[1]**2 + 1e-5

    opt = NelderMead(rosenbrock_func, 2)
    x = opt.minimize(np.array([100, -75]))
    print(x)
