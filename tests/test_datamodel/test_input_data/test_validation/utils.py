from pandas import DataFrame
from pandera.errors import SchemaErrorReason, SchemaErrors
from src.datamodel.validator import DatasetValidator


def check_schema_errors_reasons(
    validator: DatasetValidator,
    df: DataFrame,
    expected_error_reasons: list[SchemaErrorReason],
) -> None:
    try:
        validator.validate(df)
    except SchemaErrors as e:
        reason_codes = [err.reason_code for err in e.schema_errors]
        assert (
            expected_error_reasons == reason_codes
        ), f"for input df: {df} expected {expected_error_reasons}, but got {reason_codes}"
    else:
        assert not expected_error_reasons, "exception was not raised, but it should be"
