import pandas as pd
from src.preprocess.data_models.generators_data_model import \
    GeneratorsDataModel
from tests.test_preprocess.test_data_models.utils import \
    check_schema_errors_reasons


def test_validation_on_correct_input(generators_df: pd.DataFrame) -> None:
    """Test if correct data are validated without errors."""
    check_schema_errors_reasons(
        data_model=GeneratorsDataModel,
        df=generators_df,
        expected_error_reasons=[],
    )


def test_validate_empty_data() -> None:
    """Test if correct empty data are validated without errors."""
    empty_df = (
        pd.DataFrame(
            {
                "generator_id": [],
                "node_id": [],
                "P_min": [],
                "P_max": [],
            }
        ).astype(
            {
                "generator_id": str,
                "node_id": str,
                "P_min": float,
                "P_max": float,
            }
        )
    ).set_index("generator_id")
    check_schema_errors_reasons(GeneratorsDataModel, empty_df, [])
