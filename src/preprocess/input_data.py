from dataclasses import dataclass

import pandas as pd


@dataclass
class InputPowerSystemData:
    """Class for the input power system data."""

    branches: pd.DataFrame
    """Branches parameters."""
    generators: pd.DataFrame
    """Generators parameters."""
    nodes: pd.DataFrame
    """Nodes parameters."""

    def __post_init__(self) -> None:
        pass

    def validate_branches(self) -> pd.DataFrame:
        raise NotImplementedError

    def validate_nodes(self) -> pd.DataFrame:
        raise NotImplementedError

    def validate_generators(self) -> pd.DataFrame:
        raise NotImplementedError
