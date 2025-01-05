from typing import Type

import pandas as pd
import pytest
from pandas import DataFrame
from pandera.errors import SchemaErrorReason, SchemaErrors

from src.model.data_models import DataFrameModelWithContext
from src.model.data_models.error_logs import stringify_schema_errors


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


def check_error_messages(
    data_model: Type[DataFrameModelWithContext],
    df: DataFrame,
    col_to_err_msg: list[str],
    context: dict | None = None,
    check_explicite: bool = True,
) -> None:
    """Verify that all required error messages were raised (and maybe more)."""
    try:
        data_model.validate(df, lazy=True, context=context or dict())
    except SchemaErrors as schema_errors:
        stringified_errors = [err[1] for err in stringify_schema_errors(schema_errors)]
        not_called = set(col_to_err_msg).difference(stringified_errors)
        called_unexpected = set(stringified_errors).difference(col_to_err_msg)
        if len(not_called) > 0:
            not_raised_errors = ",\n".join([f"* {err}" for err in not_called])
            pytest.fail(f"\nmissing error message(s) are:\n{not_raised_errors}")
        if check_explicite and len(called_unexpected) > 0:
            unexpected_errors = ",\n".join([f"* {err}" for err in called_unexpected])
            pytest.fail(f"\nunexpected error message(s):\n{unexpected_errors}")
    else:
        assert len(col_to_err_msg) == 0, f"no error has been raised, but expected at least {len(col_to_err_msg)}"


def clear_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df.iloc[0:0]
