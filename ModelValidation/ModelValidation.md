
# Model Validation
UCAH HyperLarp University of Virginia 

Aerothermal Modeling, Verification and Validation

## Objectives

## Modeling Parameters

### Flight conditions
A given test will occur at a set of conditions which will define the vehicle's reaction to the flow.

Freestream (Dimensional) Flow Characteristics
- speed $u_\infty$
- density $\rho_\infty$
- pressure $p_\infty$
- total temperature $T_{0\infty}$
- viscosity $\mu$

### Characteristic Dimensions

- Characteristic length $l_c$ is defined by the total length.
- Normalizing area for forces & moments $A_c$ is defined by the frontal projected area.
- Characteristic pressure for a point on the surface $p_c$ is defined by the difference from the free flow pressure.
$$p_c=p_s - p_\infty$$
- Characteristic temperature for a point on the surface $T_c$ is defined by the difference from the free flow total temperature.
$$T_c = T_{0\infty} - T_s$$

### Forces & Moments

A force will be normalized by the dynamic pressure and characteristic area into a force coefficient.
$$ c_f = \frac{2}{\rho_{\infty} u_{\infty}^2 A_c}f$$

Similarly, the moments will also be normalized by the dynamic pressure, characteristic area, and characteristic moment arm $r_c$.
$$ c_m =\frac{2}{\rho_{\infty} u_{\infty}^2 A_c r_c} m$$

### Pressure Distribution

The measured surface pressures are nondimensionalized with respect to the pressure coefficient.
$$c_p=\frac{p_{\infty}}{\rho_\infty u_\infty^2}$$


### Heat Flux Distribution

The heat flux distribution across the surface is nondimensionalized with the Stanton number $\text{St}$ defined as
$$\text{St}_s = \frac{q_s}{\rho_\infty u_\infty c_p T_c}$$

## Model Validation
### Montecarlo Simulation
