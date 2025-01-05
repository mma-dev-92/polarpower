from typing import Optional

import pandas as pd
import pandera as pa
from pandera.typing import Index, Series

import src.model.data_models.utils as utils
from src.model.data_models import DataFrameModelWithContext


class GeneratorsDataModel(DataFrameModelWithContext):
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
    active: Optional[Series[bool]] = pa.Field(
        coerce=True,
        default=True,
        description="Indicates if given generator is active or not.",
    )

    @pa.check("node_id", error=utils.err_foreign_key(fk_col="node_id"))
    def validate_node_identifiers(cls, node_id: Series[str]):
        return node_id.isin(cls.get_context("nodes_index"))

    @pa.check("P_max", error=utils.err_finite_check("P_max", null=False))
    def validate_P_max_is_finite(cls, P_max: Series[float]):
        return utils.finite_check(P_max, allow_nan=False)

    @pa.check("P_min", error=utils.err_finite_check("P_min", null=False))
    def validate_P_min_is_finite(cls, P_min: Series[float]):
        return utils.finite_check(P_min, allow_nan=False)

    @pa.dataframe_check(error=utils.err_ge_check("P_max", "P_min", null=False))
    def validate_power_bounds(cls, df: pd.DataFrame) -> pd.Series:
        """Validate if P_max is greater or equal than P_min."""
        return df["P_max"] >= df["P_min"]

