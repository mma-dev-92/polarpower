from dataclasses import dataclass
import pandas as pd


@dataclass
class InputPowerSystemData:
    """Class for the input power system data."""

    branches: pd.DataFrame
    """Lines and trafos parameters."""
    generators: pd.DataFrame
    """Generators parameters."""
    nodes: pd.DataFrame
    """Nodes parameters."""
