import sys
from dataclasses import dataclass
from typing import Self

import numpy as np
import pandas as pd
from pandera import errors
from src.model.data_models.branches_data_model import BranchesDataModel
from src.model.data_models.error_logs import log_schema_errors
from src.model.data_models.generators_data_model import GeneratorsDataModel
from src.model.data_models.nodes_data_model import NodesDataModel


@dataclass
class SystemParameters:
    """Power system model initial parameters."""

    branches: pd.DataFrame
    """Branches parameters."""
    generators: pd.DataFrame
    """Generators parameters."""
    nodes: pd.DataFrame
    """Nodes parameters."""

    def __post_init__(self) -> None:
        self._validate()
        self._refine()

    def _validate(self) -> None:
        data_is_correct: bool = True
        for df, data_model, context in [
            (self.branches, BranchesDataModel, {"nodes_index": self.nodes.index}),
            (self.generators, GeneratorsDataModel, {"nodes_index": self.nodes.index}),
            (self.nodes, NodesDataModel, dict()),
        ]:
            try:
                data_model.validate(
                    check_obj=df, lazy=True, inplace=True, context=context
                )
            except errors.SchemaErrors as schema_errors:
                log_schema_errors(schema_errors)
                data_is_correct = False

        if not data_is_correct:
            sys.exit()

    def _refine(self) -> None:
        f_min_nan = self.branches["F_min"].isna()
        if f_min_nan.size > 0:
            self.branches.loc[f_min_nan, "F_min"] = -self.branches[f_min_nan]["F_max"]


@dataclass
class SystemState:
    """Power system state."""

    power_generation: pd.Series
    """Generators power generation."""
    power_flow: pd.Series
    """Branches power flow."""
    theta: pd.Series
    """Nodes voltage angle."""

    @classmethod
    def undefined_state(cls, params: SystemParameters) -> Self:
        """Undefined (NaN) model state."""
        return cls(
            power_generation=cls._nan_like(params.generators, "Power Generation"),
            power_flow=cls._nan_like(params.branches, "Power Flow"),
            theta=cls._nan_like(params.nodes, "Theta"),
        )

    @staticmethod
    def _nan_like(df: pd.DataFrame, name: str) -> pd.Series:
        return pd.Series(data=np.ones(len(df)) * np.nan, index=df.index, name=name)


class PowerSystemModel:
    """Power System Model Representation"""

    def __init__(
        self,
        generators: pd.DataFrame,
        branches: pd.DataFrame,
        nodes: pd.DataFrame,
    ) -> None:
        self._parameters = SystemParameters(
            generators=generators,
            branches=branches,
            nodes=nodes,
        )
        self._state = SystemState.undefined_state(self._parameters)

    @property
    def parameters(self) -> SystemParameters:
        """Parameters defining system structure and its components."""
        return self._parameters

    @property
    def state(self) -> SystemState:
        """State of the system and its compontents."""
        return self._state
