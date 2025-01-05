import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def generators_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "generator_id": "GEN1",
                "node_id": "N1",
                "P_min": -2.0,
                "P_max": 3.0,
            },
            {
                "generator_id": "GEN2",
                "node_id": "N2",
                "P_min": 3.0,
                "P_max": 4.5,
            },
            {
                "generator_id": "GEN3",
                "node_id": "N1",
                "P_min": -3.0,
                "P_max": 3.0,
            },
            {
                "generator_id": "GEN4",
                "node_id": "N3",
                "P_min": -7.0,
                "P_max": -3.5,
            },
        ]
    ).set_index("generator_id")


@pytest.fixture
def marginal_costs_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"generator_id": "GEN1", "p_start": -2, "p_end": 0.0, "cost": -1.0},
            {"generator_id": "GEN1", "p_start": 0.0, "p_end": 3.0, "cost": 2.0},
            {"generator_id": "GEN2", "p_start": 3.0, "p_end": 4.0, "cost": 2.0},
            {"generator_id": "GEN2", "p_start": 4.0, "p_end": 4.5, "cost": 3.5},
            {"generator_id": "GEN3", "p_start": -3.0, "p_end": 0.0, "cost": 0.0},
            {"generator_id": "GEN3", "p_start": 0.0, "p_end": 3.0, "cost": 1.0},
            {"generator_id": "GEN4", "p_start": -7.0, "p_end": -3.5, "cost": 0.0},
        ]
    )


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
def transmission_lines_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "line_id": "LINE1",
                "node_from": "N1",
                "node_to": "N2",
                "reactance": 0.1,
                "F_max": 3.0,
            },
            {
                "line_id": "LINE2",
                "node_from": "N3",
                "node_to": "N2",
                "reactance": 0.05,
                "F_max": 1.0,
            },
            {
                "line_id": "LINE3",
                "node_from": "N1",
                "node_to": "N3",
                "reactance": 0.01,
                "F_max": 2.0,
            },
        ]
    ).set_index("line_id")


@pytest.fixture
def trafos_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "trafo_id": "TRAFO1",
                "node_from": "N2",
                "node_to": "N3",
                "reactance": 0.07,
                "F_max": 4.5,
                "F_min": np.nan,
                "tap_ratio": 1.1,
                "phase_shift": np.pi / 6,
            },
            {
                "trafo_id": "TRAFO2",
                "node_from": "N4",
                "node_to": "N3",
                "reactance": 0.07,
                "F_max": 2.5,
                "F_min": np.nan,
                "tap_ratio": 1.1,
                "phase_shift": np.pi / 6,
            },
            {
                "trafo_id": "TRAFO3",
                "node_from": "N4",
                "node_to": "N3",
                "reactance": 0.07,
                "F_max": 4.5,
                "F_min": np.nan,
                "tap_ratio": 1.0,
                "phase_shift": 0,
            },
        ]
    ).set_index("trafo_id")
