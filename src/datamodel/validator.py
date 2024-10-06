import abc
import logging

import pandas as pd

from src.utils.logs import func_log

logger = logging.getLogger(__name__)


class DatasetValidator(abc.ABC):
    """
    Abstract class for validating datasets.
    """

    def __init__(self, dataset_name: str) -> None:
        self.dataset_name = dataset_name

    @abc.abstractmethod
    def pre_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @abc.abstractmethod
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @abc.abstractmethod
    def post_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @func_log("Validating dataset {self.dataset_name} validation")
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.pre_validate(df)
        df = self.preprocess(df)
        df = self.post_validate(df)
        return df


class BranchesValidator(DatasetValidator):
    def pre_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def post_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError


class GeneratorsValidator(DatasetValidator):
    def pre_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def post_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError


class NodesValidator(DatasetValidator):
    def pre_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def post_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError
