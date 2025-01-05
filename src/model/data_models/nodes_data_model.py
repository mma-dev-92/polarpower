from typing import Optional

import pandas as pd
import pandera as pa
from pandera.typing import Index, Series

import src.model.data_models.utils as utils
from src.model.data_models import DataFrameModelWithContext


class NodesDataModel(DataFrameModelWithContext):
    """Data model for nodes DataFrame."""

    node_id: Index[str] = pa.Field(
        check_name=True,
        nullable=False,
        description="Unique node identifier.",
        unique=True,
    )
    P_demand: Series[float] = pa.Field(
        nullable=True,
        default=0.0,
        description="Active power demand in the node.",
    )
    slack_node: Optional[Series[bool]] = pa.Field(
        default=False,
        description=(
            "Indicator which node is a slack node. If not specified, slack node "
            "will be picked randomly."
        ),
    )

    @pa.check("P_demand", error=utils.err_finite_check("P_demand", null=True))
    def validate_demand_is_finite(cls, P_demand: pd.Series):
        """Check that all provided demand values are finite."""
        return utils.finite_check(P_demand, allow_nan=True)
