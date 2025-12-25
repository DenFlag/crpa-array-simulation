# gui_layout.py

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui_helpers import create_figure_and_axes

def create_root():
    root = tk.Tk()
    root.title("CRPA Interactive Experiment")
    root.geometry("1350x780")
    return root

def create_control_panel(root):
    control = ttk.Frame(root, width=320)
    control.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    vars = {}

    # =====================================================
    # MODE
    # =====================================================
    ttk.Label(control, text="Experiment mode").pack(anchor="w")

    vars["mode"] = tk.StringVar(value="spacing")
    ttk.Combobox(
        control,
        textvariable=vars["mode"],
        values=["quantization", "spacing", "position_error"],
        state="readonly"
    ).pack(fill=tk.X, pady=4)

    # =====================================================
    # GEOMETRY  (ВАЖНО: создаётся РАНЬШЕ параметров решётки)
    # =====================================================
    ttk.Label(control, text="Array geometry").pack(anchor="w", pady=(10, 0))

    vars["geometry"] = tk.StringVar(value="rectangular")
    ttk.Combobox(
        control,
        textvariable=vars["geometry"],
        values=["rectangular", "triangular", "circular"],
        state="readonly"
    ).pack(fill=tk.X, pady=4)

    # =====================================================
    # ARRAY PARAMETERS (rect / tri / circ)
    # =====================================================
    ttk.Label(
        control,
        text="Array parameters",
        font=("Arial", 10, "bold")
    ).pack(anchor="w", pady=(15, 5))

    # создаём параметры решётки и visibility-callback
    vars.update(
        create_array_param_controls(
            parent=control,
            geometry_var=vars["geometry"]
        )
    )

    # подписка на изменение геометрии
    vars["geometry"].trace_add(
        "write",
        vars["_update_array_param_visibility"]
    )

    # первичное отображение нужных параметров
    vars["_update_array_param_visibility"]()

    # =====================================================
    # PHASE BITS (fixed)
    # =====================================================
    ttk.Label(control, text="Phase bits").pack(anchor="w", pady=(10, 0))

    vars["nBits"] = tk.IntVar(value=11)
    ttk.Spinbox(
        control,
        from_=1, to=16,
        textvariable=vars["nBits"]
    ).pack(fill=tk.X)

    # =====================================================
    # SINGLE d / λ
    # =====================================================
    ttk.Label(control, text="Single d / λ").pack(anchor="w", pady=(10, 0))

    vars["d_single"] = tk.DoubleVar(value=0.5)
    tk.Scale(
        control,
        from_=0.1, to=0.6,
        resolution=0.05,
        orient=tk.HORIZONTAL,
        variable=vars["d_single"]
    ).pack(fill=tk.X)

    # =====================================================
    # d / λ GRID (spacing mode)
    # =====================================================
    ttk.Label(control, text="d / λ grid (spacing)").pack(anchor="w", pady=(10, 0))

    vars["d_grid"] = tk.StringVar(value="0.1, 0.2, 0.3, 0.4, 0.5")
    ttk.Entry(
        control,
        textvariable=vars["d_grid"]
    ).pack(fill=tk.X)

    # =====================================================
    # PHASE BITS GRID (quantization)
    # =====================================================
    ttk.Label(control, text="Phase bits grid").pack(anchor="w", pady=(10, 0))

    vars["nBits_grid"] = tk.StringVar(value="1, 2, 4, 8")
    ttk.Entry(
        control,
        textvariable=vars["nBits_grid"]
    ).pack(fill=tk.X)

    # =====================================================
    # POSITION ERROR GRID
    # =====================================================
    ttk.Label(
        control,
        text="σ position error grid (λ)"
    ).pack(anchor="w", pady=(10, 0))

    vars["sigma_grid"] = tk.StringVar(value="0.0, 0.1, 0.2")
    ttk.Entry(
        control,
        textvariable=vars["sigma_grid"]
    ).pack(fill=tk.X)

    # =====================================================
    # NUMBER OF REALIZATIONS
    # =====================================================
    ttk.Label(
        control,
        text="Number of realizations"
    ).pack(anchor="w", pady=(10, 0))

    vars["Nrepeat"] = tk.IntVar(value=20)
    ttk.Spinbox(
        control,
        from_=1, to=500,
        textvariable=vars["Nrepeat"]
    ).pack(fill=tk.X)

    # =====================================================
    # NUMBER OF INTERFERERS
    # =====================================================
    ttk.Label(
        control,
        text="Number of interferers (range)"
    ).pack(anchor="w", pady=(10, 0))

    vars["Ninterf_min"] = tk.IntVar(value=6)
    vars["Ninterf_max"] = tk.IntVar(value=8)

    row = ttk.Frame(control)
    row.pack(fill=tk.X)

    ttk.Label(row, text="from").pack(side=tk.LEFT)
    ttk.Spinbox(
        row,
        from_=1, to=20,
        width=5,
        textvariable=vars["Ninterf_min"]
    ).pack(side=tk.LEFT, padx=5)

    ttk.Label(row, text="to").pack(side=tk.LEFT)
    ttk.Spinbox(
        row,
        from_=1, to=20,
        width=5,
        textvariable=vars["Ninterf_max"]
    ).pack(side=tk.LEFT, padx=5)

    return control, vars



def create_plot_area(root):
    fig, ax_array, ax_levels, ax_sir = create_figure_and_axes()

    frame = ttk.Frame(root)
    frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    return fig, ax_array, ax_levels, ax_sir, canvas

def create_run_button(parent, callback):
    ttk.Separator(parent, orient="horizontal").pack(
        fill=tk.X, pady=(20, 10)
    )
    ttk.Button(
        parent,
        text="RUN EXPERIMENT",
        command=callback
    ).pack(fill=tk.X)

def create_array_param_controls(parent):
    vars = {}

    rect = ttk.Frame(parent)
    vars["Nx"] = tk.IntVar(value=3)
    vars["Ny"] = tk.IntVar(value=3)
    # ...

    tri = ttk.Frame(parent)
    vars["N_side"] = tk.IntVar(value=6)

    circ = ttk.Frame(parent)
    vars["N_rings"] = tk.IntVar(value=3)
    vars["N0"] = tk.IntVar(value=6)
    vars["center"] = tk.BooleanVar(value=True)

    return vars

def create_array_param_controls(parent):
    vars = {}

    # ---------- RECTANGULAR ----------
    rect_frame = ttk.Frame(parent)

    vars["Nx"] = tk.IntVar(value=3)
    vars["Ny"] = tk.IntVar(value=3)

    ttk.Label(rect_frame, text="Nx").grid(row=0, column=0, sticky="w")
    ttk.Spinbox(rect_frame, from_=1, to=16,
                textvariable=vars["Nx"], width=6).grid(row=0, column=1)

    ttk.Label(rect_frame, text="Ny").grid(row=1, column=0, sticky="w")
    ttk.Spinbox(rect_frame, from_=1, to=16,
                textvariable=vars["Ny"], width=6).grid(row=1, column=1)

    # ---------- TRIANGULAR ----------
    tri_frame = ttk.Frame(parent)

    vars["N_side"] = tk.IntVar(value=6)

    ttk.Label(tri_frame, text="N_side").grid(row=0, column=0, sticky="w")
    ttk.Spinbox(tri_frame, from_=2, to=20,
                textvariable=vars["N_side"], width=6).grid(row=0, column=1)

    # ---------- CIRCULAR ----------
    circ_frame = ttk.Frame(parent)

    vars["N_rings"] = tk.IntVar(value=3)
    vars["N0"] = tk.IntVar(value=6)
    vars["center"] = tk.BooleanVar(value=True)

    ttk.Label(circ_frame, text="N_rings").grid(row=0, column=0, sticky="w")
    ttk.Spinbox(circ_frame, from_=1, to=10,
                textvariable=vars["N_rings"], width=6).grid(row=0, column=1)

    ttk.Label(circ_frame, text="N0").grid(row=1, column=0, sticky="w")
    ttk.Spinbox(circ_frame, from_=1, to=20,
                textvariable=vars["N0"], width=6).grid(row=1, column=1)

    ttk.Checkbutton(
        circ_frame,
        text="Include center element",
        variable=vars["center"]
    ).grid(row=2, column=0, columnspan=2, sticky="w")

    # ---------- VISIBILITY HANDLER ----------
    def update_array_param_visibility(*_):
        rect_frame.pack_forget()
        tri_frame.pack_forget()
        circ_frame.pack_forget()

        geom = vars["geometry"].get()

        if geom == "rectangular":
            rect_frame.pack(fill=tk.X, pady=4)
        elif geom == "triangular":
            tri_frame.pack(fill=tk.X, pady=4)
        elif geom == "circular":
            circ_frame.pack(fill=tk.X, pady=4)

    # ⚠ geometry var будет добавлена позже
    vars["_rect_frame"] = rect_frame
    vars["_tri_frame"] = tri_frame
    vars["_circ_frame"] = circ_frame
    vars["_update_array_param_visibility"] = update_array_param_visibility

    return vars

def create_array_param_controls(parent, geometry_var):
    vars = {}

    # ---------- RECTANGULAR ----------
    rect_frame = ttk.Frame(parent)

    vars["Nx"] = tk.IntVar(value=3)
    vars["Ny"] = tk.IntVar(value=3)

    ttk.Label(rect_frame, text="Nx").grid(row=0, column=0, sticky="w")
    ttk.Spinbox(
        rect_frame, from_=1, to=16,
        textvariable=vars["Nx"], width=6
    ).grid(row=0, column=1)

    ttk.Label(rect_frame, text="Ny").grid(row=1, column=0, sticky="w")
    ttk.Spinbox(
        rect_frame, from_=1, to=16,
        textvariable=vars["Ny"], width=6
    ).grid(row=1, column=1)

    # ---------- TRIANGULAR ----------
    tri_frame = ttk.Frame(parent)

    vars["N_side"] = tk.IntVar(value=6)

    ttk.Label(tri_frame, text="N_side").grid(row=0, column=0, sticky="w")
    ttk.Spinbox(
        tri_frame, from_=2, to=20,
        textvariable=vars["N_side"], width=6
    ).grid(row=0, column=1)

    # ---------- CIRCULAR ----------
    circ_frame = ttk.Frame(parent)

    vars["N_rings"] = tk.IntVar(value=3)
    vars["N0"] = tk.IntVar(value=6)
    vars["center"] = tk.BooleanVar(value=True)

    ttk.Label(circ_frame, text="N_rings").grid(row=0, column=0, sticky="w")
    ttk.Spinbox(
        circ_frame, from_=1, to=10,
        textvariable=vars["N_rings"], width=6
    ).grid(row=0, column=1)

    ttk.Label(circ_frame, text="N0").grid(row=1, column=0, sticky="w")
    ttk.Spinbox(
        circ_frame, from_=1, to=20,
        textvariable=vars["N0"], width=6
    ).grid(row=1, column=1)

    ttk.Checkbutton(
        circ_frame,
        text="Include center element",
        variable=vars["center"]
    ).grid(row=2, column=0, columnspan=2, sticky="w")

    # ---------- VISIBILITY ----------
    def update_array_param_visibility(*_):
        rect_frame.pack_forget()
        tri_frame.pack_forget()
        circ_frame.pack_forget()

        geom = geometry_var.get()

        if geom == "rectangular":
            rect_frame.pack(fill=tk.X, pady=4)
        elif geom == "triangular":
            tri_frame.pack(fill=tk.X, pady=4)
        elif geom == "circular":
            circ_frame.pack(fill=tk.X, pady=4)

    vars["_update_array_param_visibility"] = update_array_param_visibility

    return vars
