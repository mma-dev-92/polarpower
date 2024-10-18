from typing import Optional

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import Index, Series
from src.preprocess import LINE, TRAFO
from src.preprocess.data_models.utils import (err_finite_check, err_ge_check,
                                              err_line_col_check, finite_check,
                                              line_col_check)


class BranchesDataModel(pa.DataFrameModel):
    """Base data model for branches DataFrame."""

    branch_id: Index[str] = pa.Field(
        check_name=True,
        coerce=True,
        unique=True,
        description="Branch default identifier.",
    )
    branch_type: Series[str] = pa.Field(
        coerce=True,
        isin=[TRAFO, LINE],
        description="Branch type, can be either 'LINE' or 'TRAFO'",
    )
    node_from: Series[str] = pa.Field(
        coerce=True, description="Identifier of branch starting node."
    )
    node_to: Series[str] = pa.Field(
        coerce=True, description="Identifier of branch ending node."
    )
    reactance: Series[float] = pa.Field(
        gt=0.0,
        coerce=True,
        description="Reactance of a branch [per unit].",
    )
    F_max: Series[float] = pa.Field(
        coerce=True,
        description="Maximal flow on a branch [per unit].",
    )
    F_min: Optional[Series[float]] = pa.Field(
        nullable=True,
        default=np.nan,
        coerce=True,
        description="Minimal flow on a branch, if not provided set to -F_max.",
    )
    tap_ratio: Optional[Series[float]] = pa.Field(
        nullable=True,
        default=1.0,
        gt=0.0,
        coerce=True,
        description="Tap ratio (for 'TRAFO' branches only.)",
    )
    phase_shift: Optional[Series[float]] = pa.Field(
        coerce=True,
        default=0.0,
        in_range={"min_value": 0.0, "max_value": np.pi / 2},
        description="Phase shift (for 'TRAFO' branches only).",
    )
    phase_shift_min: Optional[Series[float]] = pa.Field(
        nullable=True,
        default=np.nan,
        in_range={"min_value": 0.0, "max_value": np.pi / 2},
        coerce=True,
        description="Minimal phase shift (optional for 'TRAFO' branches only).",
    )
    phase_shift_max: Optional[Series[float]] = pa.Field(
        nullable=True,
        default=np.nan,
        in_range={"min_value": 0.0, "max_value": np.pi / 2},
        coerce=True,
        description="Maximal phase shift (optional for 'TRAFO' branches only).",
    )

    @pa.check("reactance", error=err_finite_check("reactance", null=False))
    def validate_reactance_is_finite(cls, reactance: Series[float]):
        return finite_check(reactance, allow_nan=False)

    @pa.check("F_max", error=err_finite_check("F_max", null=False))
    def validate_F_max_is_finite(cls, F_max: Series[float]):
        return finite_check(F_max, allow_nan=False)

    @pa.check("F_min", error=err_finite_check("F_min", null=True))
    def validate_F_min_is_finite(cls, F_min: Series[float]):
        return finite_check(F_min, allow_nan=True)

    @pa.check("tap_ratio", error=err_finite_check("tap_ratio", null=True))
    def validate_tap_ratio_is_finite(cls, tap_ratio: Series[float]):
        return finite_check(tap_ratio, allow_nan=True)

    @pa.check("phase_shift", error=err_finite_check("phase_shift", null=True))
    def validate_phase_shift_is_finite(cls, phase_shift: Series[float]):
        return finite_check(phase_shift, allow_nan=True)

    @pa.check("phase_shift_min", error=err_finite_check("phase_shift_min", null=True))
    def validate_phase_shift_min_is_finite(cls, phase_shift_min: Series[float]):
        return finite_check(phase_shift_min, allow_nan=True)

    @pa.check("phase_shift_max", error=err_finite_check("phase_shift_min", null=True))
    def validate_phase_shift_max_is_finite(cls, phase_shift_max: Series[float]):
        return finite_check(phase_shift_max, allow_nan=True)

    @pa.dataframe_check(error=err_ge_check("F_max", "F_min", null=True))
    def validate_flow_limits(cls, df: pd.DataFrame):
        """Validate if F_max >= F_min for each branch, where F_min is specified."""
        if "F_min" not in df.columns:
            return True
        min_flow_provided = df[~np.isnan(df["F_min"])]
        return min_flow_provided["F_min"] <= min_flow_provided["F_max"]

    @pa.dataframe_check
    def validate_optional_parameters_for_trafos(cls, df: pd.DataFrame):
        """
        For each 'TRAFO' branch:
        - phase_shift value MUST be provided AND phase_shift_limits NOT OR
        - phase_shift_limits MUST be provided AND phase shift NOT.
        """
        trafos_df = df[df["branch_type"] == TRAFO]
        if trafos_df.size == 0:
            return True
        elif not any(
            col in df.columns
            for col in ["phase_shift", "phase_shift_min", "phase_shift_max"]
        ):
            return False

        ps = pd.notna(trafos_df["phase_shift"])
        ps_min = pd.notna(trafos_df["phase_shift_min"])
        ps_max = pd.notna(trafos_df["phase_shift_max"])

        ps_provided = ps & ~ps_min & ~ps_max
        ps_limits_provided = ~ps & ps_min & ps_max

        return ps_provided | ps_limits_provided

    @pa.dataframe_check(error=err_line_col_check("tap_ratio"))
    def validate_lines_tap_ratio(cls, df: pd.DataFrame):
        return line_col_check(df, "tap_ratio", 1.0)

    @pa.dataframe_check(error=err_line_col_check("phase_shift"))
    def validate_lines_phase_shift(cls, df: pd.DataFrame):
        return line_col_check(df, "phase_shift", 0.0)

    @pa.dataframe_check(error=err_line_col_check("phase_shift_min"))
    def validate_lines_phase_shift_min(cls, df: pd.DataFrame):
        return line_col_check(df, "phase_shift_min", np.nan)

    @pa.dataframe_check(error=err_line_col_check("phase_shift_max"))
    def validate_lines_phase_shift_max(cls, df: pd.DataFrame):
        return line_col_check(df, "phase_shift_max", np.nan)
