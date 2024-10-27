import pandas as pd
import pytest
from src.model.power_system_model import PowerSystemModel


def test_create_power_system_model_on_correct_data(
    nodes_df: pd.DataFrame,
    branches_lines_and_trafos_df: pd.DataFrame,
    generators_df: pd.DataFrame,
) -> None:
    try:
        PowerSystemModel(
            nodes=nodes_df,
            branches=branches_lines_and_trafos_df,
            generators=generators_df,
        )
    except:
        pytest.fail()
