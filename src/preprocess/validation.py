import logging
from typing import Type

from pandas import DataFrame
from pandera import DataFrameModel, errors

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _stringify_schema_errors(schema_errors: errors.SchemaErrors) -> list[str]:
    error_parameters = [("SCHEMA", "error"), ("DATA", "check")]
    result = []
    for message_key, error_key in error_parameters:
        for error_data in schema_errors.message[message_key].values():
            result.extend(
                [f"error in {data['column']}: {data[error_key]}" for data in error_data]
            )
    return result


def _err_line_sep() -> str:
    return 80 * "-"


def _err_header(msg: str) -> str:
    return _err_line_sep() + "\n" + msg + "\n" + _err_line_sep()


def log_schema_errors(schema_errors: list[errors.SchemaErrors]) -> None:
    for e in schema_errors:
        logger.error(_err_header(f"{e.schema.name} Validation Errors:"))
        for err in _stringify_schema_errors(e):
            logger.error(err)
        logger.error(_err_line_sep())


def validate(
    data: list[tuple[Type[DataFrameModel], DataFrame]], stacktrace: bool = True
) -> None:
    schema_errors: list[errors.SchemaErrors] = []
    for data_model, df in data:
        try:
            data_model.validate(check_obj=df, lazy=True, inplace=True)
        except errors.SchemaErrors as e:
            schema_errors.append(e)
    if stacktrace:
        raise ExceptionGroup("Data Validation Exceptions", schema_errors)
    else:
        log_schema_errors(schema_errors)
