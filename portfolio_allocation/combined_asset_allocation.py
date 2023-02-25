"""This module combines both blend and non-blend accounts."""

from typing import Dict, List, Set

import pandas as pd

from portfolio_allocation import combine_portfolios, PORTFOLIO_BREAKDOWN

DEFAULT_DATAFRAME_ORIENT: str = "index"
DEFAULT_ASSET_AMOUNT_COLUMN_NAME: str = "asset_value($)"
DEFAULT_ASSET_PCT_COLUMN_NAME: str = "asset_pct"
DEFAULT_ASSET_ALLOCATION_BY_REGION_AND_ASSET_CLASS_COLUMNS: List[str] = [
    "cash",
    "fixed_income",
    "stock",
    "mortgage",
    "other",
    "not_classified",
]
DEFAULT_US_ASSET_TYPES: Set[str] = {"cash", "other", "not_classified", "mortgage"}
ALL_ASSET_TYPES: Set[str] = {"mortgage"}.union(PORTFOLIO_BREAKDOWN.keys())
DEFAULT_US_INTERNATIONAL_ASSET_TYPES: Set[str] = {"fixed_income"}
DEFAULT_REGION_INDICES: List[str] = ["us", "international", "us_international"]
DEFAULT_NA_VALUE: float = 0.0
DEFAULT_TOTAL_ROW_INDEX: str = "total"


def combine_all_asset_allocation(
    blend_fund_asset_allocation: Dict[str, float],
    non_blend_fund_asset_allocation: Dict[str, float],
) -> Dict[str, float]:
    """
    This function takes in both blend_fund_asset_allocation and non blend
    fund asset allocation and combines into a final all_asset_allocation.
    Args:
        blend_fund_asset_allocation (Dict[str, float]): asset allocation for
        blend fund accounts.
        non_blend_fund_asset_allocation (Dict[str, float]): asset allocation for
        non blend fund accounts.

    Returns:
        combined asset allocation from both account types.
    """
    return combine_portfolios(
        portfolio_a=blend_fund_asset_allocation,
        portfolio_b=non_blend_fund_asset_allocation,
    )


def generate_asset_allocation_by_asset_class_table(
    all_asset_allocation: Dict[str, float]
) -> pd.DataFrame:
    """
    Create a pandas dataframe per asset class type.

    Args:
        all_asset_allocation (Dict[str, float]): combined asset allocation from all
        account types.
    Returns:
        a pandas dataframe with asset type as indices and asset amount in US dollars
        and asset_percentage as dataframe columns.
    """
    all_asset_allocation_df = pd.DataFrame.from_dict(
        data=all_asset_allocation,
        orient=DEFAULT_DATAFRAME_ORIENT,
        columns=[DEFAULT_ASSET_AMOUNT_COLUMN_NAME],
    )
    all_asset_allocation_df[
        DEFAULT_ASSET_PCT_COLUMN_NAME
    ] = _calculate_asset_percentage_column(
        all_asset_allocation_df=all_asset_allocation_df,
    )
    return all_asset_allocation_df


def _calculate_asset_percentage_column(
    all_asset_allocation_df: pd.DataFrame,
) -> pd.Series:
    """
    This function calculates the asset percentage for each asset
    class.
    Args:
        all_asset_allocation_df (pd.DataFrame): a pandas dataframe
        by asset class type.

    Returns:
        a pandas series with asset percentage information.
    """
    total_asset_amount = all_asset_allocation_df[DEFAULT_ASSET_AMOUNT_COLUMN_NAME].sum()
    return all_asset_allocation_df[DEFAULT_ASSET_AMOUNT_COLUMN_NAME].map(
        lambda amount: amount / total_asset_amount * 100.0
    )


def _assign_asset_type_breakdown(asset_type):
    if asset_type in DEFAULT_US_ASSET_TYPES:
        return ["us", asset_type]
    if asset_type in DEFAULT_US_INTERNATIONAL_ASSET_TYPES:
        return ["us_international", "fixed_income"]
    return asset_type.split("_")


def generate_asset_allocation_by_region_and_asset_class_table(
    asset_allocation_by_asset_class_table: pd.DataFrame,
) -> pd.DataFrame:
    """
    creates a pandas dataframe with regions as indices and asset class
    as columns for percentage information only.
    Args:
        asset_allocation_by_asset_class_table (pd.DataFrame): a pandas dataframe with
        asset type as indices and asset amount in US dollars and asset_percentage as
        dataframe columns.
    Returns:
         a pandas dataframe with regions as indices and asset class
         as columns for percentage information only.
    """
    asset_allocation_by_region_and_asset_class_df = pd.DataFrame(
        columns=DEFAULT_ASSET_ALLOCATION_BY_REGION_AND_ASSET_CLASS_COLUMNS,
        index=DEFAULT_REGION_INDICES,
    )
    asset_allocation_by_region_and_asset_class_df.fillna(
        value=DEFAULT_NA_VALUE,
        inplace=True,
    )
    for asset_type in ALL_ASSET_TYPES:
        df_index, col_name = _assign_asset_type_breakdown(
            asset_type=asset_type,
        )
        asset_allocation_by_region_and_asset_class_df.loc[
            df_index, col_name
        ] = asset_allocation_by_asset_class_table.loc[
            asset_type, DEFAULT_ASSET_PCT_COLUMN_NAME
        ]
    asset_allocation_by_region_and_asset_class_df.loc[
        DEFAULT_TOTAL_ROW_INDEX
    ] = asset_allocation_by_region_and_asset_class_df.sum()
    return asset_allocation_by_region_and_asset_class_df
