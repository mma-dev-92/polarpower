from typing import Optional
import pandas as pd
from pathlib import Path
import logging

from src.utils.logs import func_log

logger = logging.getLogger(__name__)


class FileLoaderError(Exception):
    pass


class FileLoader:
    """
    A class responsible for loading datasets from various file formats.
    """

    LOAD_METHODS = {
        '.csv': lambda path: pd.read_csv(path, sep=';', index_col=None),
        '.xlsx': lambda path, sn=0: pd.read_excel(path, sheet_name=sn),
        '.feather': lambda path: pd.read_feather(path),
    }

    def __init__(self, path: Path, sheet_name: Optional[str]) -> None:
        self.path = path
        self.sheet_name: Optional[str] = sheet_name
        self.validate_path()

    @func_log("Validating file path {self.path}")
    def validate_path(self) -> None:
        if not self.path.exists():
            raise FileLoaderError(
                f"Provided path: {self.path} does not exist."
            )

        if not self.path.is_file():
            raise FileLoaderError(
                f"Provided path: {self.path} is not a valid file."
            )

        if self.path.suffix not in self.LOAD_METHODS:
            supported_formats = ', '.join(self.LOAD_METHODS.keys())
            raise FileLoaderError(
                f"Unsupported file format for {self.path}. "
                f"Supported formats are {supported_formats}."
            )

    @func_log("Loading dataset from {self.path}")
    def load(self) -> pd.DataFrame:
        try:
            if self.path.suffix == '.xlsx':
                df = self.LOAD_METHODS[self.path.suffix](
                    self.path, sn=self.sheet_name
                )
            else:
                df = self.LOAD_METHODS[self.path.suffix](self.path)
            return df
        except Exception as e:
            raise FileLoaderError(f"Failed to load file from {self.path}: {e}")
