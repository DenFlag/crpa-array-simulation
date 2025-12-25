import numpy as np

# =========================================================
# STEERING
# =========================================================

def steering_vector(theta_deg, phi_deg, positions, k):
    theta = np.deg2rad(theta_deg)
    phi   = np.deg2rad(phi_deg)

    phase = (
        positions[:, 0] * np.sin(theta) * np.cos(phi) +
        positions[:, 1] * np.sin(theta) * np.sin(phi)
    )
    return np.exp(1j * k * phase)


def steering_matrix(TH_deg, PH_deg, positions, k):
    TH = np.deg2rad(TH_deg.ravel())
    PH = np.deg2rad(PH_deg.ravel())

    x = positions[:, 0][:, None]
    y = positions[:, 1][:, None]

    phase = (
        x * np.sin(TH) * np.cos(PH) +
        y * np.sin(TH) * np.sin(PH)
    )
    return np.exp(1j * k * phase)