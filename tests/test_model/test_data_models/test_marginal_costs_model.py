import pandas as pd
import pytest
from numpy import inf

import src.model.data_models.utils as u
import tests.test_model.test_data_models.utils as tu
from src.model.data_models.marginal_costs_model import MarginalCostsDataModel
from tests.test_model.test_data_models import utils


def test_correct_data(
    marginal_costs_df: pd.DataFrame, generators_df: pd.DataFrame
) -> None:
    tu.check_schema_errors_reasons(
        data_model=MarginalCostsDataModel,
        df=marginal_costs_df,
        expected_error_reasons=[],
        context={"generators_df": generators_df},
    )


def test_empty_data(
    marginal_costs_df: pd.DataFrame, generators_df: pd.DataFrame
) -> None:
    empty_df = utils.clear_dataframe(marginal_costs_df)
    empty_generators_df = utils.clear_dataframe(generators_df)
    tu.check_schema_errors_reasons(
        data_model=MarginalCostsDataModel,
        df=empty_df,
        expected_error_reasons=[],
        context={"generators_df": empty_generators_df},
    )


def test_invalid_generator_id(
    marginal_costs_df: pd.DataFrame, generators_df: pd.DataFrame
) -> None:
    marginal_costs_df.loc[0, "generator_id"] = "NON-EXISTING-GEN-ID"
    tu.check_error_messages(
        data_model=MarginalCostsDataModel,
        df=marginal_costs_df,
        col_to_err_msg=[
            u.err_foreign_key(fk_col="generator_id"),
            u.err_prange(),  # prange is incorrect for non-existing generator
        ],
        context={"generators_df": generators_df},
    )


def test_finite_cost(
    marginal_costs_df: pd.DataFrame, generators_df: pd.DataFrame
) -> None:
    marginal_costs_df.loc[3, "cost"] = inf
    tu.check_error_messages(
        data_model=MarginalCostsDataModel,
        df=marginal_costs_df,
        col_to_err_msg=[u.err_finite_check("cost", null=False)],
        context={"generators_df": generators_df},
    )


@pytest.mark.parametrize(
    argnames=("vals", "errors"),
    argvalues=(
        pytest.param(
            {(0, "p_start"): -3.0},
            [u.err_prange()],
            id="too small first p_start",
        ),
        pytest.param(
            {(0, "p_start"): -1.5},
            [u.err_prange()],
            id="invalid first p_start",
        ),
        pytest.param(
            {(0, "p_end"): 1.0},
            [u.err_prange()],
            id="too big first p_end",
        ),
        pytest.param(
            {(0, "p_end"): -1.0},
            [u.err_prange()],
            id="too small first p_end",
        ),
        pytest.param(
            {(1, "p_end"): 2.5},
            [u.err_prange()],
            id="too small last p_end",
        ),
        pytest.param(
            {(1, "p_end"): 3.5},
            [u.err_prange()],
            id="too big last p_end",
        ),
        pytest.param(
            {(2, "p_end"): 4.1, (3, "p_start"): 3.9},
            [u.err_prange()],
            id="overlapping power intervals",
        ),
        pytest.param(
            {(0, "cost"): 10.0},
            [u.err_non_monotonic_merit_order()],
            id="one generator decreasing merit order costs",
        ),
        pytest.param(
            {
                (0, "cost"): 10.0,
                (2, "cost"): 15.0,
                (4, "cost"): 40.0,
            },
            [u.err_non_monotonic_merit_order()],
            id="three generators decreasing merit order costs",
        ),
    ),
)
def test_error_messages(
    marginal_costs_df: pd.DataFrame,
    generators_df: pd.DataFrame,
    vals: dict[tuple[int, str], float],
    errors: list[str],
) -> None:

    for (idx, col), v in vals.items():
        marginal_costs_df.loc[idx, col] = v

    tu.check_error_messages(
        data_model=MarginalCostsDataModel,
        df=marginal_costs_df,
        col_to_err_msg=errors,
        context={"generators_df": generators_df},
    )
