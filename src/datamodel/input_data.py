from dataclasses import dataclass
import pandas as pd


@dataclass
class InputPowerSystemData:
    """Class for the input power system data."""

    lines: pd.DataFrame
    """Lines parameters."""
    trafos: pd.DataFrame
    """Trafos parameters."""
    generators: pd.DataFrame
    """Generators parameters."""
    nodes: pd.DataFrame
    """Nodes parameters."""
