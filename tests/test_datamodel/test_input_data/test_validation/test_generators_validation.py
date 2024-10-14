from typing import Any

import pandas as pd
import pandera.errors as err
import pytest
from numpy import nan
from src.datamodel.validator import GeneratorsValidator
from tests.test_datamodel.test_input_data.test_validation.utils import \
    check_schema_errors_reasons


def test_validate_correct_data(generators_df: pd.DataFrame) -> None:
    """Test if correct data are validated without errors."""
    check_schema_errors_reasons(GeneratorsValidator(), generators_df, [])


def test_validate_empty_data() -> None:
    """Test if correct empty data are validated without errors."""
    empty_df = pd.DataFrame(
        {
            "generator_id": [],
            "node": [],
            "P_min": [],
            "P_max": [],
        }
    ).astype(
        {
            "generator_id": str,
            "node": str,
            "P_min": float,
            "P_max": float,
        }
    )
    check_schema_errors_reasons(GeneratorsValidator(), empty_df, [])


@pytest.mark.parametrize(
    argnames=["col", "ndp"],
    argvalues=[
        pytest.param("generator_id", 1, id="generator_id one duplicate"),
        pytest.param("generator_id", 2, id="generator_id two duplicates"),
        pytest.param("generator_id", 3, id="generator_id three duplicates"),
    ],
)
def test_column_uniquness(generators_df: pd.DataFrame, col: str, ndp: int) -> None:
    """Test if error is raised when unique-required columns contain duplicates."""
    df = generators_df.copy()
    df.loc[1:ndp, col] = df.loc[0, col]
    check_schema_errors_reasons(
        GeneratorsValidator(),
        df,
        expected_error_reasons=[err.SchemaErrorReason.SERIES_CONTAINS_DUPLICATES],
    )


@pytest.mark.parametrize(
    argnames=["col", "val", "err_reasons"],
    argvalues=[
        pytest.param(
            "generator_id",
            True,
            [err.SchemaErrorReason.WRONG_DATATYPE],
            id="generator_id",
        ),
        pytest.param("node", 3.5, [err.SchemaErrorReason.WRONG_DATATYPE], id="node"),
        pytest.param(
            "P_min",
            "3.0",
            [
                err.SchemaErrorReason.WRONG_DATATYPE,
                err.SchemaErrorReason.CHECK_ERROR,
            ],
            id="P_min as string",
        ),
        pytest.param(
            "P_max",
            True,
            [
                err.SchemaErrorReason.WRONG_DATATYPE,
                err.SchemaErrorReason.DATAFRAME_CHECK,
            ],
            id="P_max as bool",
        ),
    ],
)
def test_wrong_type_err(
    generators_df: pd.DataFrame,
    col: str,
    val: Any,
    err_reasons: list[err.SchemaErrorReason],
) -> None:
    """Test if error for wrong data type is raised when it should be."""
    df = generators_df.copy()
    df[col] = df[col].astype(object)
    df.loc[1, col] = val
    check_schema_errors_reasons(
        GeneratorsValidator(),
        df,
        expected_error_reasons=err_reasons,
    )


@pytest.mark.parametrize(
    argnames=("cols", "err_reasons"),
    argvalues=[
        pytest.param(
            ["generator_id"],
            [err.SchemaErrorReason.SERIES_CONTAINS_NULLS],
            id="generator_id null test",
        ),
        pytest.param(
            ["node"], [err.SchemaErrorReason.SERIES_CONTAINS_NULLS], id="node null test"
        ),
        pytest.param(
            ["P_max"],
            [
                err.SchemaErrorReason.SERIES_CONTAINS_NULLS,
                err.SchemaErrorReason.DATAFRAME_CHECK,
            ],
            id="P_max null test",
        ),
        pytest.param(
            ["P_min"],
            [
                err.SchemaErrorReason.SERIES_CONTAINS_NULLS,
                err.SchemaErrorReason.DATAFRAME_CHECK,
            ],
            id="P_min null test",
        ),
        pytest.param(
            ["generator_id", "node"],
            [err.SchemaErrorReason.SERIES_CONTAINS_NULLS] * 2,
            id="multiple null columns test",
        ),
        pytest.param("cost", [], id="P_min null test"),
    ],
)
def test_not_nullable_columns(
    generators_df: pd.DataFrame,
    cols: str,
    err_reasons: list[err.SchemaErrorReason],
) -> None:
    """Test if error is raised if non-nullable columns contains null values."""
    df = generators_df.copy()
    df.loc[0, cols] = nan
    check_schema_errors_reasons(GeneratorsValidator(), df, err_reasons)


@pytest.mark.parametrize(
    argnames=["col", "err_reasons"],
    argvalues=[
        pytest.param(
            "generator_id",
            [err.SchemaErrorReason.COLUMN_NOT_IN_DATAFRAME],
            id="generator_id is required",
        ),
        pytest.param(
            "node",
            [err.SchemaErrorReason.COLUMN_NOT_IN_DATAFRAME],
            id="node is required",
        ),
        pytest.param(
            "P_min",
            [
                err.SchemaErrorReason.COLUMN_NOT_IN_DATAFRAME,
                err.SchemaErrorReason.CHECK_ERROR,
            ],
            id="P_min is required",
        ),
        pytest.param(
            "P_max",
            [
                err.SchemaErrorReason.COLUMN_NOT_IN_DATAFRAME,
                err.SchemaErrorReason.CHECK_ERROR,
            ],
            id="P_max is required",
        ),
        pytest.param(
            "cost",
            [],
            id="cost is not required",
        ),
    ],
)
def test_required_columns(
    generators_df: pd.DataFrame,
    col: str,
    err_reasons: list[err.SchemaErrorReason],
) -> None:
    df = generators_df.copy()
    df.drop(columns=[col], inplace=True)
    check_schema_errors_reasons(GeneratorsValidator(), df, err_reasons)


def test_pmin_pmax_relationship(generators_df: pd.DataFrame) -> None:
    """Test if for P_min > P_max validation error is raised."""
    df = generators_df.copy()
    df.loc[0, ["P_min", "P_max"]] = [3, 1]
    check_schema_errors_reasons(
        GeneratorsValidator(), df, [err.SchemaErrorReason.DATAFRAME_CHECK]
    )
