# Aerodynamic Modeling and Validation
University of Virginia - HyperLARP

University Consortium of Applied Hypersonics undergraduate design competition.

---
## Objective
To produce a surrogate model for the aerodynamic performance of the UVA HyperLARP hypersonic glider design, validated by the experimental work done in collaboration with the CUBRC hypersonic research facility.

---
## Aerodynamic Model
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
---

## Model Verification and Refinement

For a given output variable $f$, record the following to estimate that variable's uncertainty.

### Numerical Uncertainty
#### (i) Mesh Adaptation convergence metrics.
Define the discritization error
$$\epsilon_{disc} \approx |f_k - f_{k-1}|$$
Where $f_k$ is the final converged value and $f_{k-1}$ is the final value prior to the next most recent mesh adaptation step.

#### (ii) Adjoint-based error estimation.
For each available output variable, record the adjoint estimated error from Ansys Fluent's interface.
$$\epsilon_j \approx \sum_i{R_i \cdot\psi_i}$$

(This is the gold standard for CFD UQ in aerospace engineering)

Merge these two error into the discritization variance
$$\sigma_{disc} = \text{max}(|\epsilon_j|, |\epsilon_{disc}|)$$

#### (iii) Solver convergence uncertainty.
Repeat the same case with:
- different CFL schedules
- different initializations
- slightly perturbed tolerances

Estimate
$$\sigma^2_{solver} = \text{Var}[f_{runs}]$$

### Model-Form Uncertainty
#### (i) Multi-model ensemble
Run variations of:
- turbulence models
- wall models

Then
$$\sigma^2_{model} = \text{Var}[f_{models}]$$

#### (ii) Parameter perturbation
Perturb uncertain parameters:
- Transition onset
- Turbulence coefficients
- Wall temperature

### Total CFD uncertainty
The pointwise uncertainty for each CFD sample can be found by:
$$\sigma^2_{CFD} = \sigma^2_{disc} + \sigma^2_{solver} + \sigma^2_{model}$$

---
## Surrogate Modeling and Adaptive Sampling
Instead of treating $y_i=f_i(x)$ as exact, allow a zero-mean disturbance.
$$y_i=f_i(x) + \epsilon_i, \quad \epsilon \sim \mathcal{N}(0, \sigma_{i, CFD}^2)$$

Following this,
$$
\text{E}[y_i] = E[f_i(x)] +0
$$
$$
\text{Var}[y_i] = \sigma^2_{i, model} + \sigma_{i, CFD}^2
$$