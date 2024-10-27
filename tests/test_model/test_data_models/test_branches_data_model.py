import pandas as pd
from src.model.data_models.branches_data_model import BranchesDataModel
from tests.test_model.test_data_models.utils import check_schema_errors_reasons


def test_validate_branches_data_model_on_correct_input(
    branches_lines_and_trafos_df: pd.DataFrame,
    nodes_df: pd.DataFrame,
) -> None:
    check_schema_errors_reasons(
        BranchesDataModel,
        branches_lines_and_trafos_df,
        [],
        context={"nodes_index": nodes_df.index},
    )


def test_validate_transformers_data_model_on_empty_data() -> None:
    empty_df = (
        pd.DataFrame(
            {
                "branch_id": [],
                "branch_type": [],
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
                "branch_id": str,
                "branch_type": str,
                "node_from": str,
                "node_to": str,
                "reactance": float,
                "F_max": float,
                "F_min": float,
                "tap_ratio": float,
                "phase_shift": float,
            }
        )
        .set_index("branch_id")
    )
    check_schema_errors_reasons(
        BranchesDataModel, empty_df, [], context={"nodes_index": []}
    )
