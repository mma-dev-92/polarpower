from typing import Type

from pandas import DataFrame
from pandera.errors import SchemaErrorReason, SchemaErrors
from src.model.data_models import DataFrameModelWithContext


def check_schema_errors_reasons(
    data_model: Type[DataFrameModelWithContext],
    df: DataFrame,
    expected_error_reasons: list[SchemaErrorReason],
    context: dict | None = None,
) -> None:
    try:
        data_model.validate(df, lazy=True, context=context or dict())
    except SchemaErrors as e:
        reason_codes = [err.reason_code for err in e.schema_errors]
        assert (
            expected_error_reasons == reason_codes
        ), f"for input df: {df} expected {expected_error_reasons}, but got {reason_codes}"
    else:
        assert not expected_error_reasons, "exception was not raised, but it should be"
