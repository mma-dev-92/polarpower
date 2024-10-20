from typing import Type

from pandas import DataFrame
from pandera import DataFrameModel
from pandera.errors import SchemaErrorReason, SchemaErrors


def check_schema_errors_reasons(
    data_model: Type[DataFrameModel],
    df: DataFrame,
    expected_error_reasons: list[SchemaErrorReason],
) -> None:
    try:
        data_model.validate(df, lazy=True)
    except SchemaErrors as e:
        reason_codes = [err.reason_code for err in e.schema_errors]
        assert (
            expected_error_reasons == reason_codes
        ), f"for input df: {df} expected {expected_error_reasons}, but got {reason_codes}"
    else:
        assert not expected_error_reasons, "exception was not raised, but it should be"
