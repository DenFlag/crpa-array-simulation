import numpy as np

# =========================================================
# SCENARIOS
# =========================================================

def generate_scenarios(N_repeat, Max_interf,
                       theta_s_range, phi_s_range,
                       theta_i_range, phi_i_range):
    scenarios = []
    for N_interf in range(1, Max_interf + 1):
        block = []
        for _ in range(N_repeat):
            block.append({
                "theta_s": float(np.random.uniform(*theta_s_range)),
                "phi_s":   float(np.random.uniform(*phi_s_range)),
                "theta_i": np.random.uniform(*theta_i_range, N_interf),
                "phi_i":   np.random.uniform(*phi_i_range, N_interf),
            })
        scenarios.append(block)
    return scenarios