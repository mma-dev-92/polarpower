from dataclasses import dataclass

import pandas as pd


@dataclass
class InputData:
    """Class for the input power system data."""

    branches: pd.DataFrame
    """Branches parameters."""
    generators: pd.DataFrame
    """Generators parameters."""
    nodes: pd.DataFrame
    """Nodes parameters."""
