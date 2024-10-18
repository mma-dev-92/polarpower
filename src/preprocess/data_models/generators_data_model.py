from typing import Optional

import pandas as pd
import pandera as pa
from pandera.typing import Index, Series
from src.preprocess.data_models.utils import (err_finite_check, err_ge_check,
                                              finite_check)


class GeneratorsDataModel(pa.DataFrameModel):
    """Data model for generators DataFrame."""

    generator_id: Index[str] = pa.Field(
        check_name=True,
        unique=True,
        coerce=True,
        description="Unique generator identifier.",
    )
    node_id: Series[str] = pa.Field(
        coerce=True, description="Node, to which generator is attached."
    )
    P_max: Series[float] = pa.Field(
        coerce=True,
        description="Maximal power generation.",
    )
    P_min: Series[float] = pa.Field(
        coerce=True,
        description="Minimal power generation.",
    )
    cost: Optional[Series[float]] = pa.Field(
        coerce=True,
        default=0.0,
        description="Linear cost of generation [per unit].",
    )
    active: Optional[Series[bool]] = pa.Field(
        coerce=True,
        default=True,
        description="Indicates if given generator is active or not.",
    )

    @pa.check("P_max", error=err_finite_check("P_max", null=False))
    def validate_P_max_is_finite(cls, P_max: Series[float]):
        return finite_check(P_max, allow_nan=False)

    @pa.check("P_min", error=err_finite_check("P_min", null=False))
    def validate_P_min_is_finite(cls, P_min: Series[float]):
        return finite_check(P_min, allow_nan=False)

    @pa.check("cost", error=err_finite_check("cost", null=True))
    def validate_cost_is_finite(cls, cost: Series[float]):
        return finite_check(cost, allow_nan=True)

    @pa.dataframe_check(error=err_ge_check("P_max", "P_min", null=False))
    def validate_power_bounds(cls, df: pd.DataFrame) -> pd.Series:
        """Validate if P_max is greater or equal than P_min."""
        return df["P_max"] >= df["P_min"]
