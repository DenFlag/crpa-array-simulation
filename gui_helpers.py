# gui_helpers.py

from matplotlib.figure import Figure
from geometry import get_array_positions



# Жесткий ГУИ

def create_figure_and_axes():
    fig = Figure(figsize=(10, 7))

    ax_array  = fig.add_subplot(221)   # геометрия решётки
    ax_levels = fig.add_subplot(222)   # Signal / Interference
    ax_sir    = fig.add_subplot(224)   # SIR

    ax_array.set_aspect("equal", adjustable="box")
    ax_array.set_xlabel("x / λ")
    ax_array.set_ylabel("y / λ")
    ax_array.grid(True)

    ax_levels.set_ylabel("Level, dB")
    ax_levels.grid(True)

    ax_sir.set_ylabel("SIR, dB")
    ax_sir.grid(True)
    fig.subplots_adjust(hspace=0.35, wspace=0.25)
    return fig, ax_array, ax_levels, ax_sir


def clear_axes(ax_levels, ax_sir):
    ax_levels.clear()
    ax_sir.clear()

    ax_levels.set_ylabel("Level, dB")
    ax_sir.set_ylabel("SIR, dB")
    ax_sir.set_xlabel("X")

    ax_levels.grid(True)
    ax_sir.grid(True)

def build_array_from_gui(geometry, d_lambda, gui):
    """
    Строит описание решётки на основе GUI-параметров
    """

    if geometry == "rectangular":
        return {
            "geometry": "rectangular",
            "Nx": gui["Nx"].get(),
            "Ny": gui["Ny"].get(),
            "d_lambda": d_lambda
        }

    elif geometry == "triangular":
        return {
            "geometry": "triangular",
            "params": {
                "N_side": gui["N_side"].get(),
                "d_lambda": d_lambda
            }
        }

    elif geometry == "circular":
        return {
            "geometry": "circular",
            "params": {
                "N_rings": gui["N_rings"].get(),
                "dr_lambda": d_lambda,
                "N0": gui["N0"].get(),
                "include_center": gui["center"].get()
            }
        }

    else:
        raise ValueError("Unknown geometry")


def update_controls(mode, d_slider, d_grid_entry):
    if mode == "spacing":
        d_slider.config(state="disabled")
        d_grid_entry.config(state="normal")
    else:
        d_slider.config(state="normal")
        d_grid_entry.config(state="disabled")

def update_array_param_visibility(*_):
    rect_frame.pack_forget()
    tri_frame.pack_forget()
    circ_frame.pack_forget()

    geom = geom_var.get()

    if geom == "rectangular":
        rect_frame.pack(fill=tk.X, pady=4)
    elif geom == "triangular":
        tri_frame.pack(fill=tk.X, pady=4)
    elif geom == "circular":
        circ_frame.pack(fill=tk.X, pady=4)

def clear_axes(ax_levels, ax_sir):
    ax_levels.clear()
    ax_sir.clear()

    ax_levels.set_ylabel("Level, dB")
    ax_sir.set_ylabel("SIR, dB")
    ax_sir.set_xlabel("X")

    ax_levels.grid(True)
    ax_sir.grid(True)

