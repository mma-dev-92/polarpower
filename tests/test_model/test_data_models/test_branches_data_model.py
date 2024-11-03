import pandas as pd
from src.model.data_models.branches_data_model import (
    TransformersDataModel, TransmissionLinesDataModel)
from tests.test_model.test_data_models.utils import check_schema_errors_reasons


def test_validate_transmission_lines_data_model_on_correct_input(
    transmission_lines_df: pd.DataFrame,
    nodes_df: pd.DataFrame,
) -> None:
    check_schema_errors_reasons(
        TransmissionLinesDataModel,
        transmission_lines_df,
        [],
        context={"nodes_index": nodes_df.index},
    )


def test_validate_transformers_data_model_on_correct_input(
    trafos_df: pd.DataFrame,
    nodes_df: pd.DataFrame,
) -> None:
    check_schema_errors_reasons(
        TransformersDataModel,
        trafos_df,
        [],
        context={"nodes_index": nodes_df.index},
    )


def test_validate_transformers_data_model_on_empty_data() -> None:
    empty_df = (
        pd.DataFrame(
            {
                "trafo_id": [],
                "node_from": [],
                "node_to": [],
                "reactance": [],
                "F_max": [],
                "F_min": [],
                "tap_ratio": [],
                "phase_shift": [],
            },
        )
        .astype(
            {
                "trafo_id": str,
                "node_from": str,
                "node_to": str,
                "reactance": float,
                "F_max": float,
                "F_min": float,
                "tap_ratio": float,
                "phase_shift": float,
            }
        )
        .set_index("trafo_id")
    )
    check_schema_errors_reasons(
        TransformersDataModel, empty_df, [], context={"nodes_index": []}
    )


def test_validate_transmission_lines_data_on_empty_data() -> None:
    empty_df = (
        pd.DataFrame(
            {
                "line_id": [],
                "node_from": [],
                "node_to": [],
                "reactance": [],
                "F_max": [],
            },
        )
        .astype(
            {
                "line_id": str,
                "node_from": str,
                "node_to": str,
                "reactance": float,
                "F_max": float,
            }
        )
        .set_index("line_id")
    )
    check_schema_errors_reasons(
        TransmissionLinesDataModel, empty_df, [], context={"nodes_index": []}
    )
