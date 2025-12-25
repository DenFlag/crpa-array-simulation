import numpy as np
k = 2 * np.pi

from gui_controller import run_gui_experiment
from gui_layout import (
    create_root,
    create_control_panel,
    create_plot_area,
    create_run_button
)

if __name__ == "__main__":

    root = create_root()

    control, gui = create_control_panel(root)

    fig, ax_array, ax_levels, ax_sir, canvas = create_plot_area(root)


    def on_run():
        run_gui_experiment(
            mode=gui["mode"].get(),
            geometry=gui["geometry"].get(),
            d_lambda_single=gui["d_single"].get(),
            d_lambda_grid_text=gui["d_grid"].get(),
            sigma_grid_text=gui["sigma_grid"].get(),
            nBits_grid_text=gui["nBits_grid"].get(),
            nBits=gui["nBits"].get(),
            gui=gui,
            k=k,
            N_interf_min=gui["Ninterf_min"].get(),
            ax_array=ax_array,
            ax_levels=ax_levels,
            ax_sir=ax_sir,
            canvas=canvas
        )


    create_run_button(control, on_run)
    root.mainloop()


