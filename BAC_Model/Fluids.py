from functions import read_json

class Fluid:
    R: float
    gamma: float
    c_p: float

    def __init__(self, R: float, gamma: float, c_p: float):
        self.R = R
        self.gamma = gamma
        self.c_p = c_p

air_config = read_json('AAB_PrerequisiteData/air.json')
Air = Fluid(R = air_config['R'], gamma = air_config['gamma'], c_p = air_config['c_p'])