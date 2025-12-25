import numpy as np

# =========================================================
# GEOMETRY
# =========================================================


def get_array_positions(array):
    geom = array["geometry"]

    if geom == "rectangular":
        return rectangular_positions(
            array["Nx"], array["Ny"], array["d_lambda"]
        )

    elif geom == "triangular":
        return triangular_positions(
            array["params"]["N_side"],
            array["params"]["d_lambda"]
        )

    elif geom == "circular":
        return circular_positions(
            array["params"]["N_rings"],
            array["params"]["dr_lambda"],
            array["params"]["N0"],
            array["params"].get("include_center", True)
        )

    else:
        raise ValueError(f"Unknown geometry: {geom}")

def rectangular_positions(Nx, Ny, d_lambda):
    x, y = np.meshgrid(np.arange(Nx), np.arange(Ny), indexing="ij")
    x = (x - (Nx - 1) / 2) * d_lambda
    y = (y - (Ny - 1) / 2) * d_lambda
    return np.column_stack((x.ravel(), y.ravel()))

def triangular_positions(N_side, d_lambda):
    positions = []

    dy = np.sqrt(3) / 2 * d_lambda

    for row in range(N_side):
        for col in range(N_side - row):
            x = col * d_lambda + row * d_lambda / 2
            y = row * dy
            positions.append([x, y])

    positions = np.array(positions)

    # центрирование
    positions[:, 0] -= np.mean(positions[:, 0])
    positions[:, 1] -= np.mean(positions[:, 1])

    return positions

def circular_positions(N_rings, dr_lambda, N0, include_center=True):
    positions = []

    if include_center:
        positions.append([0.0, 0.0])

    for k in range(1, N_rings + 1):
        r = k * dr_lambda
        Nk = int(round(2 * np.pi * r / (2 * np.pi * dr_lambda / N0)))
        Nk = max(Nk, 1)

        for n in range(Nk):
            phi = 2 * np.pi * n / Nk
            x = r * np.cos(phi)
            y = r * np.sin(phi)
            positions.append([x, y])

    return np.array(positions)

# Ошибка позиции
def apply_position_error(positions, sigma_pos):
    """
    Добавляет ошибку положения элементов.

    positions : (N, 2)
    sigma_pos : СКО ошибки в долях длины волны
    """
    if sigma_pos <= 0:
        return positions

    perturbation = np.random.normal(
        loc=0.0,
        scale=sigma_pos,
        size=positions.shape
    )

    return positions + perturbation
