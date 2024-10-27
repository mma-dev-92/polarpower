from typing import Optional

import numpy as np
import pandas as pd
import pandera as pa
import src.model.data_models.utils as u
from pandera.typing import Index, Series
from src.model import BranchType
from src.model.data_models import DataFrameModelWithContext


class BranchesDataModel(DataFrameModelWithContext):
    """Data model for TransmissionLines dataset."""

    branch_id: Index[str] = pa.Field(
        check_name=True,
        coerce=True,
        unique=True,
        description="Element identifier.",
    )
    branch_type: Series[str] = pa.Field(
        coerce=True,
        isin=[BranchType.LINE.name, BranchType.TRAFO.name],
        description=f"Branch type: {BranchType.LINE} or {BranchType.TRAFO}.",
    )
    node_from: Series[str] = pa.Field(
        coerce=True, description="Identifier of a starting node."
    )
    node_to: Series[str] = pa.Field(
        coerce=True, description="Identifier of an ending node."
    )
    reactance: Series[float] = pa.Field(
        gt=0.0,
        coerce=True,
        description="Reactance [per unit].",
    )
    F_max: Series[float] = pa.Field(
        coerce=True,
        description="Maximal power flow [per unit].",
    )
    F_min: Optional[Series[float]] = pa.Field(
        nullable=True,
        default=np.nan,
        coerce=True,
        description="Minimal power flow [per unit].",
    )
    tap_ratio: Optional[Series[float]] = pa.Field(
        nullable=True,
        default=1.0,
        gt=0.0,
        coerce=True,
        description="Transforer tap ratio.",
    )
    phase_shift: Optional[Series[float]] = pa.Field(
        coerce=True,
        default=0.0,
        in_range={"min_value": 0.0, "max_value": np.pi / 2},
        description="Transformer phase shift angle.",
    )

    @pa.check("node_from")
    def validate_node_from_ideitifier(cls, node_from: Series[str]):
        return node_from.isin(cls.get_context("nodes_index"))

    @pa.check("node_to")
    def validate_node_to_identifier(cls, node_to: Series[str]):
        return node_to.isin(cls.get_context("nodes_index"))

    @pa.check("reactance", error=u.err_finite_check("reactance", null=False))
    def validate_reactance_is_finite(cls, reactance: Series[float]):
        return u.finite_check(reactance, allow_nan=False)

    @pa.check("F_max", error=u.err_finite_check("F_max", null=False))
    def validate_F_max_is_finite(cls, F_max: Series[float]):
        return u.finite_check(F_max, allow_nan=False)

    @pa.check("F_min", error=u.err_finite_check("F_min", null=True))
    def validate_F_min_is_finite(cls, F_min: Series[float]):
        return u.finite_check(F_min, allow_nan=True)

    @pa.dataframe_check(error=u.err_ge_check("F_max", "F_min", null=True))
    def validate_flow_limits(cls, df: pd.DataFrame):
        """Validate if F_max >= F_min for each branch, where F_min is specified."""
        if "F_min" not in df.columns:
            return True
        min_flow_provided = df[~np.isnan(df["F_min"])]
        return min_flow_provided["F_min"] <= min_flow_provided["F_max"]

    @pa.check("tap_ratio", error=u.err_finite_check("tap_ratio", null=True))
    def validate_tap_ratio_is_finite(cls, tap_ratio: Series[float]):
        return u.finite_check(tap_ratio, allow_nan=True)

    @pa.check("phase_shift", error=u.err_finite_check("phase_shift", null=True))
    def validate_phase_shift_is_finite(cls, phase_shift: Series[float]):
        return u.finite_check(phase_shift, allow_nan=True)

    @pa.dataframe_check(error=u.err_line_col_check("tap_ratio", default=1.0))
    def validate_lines_tap_ratio(cls, df: pd.DataFrame):
        return u.line_col_check(df, "tap_ratio", 1.0)

    @pa.dataframe_check(error=u.err_line_col_check("phase_shift", default=0.0))
    def validate_lines_phase_shift(cls, df: pd.DataFrame):
        return u.line_col_check(df, "phase_shift", 0.0)
