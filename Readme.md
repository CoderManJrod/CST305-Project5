# Project 5 — Self-Organized Criticality: Lorenz File System Model

**Course:** CST-305: Principles of Modeling and Simulation  
**Author:** Jared Walker 
**Semester/Date:** Spring 2026/March 29, 2026
**University:** Grand Canyon University

---

## Overview

This project models the deterministically chaotic behavior of a file system using the Lorenz system of ODEs. As files are repeatedly saved and deleted, fragmentation grows until the system approaches a critical threshold — a phenomenon captured by the Lorenz attractor as it transitions from stable to chaotic behavior.

File sizes are mapped to the Lorenz state variables:
- `x` = 128 KB file (config/log)
- `y` = 384 KB file (data file)
- `z` = 768 KB file (media/archive)

Fixed parameters: **σ = 10** (Prandtl), **b = 8/3** (geometry ratio)  
Variable parameter: **r** (Rayleigh number — user supplied at runtime)

---

## Requirements

- Python 3.8+
- numpy
- scipy
- matplotlib

---

## Installation

```bash
pip install numpy scipy matplotlib
```

---

## Running the Program

```bash
python3 lorenz_soc.py
```

The program prompts you to enter `r` for each of the three chaos regimes:

```
Non-chaotic   r  [default = 0.5,  range r < 1    ]:
Mid-chaotic   r  [default = 15.0, range 1 < r < 24]:
Chaotic       r  [default = 28.0, range r >= 28   ]:
```

Press **Enter** to accept the default, or type your own value.

---

## Output

For each of the 3 regimes, 4 plots are generated (12 total):

| Plot | Description |
|------|-------------|
| 3D phase space | Lorenz attractor trajectory in (x, y, z) |
| x(t) | 128 KB file size variable vs time |
| y(t) | 384 KB file size variable vs time |
| z(t) | 768 KB file size variable vs time |

Figures are saved as PNG files and displayed on screen.

---

## Chaos Regimes

| Regime | r value | Behavior |
|--------|---------|----------|
| Non-chaotic | r < 1 | All trajectories decay to origin (stable) |
| Mid-chaotic | 1 < r < 24 | Trajectories spiral to fixed-point attractors |
| Chaotic | r ≥ 28 | Butterfly attractor — deterministic chaos (SOC) |

---

## References

- Lorenz, E. N. (1963). Deterministic nonperiodic flow. *Journal of Atmospheric Sciences, 20*(2), 130–141.
- Strogatz, S. H. (2015). *Nonlinear Dynamics and Chaos* (2nd ed.). Westview Press.
- SciPy Documentation: https://docs.scipy.org/doc/scipy/reference/integrate.html
