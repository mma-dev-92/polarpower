import numpy as np
import pandas as pd
from src.model import BranchType


def line_col_check(df: pd.DataFrame, col_name: str, val: float):
    """
    Validate transformer parameter column for 'LINE' branches.

    If given column is not in the given DataFrame - validation passes only
    if there is no transformer ('TRAFO' branch) in the DataFrame.

    If given column exists in the given DataFrame, make sure, that all
    values for 'LINE' branches are euqal to specific value.
    """
    line_data = df[df["branch_type"] == BranchType.LINE]
    if col_name not in df.columns:
        result = line_data.size == df.size
    elif np.isnan(val):
        result = pd.isna(line_data[col_name])
    else:
        result = line_data[col_name] == val
    return result


def err_line_col_check(col_name: str, default: float) -> str:
    return f"For '{BranchType.LINE}' branches '{col_name} must be set to {default} or left empty."


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
