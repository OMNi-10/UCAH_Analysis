import json
import math

import numpy as np
import numpy.typing as npt

def read_json(filename: str) -> dict:
    with open(filename, "r") as f:
        return json.load(f)

def get_digits(n: int) -> int:
    return math.floor(math.log10(n))

def standardize(input: int | float | list | npt.NDArray) -> npt.NDArray:
    if type(input) == int or type(input) == float:
        return np.array([input])
    elif type(input) == list:
        return np.array(input)
    elif type(input) == np.ndarray:
        return input
    else:
        raise TypeError(f"Input type {type(input)} not supported")