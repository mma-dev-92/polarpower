from typing import Any

from pandera import DataFrameModel
from pandera.typing.common import DataFrameBase


class DataFrameModelWithContext(DataFrameModel):
    """DataFrameModel wrapper with dynamic validation parameters."""

    _context = dict()

    @classmethod
    def validate(cls, *args, context: dict[Any, Any] | None, **kwargs) -> DataFrameBase:
        cls._context = context or dict()
        try:
            result = super().validate(*args, **kwargs)
        finally:
            cls._context = dict()
        return result

    @classmethod
    def get_context(cls, context_parameter: str) -> Any:
        if not context_parameter in cls._context:
            raise KeyError(
                f"given context parameter: {context_parameter} "
                "was not provided as validation context"
            )
        return cls._context.get(context_parameter)
