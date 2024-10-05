import abc
from dataclasses import dataclass

import numpy as np
import pandas as pd
import pandera as pa
from src.datamodel.config import LINE, TRAFO


@dataclass
class InputPowerSystemData:
    """Class for the input power system data."""

    branches: pd.DataFrame
    """Lines and trafos parameters."""
    generators: pd.DataFrame
    """Generators parameters."""
    nodes: pd.DataFrame
    """Nodes parameters."""


class DataSetSchema(abc.ABC):

    def __init__(self, input_data: InputPowerSystemData, dataset_name: str) -> None:
        self.data = input_data
        self.dataset_name = dataset_name

    def _error_msg(self, msg: str) -> str:
        return f"Error in {self.dataset_name}: {msg}"

    @abc.abstractmethod
    def data_frame_schema(self) -> pa.DataFrameSchema:
        raise NotImplementedError

    def _node_reference_col(self, col_name) -> pa.Column:
        return pa.Column(
            dtype=pa.String,
            checks=[
                pa.Check(
                    lambda n: n.isin(self.data.nodes.index),
                    error=self._error_msg(f"{col_name} must contain node identifiers."),
                )
            ],
        )



class BranchesSchema(DataSetSchema):

    _required_trafo_cols = [
        "tap_ratio",
        "phase_shift",
    ]

    _trafo_cols = [
        "tap_ratio",
        "phase_shift",
        "phase_shift_min",
        "phase_shift_max",
    ]

    def __init__(self, input_data: InputPowerSystemData) -> None:
        super().__init__(input_data, dataset_name="branches")

    def _phase_shift_col(self, col_name) -> pa.Column:
        return pa.Column(
            dtype=pa.Float,
            checks=[
                pa.Check(
                    lambda pshift: 0 <= pshift <= np.pi / 2,
                    error=self._error_msg(f"{col_name} must be between 0 and pi/2."),
                )
            ],
            nullable=True,
            required=False,
        )

    def _required_trafo_cols_provided_for_trafos_checks(self) -> list[pa.Check]:
        def _validate(df: pd.DataFrame, col_name: str) -> bool:
            trafo_df = df[df["type"] == TRAFO]
            if col_name not in df.columns:
                return trafo_df.size == 0
            else:
                return not trafo_df[col_name].isna().all()

        return [
            pa.Check(
                lambda df: _validate(df, col_name),
                error=self._error_msg(
                    f"{col_name} value must be provided for all {TRAFO} branches."
                ),
            )
            for col_name in self._required_trafo_cols
        ]

    def _trafo_cols_not_provided_for_lines_checks(self) -> list[pa.Check]:
        def _validate(df: pd.DataFrame, col_name: str) -> bool:
            line_df = df[df["type"] == LINE]
            return col_name not in df.columns or line_df[col_name].isna().all()
        
        return [
            pa.Check(
                lambda df: _validate(df, col_name),
                error=self._error_msg(
                    msg=f"{col_name} value can not be specified for any {LINE} branch."
                ),
            )
            for col_name in self._trafo_cols
        ]

    def _phase_shift_cross_checks(self) -> list[pa.Check]:
        return [
            pa.Check(
                lambda df: (df['phase_shift_min'].isna() == df['phase_shift_max'].isna()).all(),
                error=self._error_msg(
                    f"for any {TRAFO} branch both 'phase_shift_minus' and 'phase_shift_plus' must be specified or none."
                ),
            ),
            pa.Check(
                lambda df: (~(df['phase_shift_min'].isna) & ~(df['phase_shift'].isna())).size == 0,
                error=self._error_msg(
                    f"for any {TRAFO} branch 'phase_shift' can be specified if an only if 'phase_shift_minus' and 'phase_shift_plus' are not."
                ),
            ),
            pa.Check(
                lambda df: df[~df['phase_shift_min'].isna()]['phase_shift_min'] <= df[~df['phase_shift_max'].isna()]['phase_shift_max'],
                error=self._error_msg(f"'phase_shift_min' must be smaller or equal than 'phase_shift_max' (if both are defined).")
            )
        ]

    def data_frame_schema(self) -> pa.DataFrameSchema:
        return pa.DataFrameSchema(
            {
                "type": pa.Column(pa.String, [pa.Check(lambda t: t.isin([LINE, TRAFO]))]),
                "node_from": self._node_reference_col(col_name="node_from"),
                "node_to": self._node_reference_col(col_name="node_to"),
                "reactance": pa.Column(
                    dtype=pa.Float,
                    checks=[
                        pa.Check(
                            lambda x: 0.0 < x,
                            error=self._error_msg("reactance must be positive."),
                        ),
                    ],
                ),
                "F_max": pa.Column(
                    dtype=pa.Float,
                    checks=[
                        pa.Check(
                            lambda f_max: f_max >= 0.0,
                            error=self._error_msg("F_max must be non-negative."),
                        )
                    ],
                ),
                "F_min": pa.Column(
                    dtype=pa.Float,
                    checks=[
                        pa.Check(
                            lambda f_min: f_min <= 0.0,
                            error=self._error_msg("F_min must be non-positive."),
                        )
                    ],
                    nullable=True,
                    required=False,
                ),
                "tap_ratio": pa.Column(
                    dtype=pa.Float,
                    checks=[
                        pa.Check(
                            lambda tap: tap > 0,
                            error=self._error_msg("tap_ratio must be positive."),
                        )
                    ],
                    nullable=True,
                    required=False,
                ),
                "phase_shift": self._phase_shift_col("phase_shift"),
                "phase_shift_min": self._phase_shift_col("phase_shift_min"),
                "phase_shift_max": self._phase_shift_col("phase_shift_max"),
            },
            checks=[
                *self._trafo_cols_not_provided_for_lines_checks(), 
                *self._required_trafo_cols_provided_for_trafos_checks, 
                *self._phase_shift_cross_checks(),
            ]
        )


class NodesSchema(DataSetSchema):

    def __init__(self, input_data: InputPowerSystemData) -> None:
        super().__init__(input_data, dataset_name='nodes')

    def data_frame_schema(self) -> pa.DataFrameSchema:
        return pa.DataFrameSchema(
            {
                "node_id": pa.Column(dtype=pa.String),
                "active_power_demand": pa.Column(
                    dtype=pa.Float,
                    checks=[
                        pa.Check(
                            lambda dem: dem >= 0,
                            error=self._error_msg(msg="'active_power_demand' must be non-negative (if provided).")
                        )
                    ],
                    nullable=True,
                    required=False,
                )
            }
        )


class GeneratorsSchema(DataSetSchema):

    def __init__(self, input_data: InputPowerSystemData) -> None:
        super().__init__(input_data, dataset_name='generators')

    def data_frame_schema(self) -> pa.DataFrameSchema:
        return pa.DataFrameSchema(
            {
                "node": self._node_reference_col('node'),
                "P_min": pa.Column(dtype=pa.Float),
                "P_max": pa.Column(dtype=pa.Float),
                "cost": pa.Column(
                    dtype=pa.Float,
                    checks=[
                        pa.Check(
                            lambda cost: cost >= 0,
                            error=self._error_msg(f"'cost' must be a non-negative value (if provided).")
                        )
                    ],
                    nullable=True,
                    required=False,
                )
            }
        )
