import pandas as pd
import pytest
from numpy import inf

import src.model.data_models.utils as u
import tests.test_model.test_data_models.utils as tu
from src.model.data_models.generators_data_model import GeneratorsDataModel


def test_validation_on_correct_input(
    generators_df: pd.DataFrame,
    nodes_df: pd.DataFrame,
) -> None:
    """Test if correct data are validated without errors."""
    tu.check_schema_errors_reasons(
        data_model=GeneratorsDataModel,
        df=generators_df,
        expected_error_reasons=[],
        context={"nodes_index": nodes_df.index},
    )


def test_validate_empty_data(
    generators_df: pd.DataFrame,
) -> None:
    """Test if correct empty data are validated without errors."""
    empty_df = tu.clear_dataframe(generators_df)
    tu.check_schema_errors_reasons(
        GeneratorsDataModel, empty_df, [], context={"nodes_index": []}
    )


@pytest.mark.parametrize(
    argnames=("vals", "errors"),
    argvalues=(
        (
            pytest.param(
                {("GEN1", "node_id"): "NON-EXISTING-NODE-ID"},
                [u.err_foreign_key(fk_col="node_id")],
                id="One non-existing node",
            ),
            pytest.param(
                {
                    ("GEN1", "node_id"): "NON-EXISTING-NODE-ID",
                    ("GEN2", "node_id"): "NON-EXISTING-NODE-ID",
                    ("GEN3", "node_id"): "NON-EXISTING-NODE-ID-2",
                },
                [u.err_foreign_key(fk_col="node_id")],
                id="Three non-existing nodes",
            ),
            pytest.param(
                {("GEN1", "P_min"): inf},
                [
                    u.err_finite_check("P_min", null=False),
                    u.err_ge_check("P_max", "P_min", null=False),
                ],
                id="One P_min set to inf.",
            ),
            pytest.param(
                {("GEN1", "P_max"): inf},
                [u.err_finite_check("P_max", null=False)],
                id="One P_max set to inf.",
            ),
            pytest.param(
                {
                    ("GEN1", "P_min"): inf,
                    ("GEN1", "P_max"): inf,
                },
                [
                    u.err_finite_check("P_min", null=False),
                    u.err_finite_check("P_max", null=False),
                ],
                id="P_min and P_max for one generator set to inf.",
            ),
            pytest.param(
                {
                    ("GEN1", "P_min"): inf,
                    ("GEN2", "P_max"): inf,
                },
                [
                    u.err_finite_check("P_min", null=False),
                    u.err_finite_check("P_max", null=False),
                    u.err_ge_check("P_max", "P_min", null=False),
                ],
                id="P_min and P_max for different generators set to inf.",
            ),
        )
    ),
)
def test_error_messages(
    vals: dict[tuple[str, str], float],
    errors: list[str],
    generators_df: pd.DataFrame,
    nodes_df: pd.DataFrame,
) -> None:
    for (idx, col), val in vals.items():
        generators_df.loc[idx, col] = val

    tu.check_error_messages(
        data_model=GeneratorsDataModel,
        df=generators_df,
        col_to_err_msg=errors,
        context={"nodes_index": nodes_df.index},
    )
