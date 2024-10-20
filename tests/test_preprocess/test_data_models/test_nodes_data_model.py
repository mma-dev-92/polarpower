import pandas as pd
import pytest
from pandas.io import pytables
from src.preprocess.data_models.nodes_data_model import NodesDataModel
from src.preprocess.validation import validation_logs
from tests.test_preprocess.test_data_models.utils import \
    check_schema_errors_reasons


def test_validation_on_correct_input(nodes_df: pd.DataFrame) -> None:
    """Test if no validation errors will be raised for correct input."""
    check_schema_errors_reasons(
        data_model=NodesDataModel,
        df=nodes_df,
        expected_error_reasons=[],
    )


def test_validation_on_correct_empty_data() -> None:
    """Test validation on empty dataframe (with correct types)."""
    empty_df = (
        pd.DataFrame({"node_id": [], "P_demand": []})
        .astype({"node_id": str, "P_demand": float})
        .set_index("node_id")
    )
    check_schema_errors_reasons(
        data_model=NodesDataModel,
        df=empty_df,
        expected_error_reasons=[],
    )


def test_failure(nodes_df: pd.DataFrame) -> None:
    df = nodes_df.copy()
    df["P_demand"] = df["P_demand"].astype(object)
    df.loc["N2", "P_demand"] = True
