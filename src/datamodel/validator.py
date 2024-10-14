import abc
import logging
from typing import Optional

import numpy as np
import pandas as pd
import pandera as pa
from src.datamodel import LINE, TRAFO
from src.utils.logs import func_log

logger = logging.getLogger(__name__)


class DatasetValidator(abc.ABC):
    """
    Abstract class for validating separate datasets.
    """

    def __init__(self, dataset_name: str) -> None:
        self.dataset_name = dataset_name

    def _err_msg(self, msg: str) -> str:
        return f"{self.dataset_name} error: {msg}."

    @abc.abstractmethod
    @func_log("Validating dataset {self.dataset_name}")
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError


class BranchesValidator(DatasetValidator):

    def __init__(self) -> None:
        super().__init__(dataset_name="branches")

    def _positive_float_col(
        self, col: str, default: Optional[float] = None
    ) -> pa.Column:
        return pa.Column(
            dtype=pa.Float,
            checks=[
                pa.Check(
                    lambda fmax: fmax > 0,
                    error=self._err_msg(f"'{col}' value must be positive"),
                ),
            ],
            default=default,
        )

    def _phase_shift_col(self, col: str, default: Optional[float] = None) -> pa.Column:
        return pa.Column(
            dtype=pa.Float,
            checks=[
                pa.Check(
                    lambda x: 0 <= x <= np.pi / 2,
                    error=self._err_msg(
                        f"'{col}' must be a number between 0 " "and pi/2 (if provided)"
                    ),
                )
            ],
            required=False,
            nullable=True,
            default=default,
        )

    def _check_col_for_line_branches(self, col: str, val: float) -> pa.Check:
        return pa.Check(
            lambda df: (
                np.all(df[df["type"] == LINE][col] == val)
                if not np.isnan(val)
                else np.all(df[df["type"] == LINE].isna())
            ),
            error=self._err_msg(
                f"for {LINE} branch '{col}' must be equal to {val} " "(if provided)"
            ),
        )

    @staticmethod
    def thermal_limits_refinment(df: pd.DataFrame) -> pd.DataFrame:
        mask = df["F_min"].isna()
        df.loc[mask, "F_min"] = -df.loc[mask, "F_max"]
        return df

    def get_schema(self) -> pa.DataFrameSchema:
        return pa.DataFrameSchema(
            {
                "branch_id": pa.Column(dtype=pa.String, unique=True),
                "type": pa.Column(
                    dtype=pa.String,
                    checks=[
                        pa.Check(
                            lambda t: t.isin([LINE, TRAFO]),
                            error=self._err_msg(
                                f"each branch 'type' must be either "
                                f"'{LINE}' or '{TRAFO}'"
                            ),
                        ),
                    ],
                ),
                "bus_from": pa.Column(dtype=pa.String),
                "bus_to": pa.Column(dtype=pa.String),
                "reactance": self._positive_float_col(col="reactance"),
                "F_max": self._positive_float_col(col="F_max"),
                "F_min": pa.Column(
                    dtype=pa.Float,
                    checks=[
                        pa.Check(
                            lambda fmin: fmin < 0,
                            error=self._err_msg(
                                "'F_min' value must be negative " "(if provided)"
                            ),
                        ),
                    ],
                    required=False,
                    nullable=True,
                    default=np.nan,
                ),
                "tap_ratio": self._positive_float_col("tap_ratio", default=1.0),
                "phase_shift": self._phase_shift_col("phase_shift", default=0.0),
                "phase_shift_min": self._phase_shift_col("phase_shift_min"),
                "phase_shift_max": self._phase_shift_col("phase_shift_max"),
            },
            checks=[
                self._check_col_for_line_branches("tap_ratio", 1.0),
                self._check_col_for_line_branches("phase_shift", 0.0),
                self._check_col_for_line_branches("phase_shift_min", np.nan),
                self._check_col_for_line_branches("phase_shift_max", np.nan),
                pa.Check(
                    lambda df: not (df["bus_from"] == df["bus_to"]).any(),
                    error=self._err_msg("'bus_from' and 'bus_to' must be different"),
                ),
            ],
            name="Branches Data Schema",
        )

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        schema = self.get_schema()
        df = schema.validate(df, lazy=True)
        df = self.thermal_limits_refinment(df)
        return df


class GeneratorsValidator(DatasetValidator):

    def __init__(self) -> None:
        super().__init__(dataset_name="generators")

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        return pa.DataFrameSchema(
            columns={
                "generator_id": pa.Column(dtype=pa.String, unique=True),
                "node": pa.Column(dtype=pa.String),
                "P_min": pa.Column(dtype=pa.Float),
                "P_max": pa.Column(dtype=pa.Float),
                "cost": pa.Column(
                    dtype=pa.Float, nullable=True, required=False, default=0.0
                ),
            },
            checks=[
                pa.Check(
                    lambda df: (df["P_min"] <= df["P_max"]).all(),
                    error=self._err_msg("'P_min' must be lesser or equal than 'P_max'"),
                )
            ],
            name="Generators Data Schema",
        ).validate(df, lazy=True)


class NodesValidator(DatasetValidator):

    def __init__(self) -> None:
        super().__init__(dataset_name="nodes")

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        return pa.DataFrameSchema(
            {
                "node_id": pa.Column(dtype=pa.String, unique=True),
                "P_demand": pa.Column(dtype=pa.Float, nullable=True, default=0.0),
            }
        ).validate(df, lazy=True)
