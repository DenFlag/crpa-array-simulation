import matplotlib.pyplot as plt
from geometry import get_array_positions


def array_label(array):
    geom = array["geometry"]

    if geom == "rectangular":
        return f'{array["Nx"]}x{array["Ny"]}, d={array["d_lambda"]}λ'

    elif geom == "triangular":
        return f'Triangular, N_side={array["params"]["N_side"]}, d={array["params"]["d_lambda"]}λ'

    elif geom == "circular":
        return f'Circular, rings={array["params"]["N_rings"]}, dr={array["params"]["dr_lambda"]}λ'

    else:
        return 'Unknown array'

def visualize_results(results, nBits_grid, N_interf_min):
    plt.figure(figsize=(14, 6))
    plt.grid(True)

    for res in results:
        for idx in range(res["Suppression"].shape[0]):
            N_real = idx + N_interf_min

            plt.plot(nBits_grid, res["Signal"][idx, :], "--",
                     label=f'{array_label(res["Array"])}, {N_real} помех (Signal)')
            plt.plot(nBits_grid, res["Suppression"][idx, :], "-",
                     label=f'{array_label(res["Array"])}, {N_real} помех (Suppression)')

    plt.xlabel("Битность фазового квантования")
    plt.ylabel("Уровень ДН, дБ")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.show()

def visualize_SIR(results, nBits_grid, N_interf_min):
    plt.figure(figsize=(12, 6))
    plt.grid(True)

    for res in results:
        for idx in range(res["Signal"].shape[0]):
            N_real = idx + N_interf_min
            SIR = res["Signal"][idx, :] - res["Suppression"][idx, :]

            plt.plot(nBits_grid, SIR,
                     label=f'{array_label(res["Array"])}, {N_real} помех'
)

    plt.xlabel("Битность фазового квантования")
    plt.ylabel("SIR, дБ")
    plt.title("Отношение сигнал–помеха")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.show()

def visualize_SIR_delta_between_spacings(results, nBits_grid, N_interf_min):
    """
    Третий график:
    ΔSIR = SIR(d_small) - SIR(d_large)

    results[0] → d = 0.5λ
    results[1] → d = 0.1λ
    """

    assert len(results) == 2, "Нужно ровно две решётки для сравнения шага"

    res_large = results[0]   # d = 0.5λ
    res_small = results[1]   # d = 0.1λ

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    for idx in range(res_large["Signal"].shape[0]):
        N_real = idx + N_interf_min

        SIR_large = res_large["Signal"][idx, :] - res_large["Suppression"][idx, :]
        SIR_small = res_small["Signal"][idx, :] - res_small["Suppression"][idx, :]

        delta_SIR = SIR_small - SIR_large

        plt.plot(
            nBits_grid,
            delta_SIR,
            linewidth=2,
            label=f'{N_real} помех'
        )

    plt.axhline(0, color='k', linestyle='--', linewidth=1)

    plt.xlabel("Битность фазового квантования")
    plt.ylabel("ΔSIR = SIR(d=0.1λ) − SIR(d=0.5λ), дБ")
    plt.title("Влияние шага решётки на отношение сигнал–помеха")
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.show()

def visualize_vs_spacing(d_lambda_grid, Signal, Supp, array, N_interf_min):
    plt.figure(figsize=(11, 6))
    plt.grid(True)

    for idx in range(Signal.shape[0]):
        N_real = idx + N_interf_min

        plt.plot(d_lambda_grid, Signal[idx, :],
                 "-o", label=f"Signal, {N_real} помех")
        plt.plot(d_lambda_grid, Supp[idx, :],
                 "--s", label=f"Suppression, {N_real} помех")

    plt.xlabel("Шаг решётки d / λ")
    plt.ylabel("Уровень ДН, дБ")
    plt.title(f"Зависимость от шага — {array_label(array)}")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.show()

def visualize_SIR_vs_spacing(d_lambda_grid, SIR, array, N_interf_min):
    plt.figure(figsize=(11, 6))
    plt.grid(True)

    for idx in range(SIR.shape[0]):
        N_real = idx + N_interf_min
        plt.plot(d_lambda_grid, SIR[idx, :],
                 linewidth=2,
                 label=f"{N_real} помех")

    plt.xlabel("Шаг решётки d / λ")
    plt.ylabel("SIR, дБ")
    plt.title(f"SIR vs spacing — {array_label(array)}")
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.show()




def visualize_SIR_vs_spacing_multi(d_lambda_grid, results, N_interf_min):
    """
    Отображает SIR vs шаг решётки
    одновременно для нескольких антенных решёток
    """

    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.grid(True)

    for res in results:
        array = res["array"]
        geom = array["geometry"]

        for idx in range(res["SIR"].shape[0]):
            N_real = idx + N_interf_min

            plt.plot(
                d_lambda_grid,
                res["SIR"][idx, :],
                linewidth=2,
                label=f'{geom}, {N_real} помех'
            )

    plt.xlabel("Шаг решётки, λ")
    plt.ylabel("SIR, дБ")
    plt.title("SIR vs шаг антенной решётки")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.show()



def visualize_levels_vs_spacing_multi(d_lambda_grid, results, N_interf_min):
    """
    Отображает:
      - уровень сигнала
      - средний уровень помех
    как функцию шага решётки
    для нескольких антенных решёток
    """

    import matplotlib.pyplot as plt

    plt.figure(figsize=(14, 6))
    plt.grid(True)

    for res in results:
        array = res["array"]
        geom = array["geometry"]

        for idx in range(res["Signal"].shape[0]):
            N_real = idx + N_interf_min

            plt.plot(
                d_lambda_grid,
                res["Signal"][idx, :],
                linestyle="--",
                linewidth=2,
                label=f'{geom}, {N_real} помех (Signal)'
            )

            plt.plot(
                d_lambda_grid,
                res["Suppression"][idx, :],
                linestyle="-",
                linewidth=2,
                label=f'{geom}, {N_real} помех (Interference)'
            )

    plt.xlabel("Шаг решётки, λ")
    plt.ylabel("Уровень ДН, дБ")
    plt.title("Уровни сигнала и помех vs шаг решётки")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.show()

def visualize_levels_vs_position_error_multi(
    sigma_pos_grid,
    results_vs_pos,
    N_interf_min
):
    """
    Визуализация уровней сигнала и помех
    в зависимости от СКО ошибки положения элементов.

    sigma_pos_grid : array of σ_pos (в долях λ)
    results_vs_pos : список словарей:
        {
            "array": {...},
            "Signal": (N_interf, N_sigma),
            "Suppression": (N_interf, N_sigma)
        }
    """

    plt.figure(figsize=(14, 6))
    plt.grid(True)

    for res in results_vs_pos:

        array = res["array"]
        Signal = res["Signal"]
        Supp   = res["Suppression"]

        # читаемое имя решётки
        geom = array["geometry"]
        if geom == "rectangular":
            label_base = f"Rect {array['Nx']}×{array['Ny']}"
        elif geom == "triangular":
            label_base = f"Tri N={array['params']['N_side']}"
        elif geom == "circular":
            label_base = f"Circ R={array['params']['N_rings']}"
        else:
            label_base = "Unknown"

        for idx in range(Signal.shape[0]):
            N_real = idx + N_interf_min

            plt.plot(
                sigma_pos_grid,
                Signal[idx, :],
                linestyle="--",
                linewidth=2,
                label=f"{label_base}, {N_real} помех (Signal)"
            )

            plt.plot(
                sigma_pos_grid,
                Supp[idx, :],
                linestyle="-",
                linewidth=2,
                label=f"{label_base}, {N_real} помех (Interference)"
            )

    plt.xlabel("СКО ошибки положения элементов, λ")
    plt.ylabel("Уровень ДН, дБ")
    plt.title("Влияние ошибок положения элементов на уровни сигнала и помех")
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.show()

def visualize_SIR_vs_position_error_multi(
    sigma_pos_grid,
    results_vs_pos,
    N_interf_min
):
    plt.figure(figsize=(12, 6))
    plt.grid(True)

    for res in results_vs_pos:
        SIR = res["SIR"]   # ← КЛЮЧЕВО

        array = res["array"]
        geom = array["geometry"]

        if geom == "rectangular":
            label_base = f"Rect {array['Nx']}×{array['Ny']}"
        elif geom == "triangular":
            label_base = f"Tri N={array['params']['N_side']}"
        elif geom == "circular":
            label_base = f"Circ R={array['params']['N_rings']}"
        else:
            label_base = "Unknown"

        for idx in range(SIR.shape[0]):
            N_real = idx + N_interf_min

            plt.plot(
                sigma_pos_grid,
                SIR[idx, :],
                linewidth=2,
                marker="o",
                label=f"{label_base}, {N_real} помех"
            )

    plt.xlabel("СКО ошибки положения элементов, λ")
    plt.ylabel("SIR = Signal − Interference, дБ")
    plt.title("Влияние ошибок положения элементов на SIR")
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.show()


def plot_array_geometry(ax, array, title_suffix=""):
    ax.clear()

    positions = get_array_positions(array)

    x = positions[:, 0]
    y = positions[:, 1]

    ax.scatter(x, y, s=80, c="tab:blue", edgecolors="k")



    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x / λ")
    ax.set_ylabel("y / λ")
    ax.grid(True)

    ax.set_title(f"Array geometry {title_suffix}")


def plot_SIR_mean_std(x, sir_mean, sir_std, label):
    plt.plot(x, sir_mean, linewidth=2, label=label)
    plt.fill_between(x, sir_mean - sir_std, sir_mean + sir_std, alpha=0.2)
def plot_SIR_percentile_band(x, sir_mean, p10, p90, label):
    plt.plot(x, sir_mean, linewidth=2, label=label)
    plt.fill_between(x, p10, p90, alpha=0.2)


def make_label(kind, n_interf, geometry=None):
    """
    kind: "Signal", "Interf", "SIR"
    n_interf: число помех (int)
    geometry: опционально ("rectangular", ...)
    """
    base = f"{kind}, N={n_interf}"
    if geometry is not None:
        base = f"{base}, {geometry}"
    return base