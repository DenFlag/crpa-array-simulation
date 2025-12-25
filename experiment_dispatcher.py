from simulation_core import *
from visualization import *

def run_experiment(mode, arrays_used, scenarios, cfg, k, N_interf_min):
    """
    Универсальный диспетчер экспериментов.
    """

    # ---------- 1. Квантование фазы ----------
    if mode == "quantization":

        nBits_grid = cfg["quantization"]["nBits_grid"]

        results = [
            run_simulation(array, scenarios, k, nBits_grid)
            for array in arrays_used
        ]

        visualize_results(results, nBits_grid, N_interf_min)
        visualize_SIR(results, nBits_grid, N_interf_min)



    # ---------- 2. Шаг решётки ----------
    elif mode == "spacing":

        d_lambda_grid = cfg["spacing"]["d_lambda_grid"]
        nBits_fixed = cfg["quantization"]["nBits_fixed"]

        results_vs_spacing = []

        for array in arrays_used:
            Signal, Supp, SIR = run_vs_spacing(
                base_array=array,
                d_lambda_grid=d_lambda_grid,
                scenarios=scenarios,
                k=k,
                nBits_fixed=nBits_fixed
            )

            results_vs_spacing.append({
                "array": array,
                "Signal": Signal,
                "Suppression": Supp,
                "SIR": SIR
            })

        visualize_levels_vs_spacing_multi(
            d_lambda_grid,
            results_vs_spacing,
            N_interf_min
        )
        visualize_SIR_vs_spacing_multi(
            d_lambda_grid,
            results_vs_spacing,
            N_interf_min
        )

    # ---------- 3. Ошибка положения ----------
    elif mode == "position_error":

        sigma_pos_grid = cfg["position_error"]["sigma_pos_grid"]
        nBits_fixed = cfg["quantization"]["nBits_fixed"]

        results_vs_pos = []

        for array in arrays_used:
            Signal, Supp, SIR = run_vs_position_error(
                base_array=array,
                sigma_pos_grid=sigma_pos_grid,
                scenarios=scenarios,
                k=k,
                nBits_fixed=nBits_fixed
            )

            results_vs_pos.append({
                "array": array,
                "Signal": Signal,
                "Suppression": Supp,
                "SIR": SIR
            })

        visualize_levels_vs_position_error_multi(
            sigma_pos_grid,
            results_vs_pos,
            N_interf_min
        )
        visualize_SIR_vs_position_error_multi(
            sigma_pos_grid,
            results_vs_pos,
            N_interf_min
        )

    else:
        raise ValueError(f"Unknown experiment mode: {mode}")

def get_default_grids_for_mode(mode):
    if mode == "quantization":
        return np.arange(1, 15), "Phase bits"

    elif mode == "spacing":
        return np.array([0.1, 0.2, 0.3, 0.4, 0.5]), "d / λ"

    elif mode == "position_error":
        return np.arange(0, 0.6, 0.1), "σ position (λ)"

    else:
        raise ValueError("Unknown mode")