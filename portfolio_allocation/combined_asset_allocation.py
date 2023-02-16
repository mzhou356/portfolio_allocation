# pylint: disable=import-error
"""This module combines both blend and non-blend accounts."""

from typing import Dict

from portfolio_allocation.blend_fund_asset_allocation import (
    generate_combined_blend_fund_asset_allocation,
)
from portfolio_allocation.non_blend_fund_asset_allocation import (
    generate_combined_non_blend_fund_asset_allocation,
)
from portfolio_allocation import combine_portfolios


def combine_all_asset_allocation(
    blend_fund_asset_allocation: Dict[str, float],
    non_blend_fund_asset_allocation: Dict[str, float],
) -> Dict[str, float]:
    """
    This function takes in both blend_fund_asset_allocation and non blend fund asset allocation
    and combines into a final all_asset_allocation.
    Args:
        blend_fund_asset_allocation (Dict[str, float]): asset allocation for blend fund accounts.
        non_blend_fund_asset_allocation (Dict[str, float]): asset allocation for non blend fund accounts.

    Returns:
        combined asset allocation from both account types.
    """
    return combine_portfolios(
        portfolio_a=blend_fund_asset_allocation,
        portfolio_b=non_blend_fund_asset_allocation,
    )


def generate_asset_allocation_dollar_value_table():
    """Create a pandas dataframe with
    number not percentage."""


def generate_asset_allocation_pct_table():
    """Create a pandas dataframe with
    percentage not just number."""


def create_html_table():
    """Create a simple html table."""
