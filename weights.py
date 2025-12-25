import numpy as np
from steering import steering_vector

# =========================================================
# WEIGHTS
# =========================================================

def get_weights(theta_s, phi_s, theta_i, phi_i, positions, k):
    a_s = steering_vector(theta_s, phi_s, positions, k)

    A_i = np.column_stack([
        steering_vector(theta_i[i], phi_i[i], positions, k)
        for i in range(len(theta_i))
    ])

    A = np.column_stack((a_s, A_i))
    b = np.concatenate(([1.0], np.zeros(len(theta_i))))

    w = np.linalg.pinv(A.conj().T) @ b
    return w / np.linalg.norm(w)


# =========================================================
# PHASE QUANTIZATION
# =========================================================

def quantize_weights_phase_only(w, nPhaseBits):
    amp = np.abs(w)
    phase = np.angle(w)

    nLevels = 2 ** int(nPhaseBits)
    phase_step = 2 * np.pi / nLevels

    phase_q = np.round(phase / phase_step) * phase_step
    wq = amp * np.exp(1j * phase_q)

    return wq / np.linalg.norm(wq)
