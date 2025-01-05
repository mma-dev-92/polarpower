import logging

from pandera import errors
from rich.console import Console
from rich.logging import RichHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RichHandler()
logger.addHandler(handler)

console = Console()

ERR_LINE_SEP = 80 * "-"


def stringify_schema_errors(schema_errors: errors.SchemaErrors) -> list[tuple[str, str]]:
    error_types = [("SCHEMA", "error"), ("DATA", "check")]

    result = list()
    for section, key in error_types:
        section_errors = schema_errors.message.get(section, {})
        for error_details in section_errors.values():
            for error_detail in error_details:
                column_name = error_detail.get("column", "Unknown column")
                error_info = error_detail.get(key, "No error info")
                result.append((column_name, error_info))

    return result


def log_schema_errors(schema_errors: errors.SchemaErrors) -> None:
    console.rule(f"{schema_errors.schema.name} Validation Errors", style="red")

    for col_name, error_info in stringify_schema_errors(schema_errors):
        err_msg = f"Error in [bold]{col_name}[/]: {error_info}"
        logger.error(err_msg)

    console.rule(style="red")


def log_error(msg: str, dataset_name: str) -> None:
    console.rule(f"{dataset_name} Validation Error", style="red")
    logger.error(msg)
    console.rule(style="red")
