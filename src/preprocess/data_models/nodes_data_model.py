from typing import Optional

import pandas as pd
import pandera as pa
from pandera.typing import Index, Series
from src.preprocess.data_models.utils import err_finite_check, finite_check


class NodesDataModel(pa.DataFrameModel):
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

    @pa.check("P_demand", error=err_finite_check("P_demand", null=True))
    def validate_demand_is_finite(cls, P_demand: pd.Series):
        """Check that all provided demand values are finite."""
        return finite_check(P_demand, allow_nan=True)
