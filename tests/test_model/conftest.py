import numpy as np
import pandas as pd
import pytest
from src.model import BranchType


@pytest.fixture
def generators_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "generator_id": "GEN1",
                "node_id": "N1",
                "P_min": -2.0,
                "P_max": 3.0,
                "cost": 1.0,
            },
            {
                "generator_id": "GEN2",
                "node_id": "N2",
                "P_min": 3.0,
                "P_max": 4.5,
                "cost": np.nan,
            },
            {
                "generator_id": "GEN3",
                "node_id": "N1",
                "P_min": -3.0,
                "P_max": 3.0,
                "cost": 3.5,
            },
            {
                "generator_id": "GEN4",
                "node_id": "N3",
                "P_min": -7.0,
                "P_max": -3.5,
                "cost": 0.0,
            },
        ]
    ).set_index("generator_id")


@pytest.fixture
def nodes_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"node_id": "N1", "P_demand": 3.5},
            {"node_id": "N2", "P_demand": 0.5},
            {"node_id": "N3", "P_demand": -2.5},
            {"node_id": "N4", "P_demand": 0.0},
            {"node_id": "N5", "P_demand": np.nan},
        ]
    ).set_index("node_id")


@pytest.fixture
def branches_lines_and_trafos_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "branch_id": "TRAFO1",
                "branch_type": BranchType.TRAFO.name,
                "node_from": "N2",
                "node_to": "N3",
                "reactance": 0.07,
                "F_max": 4.5,
                "F_min": np.nan,
                "tap_ratio": 1.1,
                "phase_shift": np.pi / 6,
            },
            {
                "branch_id": "TRAFO2",
                "branch_type": BranchType.TRAFO.name,
                "node_from": "N4",
                "node_to": "N3",
                "reactance": 0.07,
                "F_max": 4.5,
                "F_min": np.nan,
                "tap_ratio": 1.1,
                "phase_shift": np.pi / 6,
            },
            {
                "branch_id": "TRAFO3",
                "branch_type": BranchType.TRAFO.name,
                "node_from": "N4",
                "node_to": "N3",
                "reactance": 0.07,
                "F_max": 4.5,
                "F_min": np.nan,
                "tap_ratio": 1.0,
                "phase_shift": 0,
            },
            {
                "branch_id": "LINE1",
                "branch_type": BranchType.LINE.name,
                "node_from": "N4",
                "node_to": "N5",
                "reactance": 0.03,
                "F_max": 4.5,
                "F_min": -3.0,
                "tap_ratio": 1.0,
                "phase_shift": np.nan,
            },
            {
                "branch_id": "LINE2",
                "branch_type": BranchType.LINE.name,
                "node_from": "N2",
                "node_to": "N5",
                "reactance": 0.03,
                "F_max": 4.5,
                "F_min": -3.0,
                "tap_ratio": np.nan,
                "phase_shift": np.nan,
            },
            {
                "branch_id": "LINE3",
                "branch_type": BranchType.LINE.name,
                "node_from": "N3",
                "node_to": "N5",
                "reactance": 0.03,
                "F_max": 4.5,
                "F_min": -3.0,
                "tap_ratio": np.nan,
                "phase_shift": 0.0,
            },
        ]
    ).set_index("branch_id")


@pytest.fixture
def branches_only_lines_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "branch_id": "LINE1",
                "branch_type": BranchType.LINE.name,
                "node_from": "N1",
                "node_to": "N2",
                "reactance": 0.1,
                "F_max": 3.0,
            },
            {
                "branch_id": "LINE2",
                "branch_type": BranchType.LINE.name,
                "node_from": "N3",
                "node_to": "N2",
                "reactance": 0.05,
                "F_max": 1.0,
            },
            {
                "branch_id": "LINE3",
                "branch_type": BranchType.LINE.name,
                "node_from": "N1",
                "node_to": "N3",
                "reactance": 0.01,
                "F_max": 2.0,
            },
        ]
    ).set_index("branch_id")


@pytest.fixture
def branches_only_trafos_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "branch_id": "TRAFO1",
                "branch_type": BranchType.TRAFO.name,
                "node_from": "N2",
                "node_to": "N3",
                "reactance": 0.07,
                "F_max": 4.5,
                "F_min": np.nan,
                "tap_ratio": 1.1,
                "phase_shift": np.pi / 6,
            },
            {
                "branch_id": "TRAFO2",
                "branch_type": BranchType.TRAFO.name,
                "node_from": "N4",
                "node_to": "N3",
                "reactance": 0.07,
                "F_max": 2.5,
                "F_min": np.nan,
                "tap_ratio": 1.1,
                "phase_shift": np.pi / 6,
            },
            {
                "branch_id": "TRAFO3",
                "branch_type": BranchType.TRAFO.name,
                "node_from": "N4",
                "node_to": "N3",
                "reactance": 0.07,
                "F_max": 4.5,
                "F_min": np.nan,
                "tap_ratio": 1.0,
                "phase_shift": 0,
            },
        ]
    ).set_index("branch_id")
