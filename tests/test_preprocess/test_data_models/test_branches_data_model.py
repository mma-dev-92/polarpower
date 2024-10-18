import pandas as pd
from src.preprocess.data_models.branches_data_model import BranchesDataModel
from tests.test_preprocess.test_data_models.utils import \
    check_schema_errors_reasons


def test_validate_on_correct_input_only_lines(
    branches_only_lines_df: pd.DataFrame,
) -> None:
    check_schema_errors_reasons(BranchesDataModel, branches_only_lines_df, [])


def test_validate_on_correct_input_lines_and_branches(
    branches_lines_and_trafos_df: pd.DataFrame,
) -> None:
    check_schema_errors_reasons(BranchesDataModel, branches_lines_and_trafos_df, [])


def test_validate_on_correct_input_only_trafos(
    branches_only_trafos_df: pd.DataFrame,
) -> None:
    check_schema_errors_reasons(BranchesDataModel, branches_only_trafos_df, [])


def test_validate_empty_data() -> None:
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
                "phase_shift_min": [],
                "phase_shift_max": [],
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
                "phase_shift_min": float,
                "phase_shift_max": float,
            }
        )
        .set_index("branch_id")
    )
    check_schema_errors_reasons(BranchesDataModel, empty_df, [])


def test_datatypes_validation() -> None:
    pass


def test_uniquness_validation() -> None:
    pass


def test_null_values_validation() -> None:
    pass


def test_missing_columns_validation() -> None:
    pass


def test_trafos_parameters_validation() -> None:
    pass
