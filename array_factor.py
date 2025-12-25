import numpy as np
# =========================================================
# FAST AF
# =========================================================

def compute_AF_dB_fast(w, A_scan):
    AF = w.conj() @ A_scan
    AF_abs = np.abs(AF)
    AF_abs /= AF_abs.max() + 1e-15
    return 20 * np.log10(AF_abs + 1e-15)