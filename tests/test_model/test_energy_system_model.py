import pandas as pd
import pytest
from src.model.power_system_model import PowerSystemModel


def test_create_power_system_model_on_correct_data(
    nodes_df: pd.DataFrame,
    transmission_lines_df: pd.DataFrame,
    trafos_df: pd.DataFrame,
    generators_df: pd.DataFrame,
    marginal_costs_df: pd.DataFrame,
) -> None:
    try:
        PowerSystemModel(
            nodes=nodes_df,
            transmission_lines=transmission_lines_df,
            transformers=trafos_df,
            generators=generators_df,
            marginal_costs=marginal_costs_df,
        )
    except:
        pytest.fail()
