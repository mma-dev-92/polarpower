from numpy import inf
import pandas as pd
import pytest

from src.model.data_models.nodes_data_model import NodesDataModel
from src.model.data_models.utils import err_finite_check
from tests.test_model.test_data_models import utils
from tests.test_model.test_data_models.utils import check_error_messages, check_schema_errors_reasons


def test_validation_on_correct_input(nodes_df: pd.DataFrame) -> None:
    """Test if no validation errors will be raised for correct input."""
    check_schema_errors_reasons(
        data_model=NodesDataModel,
        df=nodes_df,
        expected_error_reasons=[],
    )


def test_validation_on_correct_empty_data(nodes_df: pd.DataFrame) -> None:
    """Test validation on empty dataframe (with correct types)."""
    empty_df = utils.clear_dataframe(nodes_df)
    check_schema_errors_reasons(
        data_model=NodesDataModel,
        df=empty_df,
        expected_error_reasons=[],
    )


@pytest.mark.parametrize(
    argnames=("vals", "errors"),
    argvalues=(
        pytest.param(
            {("N1", "P_demand"): inf},
            [err_finite_check(col_name="P_demand", null=True)],
            id="Infinite demand for one node",
        ),
        pytest.param(
            {
                ("N1", "P_demand"): inf,
                ("N2", "P_demand"): inf,
                ("N5", "P_demand"): inf,
            },
            [err_finite_check(col_name="P_demand", null=True)],
            id="Infinite demand for many nodes"
        ),
    )
)
def test_error_messages(vals: dict[tuple[str, str], float], errors: list[str], nodes_df: pd.DataFrame) -> None:
    for (idx, col), val in vals.items():
        nodes_df.loc[idx, col] = val

    check_error_messages(
        data_model=NodesDataModel,
        df=nodes_df,
        col_to_err_msg=errors,

    )
