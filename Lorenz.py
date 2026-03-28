# ============================================================
# CST-305: Benchmark Project 5 - Self-Organized Criticality
# Author: Jared Walker
# Date: March 27, 2026
# Packages: numpy, scipy, matplotlib
#
# Approach:
#   Model deterministic chaos in a file system using the Lorenz
#   system of ODEs. File sizes are mapped to the x, y, z state
#   variables. The Rayleigh number r controls the transition from
#   stable -> periodic -> chaotic behavior (self-organized criticality).
#
#   Fixed parameters: sigma = 10 (Prandtl), b = 8/3 (Rayleigh ratio)
#   Variable:         r (user-supplied Rayleigh number)
#
#   File size mapping (different from given 512KB/256KB example):
#     x = file of size 128 KB  (small config/log file)
#     y = file of size 384 KB  (medium data file)
#     z = file of size 768 KB  (large media/archive file)
#
#   Three chaos regimes:
#     Non-chaotic  : r < 1      (e.g. r = 0.5)
#     Mid-chaotic  : 1 < r < 24 (e.g. r = 15)
#     Chaotic      : r >= 28    (e.g. r = 28, classic Lorenz attractor)
#
#   For each regime: 1 three-dimensional plot + 3 two-dimensional
#   plots (x vs t, y vs t, z vs t) = 4 plots x 3 regimes = 12 total.
# ============================================================

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────
SIGMA = 10          # Prandtl number (fixed)
B     = 8.0 / 3.0  # Rayleigh geometry ratio (fixed)

# File size labels for axis context (different from given 512/256 KB)
X_LABEL = 'x — File size: 128 KB (config/log)'
Y_LABEL = 'y — File size: 384 KB (data file)'
Z_LABEL = 'z — File size: 768 KB (media/archive)'

# Time span for integration
T_START = 0.0
T_END   = 50.0
N_STEPS = 10000
T_EVAL  = np.linspace(T_START, T_END, N_STEPS)

# Initial conditions: [x0, y0, z0]
IC = [1.0, 1.0, 1.0]


# ─────────────────────────────────────────────────────────────
# LORENZ SYSTEM
# ─────────────────────────────────────────────────────────────
def lorenz(t, state, sigma, r, b):
    """
    Lorenz system of ODEs modeling chaotic file system behavior.

    dx/dt = sigma * (y - x)       [rate of change of small file (128 KB)]
    dy/dt = r*x - y - x*z         [rate of change of medium file (384 KB)]
    dz/dt = x*y - b*z             [rate of change of large file (768 KB)]

    Parameters
    ----------
    sigma : Prandtl number (fluid viscosity analog — fixed at 10)
    r     : Rayleigh number (thermal forcing analog — drives chaos)
    b     : geometric factor (fixed at 8/3)
    """
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = r * x - y - x * z
    dzdt = x * y - b * z
    return [dxdt, dydt, dzdt]


def solve_lorenz(r):
    """Solve the Lorenz system for a given r value."""
    sol = solve_ivp(
        lorenz, [T_START, T_END], IC,
        args=(SIGMA, r, B),
        t_eval=T_EVAL,
        method='RK45',
        rtol=1e-9, atol=1e-12
    )
    return sol.t, sol.y[0], sol.y[1], sol.y[2]


# ─────────────────────────────────────────────────────────────
# PLOTTING FUNCTIONS
# ─────────────────────────────────────────────────────────────
def plot_3d(ax, x, y, z, r, label, color):
    """
    3D phase-space plot of the Lorenz attractor.
    Each point (x,y,z) represents the simultaneous file sizes
    of all three file types at one moment in time.
    """
    ax.plot(x, y, z, lw=0.5, color=color, alpha=0.85)
    ax.set_xlabel('x (128 KB)', fontsize=8, labelpad=2)
    ax.set_ylabel('y (384 KB)', fontsize=8, labelpad=2)
    ax.set_zlabel('z (768 KB)', fontsize=8, labelpad=2)
    ax.set_title(f'3D Phase Space\n{label}  (r = {r})', fontsize=9, fontweight='bold')
    ax.tick_params(labelsize=7)


def plot_2d(ax, t, val, ylabel, r, label, color, var_name):
    """
    2D time-series plot: file size variable vs time.
    Shows how a single file size evolves as the system runs.
    """
    ax.plot(t, val, lw=0.6, color=color, alpha=0.9)
    ax.set_xlabel('Time (s)', fontsize=8)
    ax.set_ylabel(ylabel, fontsize=7.5)
    ax.set_title(f'{var_name}(t)  —  {label}  (r = {r})', fontsize=9, fontweight='bold')
    ax.tick_params(labelsize=7)
    ax.grid(True, alpha=0.25)


def make_figure(r, label, color, fig_num):
    """
    Generate all 4 plots for one r value:
      - 1 x 3D phase-space plot
      - 3 x 2D time-series (x, y, z vs t)
    """
    print(f'  Solving Lorenz system for r = {r}  ({label})...')
    t, x, y, z = solve_lorenz(r)

    fig = plt.figure(figsize=(14, 10))
    fig.suptitle(
        f'Lorenz File System Model — {label}\n'
        f'σ = {SIGMA},  b = {B:.4f},  r = {r}   |   '
        f'x = 128 KB,  y = 384 KB,  z = 768 KB',
        fontsize=11, fontweight='bold', y=1.01
    )

    # ── Plot 1: 3D attractor ──────────────────────────────────
    ax3d = fig.add_subplot(2, 2, 1, projection='3d')
    plot_3d(ax3d, x, y, z, r, label, color)

    # ── Plot 2: x(t) ─────────────────────────────────────────
    ax_x = fig.add_subplot(2, 2, 2)
    plot_2d(ax_x, t, x, 'x — 128 KB file (KB)', r, label, color, 'x')

    # ── Plot 3: y(t) ─────────────────────────────────────────
    ax_y = fig.add_subplot(2, 2, 3)
    plot_2d(ax_y, t, y, 'y — 384 KB file (KB)', r, label, color, 'y')

    # ── Plot 4: z(t) ─────────────────────────────────────────
    ax_z = fig.add_subplot(2, 2, 4)
    plot_2d(ax_z, t, z, 'z — 768 KB file (KB)', r, label, color, 'z')

    plt.tight_layout()
    fname = f'lorenz_figure{fig_num}_{label.lower().replace(" ", "_")}_r{r}.png'
    plt.savefig(fname, dpi=150, bbox_inches='tight')
    print(f'    Saved: {fname}')
    return fig, fname


# ─────────────────────────────────────────────────────────────
# USER INPUT FOR r VALUES
# ─────────────────────────────────────────────────────────────
def get_r_values():
    """
    Prompt user to enter r for each chaos regime, or press Enter
    to use the default values.

    Chaos thresholds for Lorenz system:
      r < 1       → all trajectories decay to origin (non-chaotic)
      1 < r < 24  → trajectories spiral to fixed points (mid-chaotic)
      r >= 28     → butterfly attractor, deterministic chaos
    """
    print('\n' + '='*60)
    print('  Lorenz File System — Self-Organized Criticality')
    print('='*60)
    print(f'  Fixed: sigma = {SIGMA},  b = {B:.4f}')
    print('  File mapping:  x = 128 KB | y = 384 KB | z = 768 KB')
    print('-'*60)
    print('  Enter Rayleigh number (r) for each regime.')
    print('  Press Enter to use the default value shown.')
    print('-'*60)

    def ask(prompt, default):
        raw = input(prompt).strip()
        if raw == '':
            return default
        try:
            val = float(raw)
            return val
        except ValueError:
            print(f'    Invalid input — using default {default}')
            return default

    r_non  = ask(f'  Non-chaotic   r  [default = 0.5,  range r < 1    ]: ', 0.5)
    r_mid  = ask(f'  Mid-chaotic   r  [default = 15.0, range 1 < r < 24]: ', 15.0)
    r_chaos= ask(f'  Chaotic       r  [default = 28.0, range r >= 28   ]: ', 28.0)

    print(f'\n  Using:  r_non = {r_non},  r_mid = {r_mid},  r_chaos = {r_chaos}')
    print('='*60 + '\n')
    return r_non, r_mid, r_chaos


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    # Get r values from user
    r_non, r_mid, r_chaos = get_r_values()

    regimes = [
        (r_non,   'Non-Chaotic',  '#3266ad', 1),
        (r_mid,   'Mid-Chaotic',  '#1D9E75', 2),
        (r_chaos, 'Chaotic',      '#D85A30', 3),
    ]

    saved_files = []
    for r, label, color, fig_num in regimes:
        fig, fname = make_figure(r, label, color, fig_num)
        saved_files.append(fname)

    print('\n' + '='*60)
    print('  All 12 plots generated (4 per regime x 3 regimes).')
    print('  Saved files:')
    for f in saved_files:
        print(f'    {f}')
    print('='*60)

    plt.show()


if __name__ == '__main__':
    main()
