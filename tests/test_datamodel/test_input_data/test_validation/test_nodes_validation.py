import pandas as pd
import pandera.errors as err
import pytest
from numpy import nan
from src.datamodel.validator import NodesValidator
from tests.test_datamodel.test_input_data.test_validation.utils import \
    check_schema_errors_reasons


def test_validation_on_correct_input(nodes_df: pd.DataFrame) -> None:
    """Test if no validation errors will be raised for correct input."""
    try:
        NodesValidator().validate(nodes_df)
    except err.SchemaErrors:
        pytest.fail()


def test_validation_on_correct_empty_data() -> None:
    """Test validation on empty dataframe (with correct types)."""
    empty_df = pd.DataFrame({"node_id": [], "P_demand": []}).astype(
        {"node_id": str, "P_demand": float}
    )
    try:
        NodesValidator().validate(empty_df)
    except err.SchemaErrors:
        pytest.fail()


@pytest.mark.parametrize(
    argnames=["col", "ndp"],
    argvalues=[
        pytest.param("node_id", 1, id="node_id with one duplicate"),
        pytest.param("node_id", 2, id="node_id with two duplicates"),
        pytest.param("node_id", 3, id="node_id with three duplicates"),
    ],
)
def test_column_uniquness(nodes_df: pd.DataFrame, col: str, ndp: int) -> None:
    """Test behavior for node_id column with duplicates."""
    df = nodes_df.copy()
    df.loc[1:ndp, col] = df.loc[0, col]
    check_schema_errors_reasons(
        NodesValidator(),
        df,
        expected_error_reasons=[
            err.SchemaErrorReason.SERIES_CONTAINS_DUPLICATES,
        ],
    )


@pytest.mark.parametrize(
    argnames=["col", "nna", "err_reasons"],
    argvalues=[
        pytest.param(
            "node_id",
            slice(0, 0),
            [err.SchemaErrorReason.SERIES_CONTAINS_NULLS],
            id="node_id one null value",
        ),
        pytest.param(
            "node_id",
            slice(0, 1),
            [
                err.SchemaErrorReason.SERIES_CONTAINS_NULLS,
                err.SchemaErrorReason.SERIES_CONTAINS_DUPLICATES,
            ],
            id="node_id two null values",
        ),
        pytest.param(
            "node_id",
            slice(None),
            [
                err.SchemaErrorReason.SERIES_CONTAINS_NULLS,
                err.SchemaErrorReason.SERIES_CONTAINS_DUPLICATES,
            ],
            id="node_id all null values",
        ),
        pytest.param("P_demand", slice(0, 2), [], id="P_demand with three null values"),
    ],
)
def test_nulls(
    nodes_df: pd.DataFrame,
    col: str,
    nna: int | slice,
    err_reasons: list[err.SchemaErrorReason],
) -> None:
    """
    Test behavior in case node_id column contains null values.
    Explanation: many NaN values are treated as duplicates by pandera.
    """
    df = nodes_df.copy()
    df.loc[nna, col] = nan
    check_schema_errors_reasons(NodesValidator(), df, err_reasons)


@pytest.mark.parametrize(
    argnames=["cols", "err_reasons"],
    argvalues=[
        pytest.param(
            ["node_id", "P_demand"],
            [
                err.SchemaErrorReason.WRONG_DATATYPE,
                err.SchemaErrorReason.WRONG_DATATYPE,
            ],
            id="wrong datatype for both columns",
        ),
        pytest.param(
            ["node_id"],
            [err.SchemaErrorReason.WRONG_DATATYPE],
            id="node_id wrong datatype",
        ),
        pytest.param(
            ["P_demand"],
            [err.SchemaErrorReason.WRONG_DATATYPE],
            id="P_demand wrong datatype",
        ),
    ],
)
def test_datatypes(
    nodes_df: pd.DataFrame, cols: list[str], err_reasons: list[err.SchemaErrorReason]
) -> None:
    df = nodes_df.copy()
    for col in cols:
        df[col] = df[col].astype(object)
        df.loc[1, col] = True
    check_schema_errors_reasons(NodesValidator(), df, err_reasons)


def test_multiple_validation_fails(nodes_df: pd.DataFrame) -> None:
    """Test if a combination of validation errors will be detected."""
    df = nodes_df.copy()
    df["node_id"] = df["node_id"].astype(object)
    df["P_demand"] = df["P_demand"].astype(object)
    df.loc[2, "node_id"] = "N1"
    df.loc[4, "node_id"] = "N1"
    df.loc[3, "node_id"] = True
    df.loc[2, "P_demand"] = False
    check_schema_errors_reasons(
        NodesValidator(),
        df,
        expected_error_reasons=[
            err.SchemaErrorReason.SERIES_CONTAINS_DUPLICATES,
            err.SchemaErrorReason.WRONG_DATATYPE,
            err.SchemaErrorReason.WRONG_DATATYPE,
        ],
    )
