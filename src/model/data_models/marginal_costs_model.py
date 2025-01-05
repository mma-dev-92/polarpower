import pandas as pd
import pandera as pa
from pandera.typing import Series

from src.model.data_models import DataFrameModelWithContext
from src.model.data_models.utils import err_finite_check, err_foreign_key, err_non_monotonic_merit_order, err_prange, finite_check


class MarginalCostsDataModel(DataFrameModelWithContext):
    """
    Data model for generators marginal costs.

    Validation logic:
    * If a generator is specified in MarginalCostsDataModel - it is required, that defined
      cost intervals sums up to [pmin, pmax] interval.
    * If generator has specified constant cost in GeneratorsDataModel - it is not possible to
      define marginal costs for it (it is assumed, that it has marginal cost constant for all values
      within [pmin, pmax] interval).

    """

    generator_id: Series[str] = pa.Field(
        coerce=True,
        description="Generator for which marginal cost is specified.",
    )
    p_start: Series[float] = pa.Field(
        coerce=True,
        description="Beginning of the cost interval.",
    )
    p_end: Series[float] = pa.Field(
        coerce=True,
        description="End of the cost interval.",
    )
    cost: Series[float] = pa.Field(
        coerce=True,
        description="Cost [per unit] for a given power interval",
    )

    @pa.check("generator_id", error=err_foreign_key(fk_col="generator_id"))
    def validate_generator_id(cls, generator_id: Series[str]):
        return generator_id.isin(cls.get_context("generators_df").index)

    @pa.check("cost", error=err_finite_check(col_name="cost", null=False))
    def validate_cost(cls, cost: Series[float]):
        return finite_check(cost)

    @pa.dataframe_check(error=err_prange())
    def validate_cost_intervals(cls, df: pd.DataFrame):
        """Validate, if for each generator, marginal cost intervals are correct."""
        df = df.copy()
        df["_original_index"] = df.index

        generators_df = cls.get_context("generators_df").reset_index()
        mc_sorted = df.sort_values(["generator_id", "p_start"]).copy()

        mc_merged = mc_sorted.merge(
            generators_df[["generator_id", "P_min", "P_max"]],
            on="generator_id",
            how="left",
        )

        # identify first p_start and last p_end for each generator
        mc_merged["first_p_start"] = mc_merged.groupby("generator_id")[
            "p_start"
        ].transform("first")
        mc_merged["last_p_end"] = mc_merged.groupby("generator_id")["p_end"].transform(
            "last"
        )

        # identify previous p_end for each entry (shift by 1)
        mc_merged["prev_p_end"] = mc_merged.groupby("generator_id")["p_end"].shift()

        # first rule: the smallest p_start for each generator should be equal to P_min
        mc_merged["valid_min"] = mc_merged["first_p_start"].eq(mc_merged["P_min"])

        # second rule: the biggest p_end should be equal to P_max
        mc_merged["valid_max"] = mc_merged["last_p_end"].eq(mc_merged["P_max"])

        # third rule: prev_p_end == p_start, if prev_p_end is defined
        mc_merged["valid_contiguity"] = (
            mc_merged["p_start"].eq(mc_merged["prev_p_end"])
            | mc_merged["prev_p_end"].isna()
        )

        # fetch all rules together
        overall_valid = mc_merged[
            ["valid_min", "valid_max", "valid_contiguity"]
        ]

        # reindex below DataFrame, so it matches the original DF's index and order
        overall_valid = overall_valid.set_axis(mc_merged["_original_index"], axis=0)
        overall_valid = overall_valid.reindex(df["_original_index"], fill_value=False)

        # data is correct iff all three conditions are satisfied
        return overall_valid.all(axis=1)

    @pa.dataframe_check(error=err_non_monotonic_merit_order())
    def validate_monotonic_cost(cls, df: pd.DataFrame):
        # Sort to ensure intervals are in ascending order of p_start
        df_sorted = df.sort_values(["generator_id", "p_start"]).copy()

        # For each generator, shift cost by 1 to compare current vs. previous interval
        df_sorted["prev_cost"] = (
            df_sorted.groupby("generator_id")["cost"].shift()
        )

        df_sorted["valid_monotonic"] = (
            df_sorted["prev_cost"].isna()
            | (df_sorted["cost"] >= df_sorted["prev_cost"])
        )

        return df_sorted["valid_monotonic"].reindex(df.index)

