import numpy as np

from geometry import get_array_positions, apply_position_error
from steering import steering_matrix
from weights import get_weights, quantize_weights_phase_only
from array_factor import compute_AF_dB_fast
from grid import get_scan_grid


# =========================================================
# SINGLE SCENARIO
# =========================================================

def compute_for_angles(theta_s, phi_s, theta_i, phi_i,
                       array, k,
                       TH_flat, PH_flat, A_scan,
                       nBits_grid):

    positions = get_array_positions(array)
    w = get_weights(theta_s, phi_s, theta_i, phi_i, positions, k)

    N_i = len(theta_i)
    N_bits = len(nBits_grid)

    Supp = np.zeros((N_i, N_bits))
    Sig  = np.zeros(N_bits)

    idx_s = np.argmin(np.abs(TH_flat - theta_s) + np.abs(PH_flat - phi_s))
    idx_i = [
        np.argmin(np.abs(TH_flat - theta_i[m]) + np.abs(PH_flat - phi_i[m]))
        for m in range(N_i)
    ]

    for n, nBits in enumerate(nBits_grid):
        wq = quantize_weights_phase_only(w, nBits)
        AF_dB = compute_AF_dB_fast(wq, A_scan)

        Sig[n] = AF_dB[idx_s]
        for m in range(N_i):
            Supp[m, n] = AF_dB[idx_i[m]]

    return Supp, Sig

# =========================================================
# RUN SIMULATION (WITH INTERFERENCE RANGE)
# =========================================================

def run_simulation(array, scenarios, k, nBits_grid):

    TH_deg, PH_deg = get_scan_grid(0, 90, 0, 360, 1, 1)
    TH_flat = TH_deg.ravel()
    PH_flat = PH_deg.ravel()

    positions = get_array_positions(array)
    A_scan = steering_matrix(TH_deg, PH_deg, positions, k)

    Max_interf = len(scenarios)
    N_bits = len(nBits_grid)
    N_repeat = len(scenarios[0])

    Supp_all = np.zeros((Max_interf, N_bits))
    Sig_all  = np.zeros((Max_interf, N_bits))

    for idx in range(Max_interf):
        N_real_interf = scenarios[idx][0]["theta_i"].size
        Supp_acc = np.zeros((N_real_interf, N_bits))
        Sig_acc  = np.zeros(N_bits)

        for r in range(N_repeat):
            sc = scenarios[idx][r]

            Supp_tmp, Sig_tmp = compute_for_angles(
                sc["theta_s"], sc["phi_s"],
                sc["theta_i"], sc["phi_i"],
                array, k,
                TH_flat, PH_flat, A_scan,
                nBits_grid
            )

            Supp_acc += Supp_tmp
            Sig_acc  += Sig_tmp

        Supp_all[idx, :] = np.mean(Supp_acc / N_repeat, axis=0)
        Sig_all[idx, :]  = Sig_acc / N_repeat

    return {"Suppression": Supp_all, "Signal": Sig_all, "Array": array}

# Ран с учетом ошибки позиции

def run_vs_position_error(
    base_array,
    sigma_pos_grid,
    scenarios,
    k,
    nBits_fixed
):
    """
    Физически корректный анализ ошибок положения элементов.

    ВАЖНО:
    - веса считаются по НОМИНАЛЬНОЙ геометрии
    - ДН формируется по РЕАЛЬНОЙ (ошибочной) геометрии
    """

    Max_interf = len(scenarios)
    N_repeat = len(scenarios[0])
    N_sigma = len(sigma_pos_grid)

    Signal = np.zeros((Max_interf, N_sigma))
    Supp   = np.zeros((Max_interf, N_sigma))
    SIR    = np.zeros((Max_interf, N_sigma))

    # сетка сканирования
    TH_deg, PH_deg = get_scan_grid(0, 90, 0, 360, 1, 1)
    TH_flat = TH_deg.ravel()
    PH_flat = PH_deg.ravel()

    # НОМИНАЛЬНЫЕ позиции (известны алгоритму)
    positions_nom = get_array_positions(base_array)

    for s_idx, sigma_pos in enumerate(sigma_pos_grid):

        Sig_acc  = np.zeros(Max_interf)
        Supp_acc = np.zeros(Max_interf)

        for idx in range(Max_interf):
            for r in range(N_repeat):

                sc = scenarios[idx][r]

                # --- реальные позиции элементов ---
                positions_real = apply_position_error(
                    positions_nom,
                    sigma_pos
                )

                # --- веса считаем ПО НОМИНАЛЬНОЙ геометрии ---
                w = get_weights(
                    sc["theta_s"], sc["phi_s"],
                    sc["theta_i"], sc["phi_i"],
                    positions_nom,
                    k
                )

                # --- ДН формируется ПО РЕАЛЬНОЙ геометрии ---
                A_scan = steering_matrix(
                    TH_deg, PH_deg, positions_real, k
                )

                AF_dB = compute_AF_dB_fast(
                    quantize_weights_phase_only(w, nBits_fixed),
                    A_scan
                )

                # --- направления ---
                idx_s = np.argmin(
                    np.abs(TH_flat - sc["theta_s"]) +
                    np.abs(PH_flat - sc["phi_s"])
                )

                idx_i = [
                    np.argmin(
                        np.abs(TH_flat - sc["theta_i"][m]) +
                        np.abs(PH_flat - sc["phi_i"][m])
                    )
                    for m in range(len(sc["theta_i"]))
                ]

                Sig_acc[idx]  += AF_dB[idx_s]
                Supp_acc[idx] += np.mean([AF_dB[i] for i in idx_i])

        Signal[:, s_idx] = Sig_acc / N_repeat
        Supp[:, s_idx]   = Supp_acc / N_repeat
        SIR[:, s_idx]    = Signal[:, s_idx] - Supp[:, s_idx]

    return Signal, Supp, SIR

def run_vs_spacing(
    base_array,
    d_lambda_grid,
    scenarios,
    k,
    nBits_fixed
):
    """
    Честный расчёт:
    Signal / Suppression / SIR как функции d
    ОТДЕЛЬНО для каждого числа помех
    """

    N_interf = len(scenarios)
    N_d = len(d_lambda_grid)

    Signal = np.zeros((N_interf, N_d))
    Supp   = np.zeros((N_interf, N_d))

    for j, d in enumerate(d_lambda_grid):

        # модифицируем шаг решётки
        array = dict(base_array)

        if array["geometry"] == "rectangular":
            array["d_lambda"] = d

        elif array["geometry"] == "triangular":
            array["params"] = dict(array["params"])
            array["params"]["d_lambda"] = d

        elif array["geometry"] == "circular":
            array["params"] = dict(array["params"])
            array["params"]["dr_lambda"] = d

        # запускаем моделирование (битность фиксирована!)
        res = run_simulation(array, scenarios, k, np.array([nBits_fixed]))

        # res["Signal"].shape      → (N_interf, 1)
        # res["Suppression"].shape → (N_interf, 1)

        Signal[:, j] = res["Signal"][:, 0]
        Supp[:, j]   = res["Suppression"][:, 0]

    SIR = Signal - Supp
    return Signal, Supp, SIR