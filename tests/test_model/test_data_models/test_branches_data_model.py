from typing import Any

import pandas as pd
import pytest
from numpy import inf, nan, pi

from src.model.data_models.branches_data_model import (
    BranchesDataModel, TransformersDataModel, TransmissionLinesDataModel)
from src.model.data_models.utils import (err_finite_check, err_foreign_key,
                                         err_ge_check)
from tests.test_model.test_data_models import utils
from tests.test_model.test_data_models.utils import (
    check_error_messages, check_schema_errors_reasons)


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


def test_validate_transformers_data_model_on_empty_data(
    trafos_df: pd.DataFrame,
) -> None:
    empty_df = utils.clear_dataframe(trafos_df)
    check_schema_errors_reasons(
        TransformersDataModel, empty_df, [], context={"nodes_index": []}
    )


def test_validate_transmission_lines_data_on_empty_data(
    transmission_lines_df: pd.DataFrame,
) -> None:
    empty_df = utils.clear_dataframe(transmission_lines_df)
    check_schema_errors_reasons(
        TransmissionLinesDataModel, empty_df, [], context={"nodes_index": []}
    )


@pytest.mark.parametrize(
    argnames=("vals", "errors"),
    argvalues=(
        pytest.param(
            {("LINE1", "node_from"): "NON_EXISTING"},
            [err_foreign_key("node_from")],
            id="Not-existing node from",
        ),
        pytest.param(
            {("LINE1", "node_to"): "NON_EXISTING"},
            [err_foreign_key("node_to")],
            id="Not-existing node to",
        ),
        pytest.param(
            {
                ("LINE1", "node_from"): "HAKUNA MATATA",
                ("LINE1", "node_to"): "NON_EXISTING",
            },
            [err_foreign_key("node_to"), err_foreign_key("node_from")],
            id="Not-existing node from and node to",
        ),
        pytest.param(
            {
                ("LINE1", "node_from"): "HAKUNA MATATA",
                ("LINE2", "node_to"): "HAKUNA MATATA",
                ("LINE1", "node_to"): "NON_EXISTING",
                ("LINE3", "node_from"): "HAKUNA MATATA",
            },
            [err_foreign_key("node_to"), err_foreign_key("node_from")],
            id="Many non-existing nodes from and to",
        ),
        pytest.param(
            {("LINE1", "reactance"): inf},
            [err_finite_check("reactance", null=False)],
            id="Infinite reactance",
        ),
        pytest.param(
            {("LINE1", "F_min"): inf},
            [
                err_finite_check("F_min", null=True),
                err_ge_check(ge="F_max", le="F_min", null=True),
            ],
            id="Infinite F_min",
        ),
        pytest.param(
            {("LINE1", "F_max"): inf},
            [err_finite_check("F_max", null=False)],
            id="Infinite F_max",
        ),
        pytest.param(
            {
                ("LINE1", "F_max"): 7.0,
                ("LINE1", "F_min"): nan,
            },
            [],
            id="F_min set to NaN",
        ),
        pytest.param(
            {
                ("LINE1", "F_max"): 7.0,
                ("LINE1", "F_min"): 7.001,
            },
            [err_ge_check(ge="F_max", le="F_min", null=True)],
            id="F_min grater than F_max",
        ),
    ),
)
def test_branches_error_messages(
    vals: dict[tuple[str, str], Any],
    errors: list[str],
    transmission_lines_df: pd.DataFrame,
    nodes_df: pd.DataFrame,
) -> None:
    for (idx, col), val in vals.items():
        transmission_lines_df.loc[idx, col] = val

    check_error_messages(
        data_model=BranchesDataModel,
        df=transmission_lines_df,
        col_to_err_msg=errors,
        context={"nodes_index": nodes_df.index},
    )


@pytest.mark.parametrize(
    argnames=("vals", "errors"),
    argvalues=(
        pytest.param(
            {("TRAFO1", "tap_ratio"): inf},
            [
                err_finite_check("tap_ratio", null=True),
                f"in_range(0.0, {2 * pi})",
            ],
            id="Infinite tap ratio",
        ),
        pytest.param(
            {("TRAFO1", "phase_shift"): inf},
            [
                err_finite_check("phase_shift", null=True),
                f"in_range(0.0, {pi  / 2})",
            ],
            id="Infinite phase shift",
        ),
    ),
)
def test_transformers_error_messages(
    vals: dict[tuple[str, str], float],
    errors: list[str],
    trafos_df: pd.DataFrame,
    nodes_df: pd.DataFrame,
) -> None:
    for (idx, col), val in vals.items():
        trafos_df.loc[idx, col] = val

    check_error_messages(
        data_model=TransformersDataModel,
        df=trafos_df,
        col_to_err_msg=errors,
        context={"nodes_index": nodes_df.index},
    )
