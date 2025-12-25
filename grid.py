import numpy as np


# =========================================================
# GRID
# =========================================================

def get_scan_grid(theta_min, theta_max, phi_min, phi_max, theta_step, phi_step):
    theta = np.arange(theta_min, theta_max + theta_step, theta_step)
    phi   = np.arange(phi_min, phi_max + phi_step, phi_step)
    return np.meshgrid(theta, phi, indexing="ij")
