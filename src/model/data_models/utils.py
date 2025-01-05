import numpy as np
import pandas as pd


def finite_check(s: pd.Series, allow_nan: bool = False):
    """Custom check if column contains only finite values."""
    if allow_nan:
        result = np.isfinite(s[~np.isnan(s)])
    else:
        result = np.isfinite(s)
    return result


def err_finite_check(col_name: str, null: bool):
    if not null:
        result = f"'{col_name}' must be a finite number."
    else:
        result = f"'{col_name}' must be a finite number (if provided)."
    return result


def err_ge_check(ge: str, le: str, null: bool) -> str:
    if not null:
        result = f"'{ge}' must be greater or equal to '{le}'."
    else:
        result = f"'{ge}' must be greater or equal to '{le}' (if privided)."
    return result


def err_greater_check(g: str, l: str, null: bool) -> str:
    if not null:
        result = f"'{g}' must be greater from '{l}'."
    else:
        result = f"'{g}' must be greater from '{l}' (if privided)."
    return result


def err_foreign_key(fk_col: str) -> str:
    return f"invalid refference to {fk_col}"


def err_prange() -> str:
    return "some power generation ranges [p_start, p_end] are incorrect"


def err_non_monotonic_merit_order() -> str:
    return "some generators have decreasing merit order costs"
