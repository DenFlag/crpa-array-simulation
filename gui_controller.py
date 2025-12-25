# gui_controller.py

import numpy as np

from parsing import (
    parse_nBits_grid,
    parse_d_lambda_grid,
    parse_sigma_grid
)

from simulation_core import (
    run_simulation,
    run_vs_spacing,
    run_vs_position_error
)

from visualization import plot_array_geometry
from gui_helpers import clear_axes


from gui_helpers import build_array_from_gui
from scenarios import generate_scenarios


def run_gui_experiment(
    mode,
    geometry,
    d_lambda_single,
    d_lambda_grid_text,
    sigma_grid_text,
    nBits_grid_text,
    nBits,
    gui,
    k,
    N_interf_min,
    ax_array,
    ax_levels,
    ax_sir,
    canvas
):
    # --- СЦЕНАРИИ ЗДЕСЬ ---
    scenarios = build_scenarios_from_gui(gui)


    clear_axes(ax_levels, ax_sir)
    # -------------------------------
    # Geometry visualization
    # -------------------------------

    array_for_plot = build_array_from_gui(
        geometry=geometry,
        d_lambda=d_lambda_single,
        gui=gui
    )

    if mode == "spacing":
        plot_array_geometry(
            ax_array,
            array_for_plot,
            title_suffix=f"(displayed d = {d_lambda_single:.2f} λ)"
        )
    else:
        plot_array_geometry(
            ax_array,
            array_for_plot
        )

    # ===============================
    # QUANTIZATION
    # ===============================
    if mode == "quantization":

        array = build_array_from_gui(
            geometry,
            d_lambda_single,
            gui
        )

        nBits_grid = parse_nBits_grid(nBits_grid_text)

        res = run_simulation(
            array=array,
            scenarios=scenarios,
            k=k,
            nBits_grid=nBits_grid
        )

        for i in range(res["Signal"].shape[0]):
            N_int = N_interf_min + i

            ax_levels.plot(
                nBits_grid,
                res["Signal"][i],
                "--o",
                label=f"Signal, N = {N_int}"
            )

            ax_levels.plot(
                nBits_grid,
                res["Suppression"][i],
                "-s",
                label=f"Interference, N = {N_int}"
            )

            ax_sir.plot(
                nBits_grid,
                res["Signal"][i] - res["Suppression"][i],
                "-o",
                label=f"SIR, N = {N_int}"
            )

        ax_levels.set_xlabel("Phase quantization bits")
        ax_levels.set_ylabel("Level, dB")
        ax_sir.set_xlabel("Phase quantization bits")
        ax_sir.set_ylabel("SIR, dB")

        ax_levels.set_title(
            "Signal and interference levels vs phase quantization"
        )
        ax_sir.set_title(
            "SIR vs phase quantization"
        )






    # ===============================
    # SPACING (GRID FROM GUI)
    # ===============================
    elif mode == "spacing":

        d_lambda_grid = parse_d_lambda_grid(d_lambda_grid_text)
        array = build_array_from_gui(
            geometry=geometry,
            d_lambda=0.5,
            gui=gui
        )

        Signal, Supp, SIR = run_vs_spacing(
            base_array=array,
            d_lambda_grid=d_lambda_grid,
            scenarios=scenarios,
            k=k,
            nBits_fixed=nBits
        )

        for i in range(SIR.shape[0]):
            N_int = N_interf_min + i


            ax_levels.plot(
                d_lambda_grid,
                Signal[i],
                "--o",
                label=f"Signal, N = {N_int} interferers"
            )

            ax_levels.plot(
                d_lambda_grid,
                Supp[i],
                "-s",
                label=f"Interference, N = {N_int} interferers"
            )

            ax_sir.plot(
                d_lambda_grid,
                SIR[i],
                "-o",
                label=f"SIR, N = {N_int} interferers"
            )

        ax_sir.set_xlabel("d / λ")
        ax_levels.set_xlabel("Inter-element spacing d / λ")
        ax_levels.set_ylabel("Level, dB")

        ax_sir.set_xlabel("Inter-element spacing d / λ")
        ax_sir.set_ylabel("SIR, dB")

        ax_levels.set_title(
            "Influence of array spacing on signal and interference levels"
        )
        ax_sir.set_title(
            "SIR vs inter-element spacing"
        )



    # ===============================
    # POSITION ERROR
    # ===============================
    elif mode == "position_error":

        array = build_array_from_gui(
            geometry,
            d_lambda_single,
            gui
        )

        sigma_grid = parse_sigma_grid(sigma_grid_text)

        Signal, Supp, SIR = run_vs_position_error(
            base_array=array,
            sigma_pos_grid=sigma_grid,
            scenarios=scenarios,
            k=k,
            nBits_fixed=nBits
        )

        for i in range(SIR.shape[0]):
            N_int = N_interf_min + i


            ax_levels.plot(
                sigma_grid,
                Signal[i],
                "--o",
                label=f"Signal, N = {N_int} interferers"
            )

            ax_levels.plot(
                sigma_grid,
                Supp[i],
                "-s",
                label=f"Interference, N = {N_int} interferers"
            )

            ax_sir.plot(
                sigma_grid,
                SIR[i],
                "-o",
                label=f"SIR, N = {N_int} interferers"
            )

        ax_levels.set_xlabel("RMS position error σ / λ")
        ax_levels.set_ylabel("Level, dB")
        ax_sir.set_xlabel("RMS position error σ / λ")
        ax_sir.set_ylabel("SIR, dB")

        ax_levels.set_title(
            "Signal and interference levels vs element position error"
        )
        ax_sir.set_title(
            "SIR degradation due to element position errors"
        )


    else:
        raise ValueError("Unknown mode")

    ax_levels.legend(fontsize=8)
    ax_sir.legend(fontsize=8)
    canvas.draw()

    ax_levels.relim()
    ax_levels.autoscale()
    ax_sir.relim()
    ax_sir.autoscale()



def build_scenarios_from_gui(gui):
    """
    Формирует сценарии на основе параметров GUI
    """

    theta_s_range = (10, 80)
    phi_s_range   = (0, 360)
    theta_i_range = (0, 90)
    phi_i_range   = (0, 360)

    N_repeat = gui["Nrepeat"].get()
    N_interf_min = gui["Ninterf_min"].get()
    N_interf_max = gui["Ninterf_max"].get()

    # защита от ошибок пользователя
    if N_interf_min < 1:
        N_interf_min = 1
    if N_interf_max < N_interf_min:
        N_interf_max = N_interf_min

    all_scenarios = generate_scenarios(
        N_repeat=N_repeat,
        Max_interf=N_interf_max,
        theta_s_range=theta_s_range,
        phi_s_range=phi_s_range,
        theta_i_range=theta_i_range,
        phi_i_range=phi_i_range
    )

    # выбираем только нужный диапазон
    scenarios = all_scenarios[N_interf_min - 1 : N_interf_max]

    return scenarios