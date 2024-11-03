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
