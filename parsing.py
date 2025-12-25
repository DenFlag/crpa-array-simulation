import numpy as np

def parse_nBits_grid(text):
    """
    Парсит строку вида:
    "1, 2, 3, 4, 6, 8, 10"

    -> np.array([1, 2, 3, 4, 6, 8, 10])
    """
    try:
        values = [int(v.strip()) for v in text.split(",")]
        values = [v for v in values if v >= 1]
        if len(values) < 1:
            raise ValueError
        return np.array(values)
    except Exception:
        raise ValueError("Invalid phase bits grid format")

def parse_d_lambda_grid(text):
    """
    Парсит строку вида:
    "0.1, 0.15, 0.2, 0.25"

    -> np.array([0.1, 0.15, 0.2, 0.25])
    """
    try:
        values = [float(v.strip()) for v in text.split(",")]
        values = [v for v in values if v > 0]
        if len(values) < 2:
            raise ValueError
        return np.array(values)
    except Exception:
        raise ValueError("Invalid d/λ grid format")

def parse_sigma_grid(text):
    try:
        values = [float(v.strip()) for v in text.split(",")]
        values = [v for v in values if v >= 0]
        if len(values) < 2:
            raise ValueError
        return np.array(values)
    except Exception:
        raise ValueError("Invalid σ grid format")