from math import sqrt

from Fluids import Fluid, Air

# Ideal Gas Law
def density(pressure, temperature, fluid: Fluid = Air):
    return fluid.R * T / p

def reynolds(density, velocity, length, d_viscosity):
    return density * velocity * length / d_viscosity

def mach(velocity, temperature, fluid: Fluid = Air):
    return velocity / sqrt(fluid.gamma * fluid.R * temperature)

def stanton(conv_heat_transfer_coef, density, velocity, fluid: Fluid = Air):
    return conv_heat_transfer_coef / (density * velocity * fluid.c_p)