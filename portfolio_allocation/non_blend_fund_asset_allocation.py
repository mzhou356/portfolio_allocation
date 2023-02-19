# pylint:disable=no-name-in-module, import-error
"""This module calculates asset_allocation for all accounts with just one
type fund."""
from typing import Dict

from portfolio_allocation import PORTFOLIO_BREAKDOWN, combine_portfolios
from portfolio_allocation.configuration import (
    NON_BLEND_FUND_ACCOUNT_TO_ASSET_TYPE_MAPPING,
    ALL_CURRENT_NON_BLEND_ACCOUNTS,
)


def _create_non_blend_fund_asset_allocation(account_name: str) -> Dict[str, float]:
    """
    This prompts the user to enter the asset type and asset amount for
    a specified account_name for a non blend fund account.
    Args:
        account_name (str): the name of the non blend fund financial account.

    Returns:
         A dictionary with asset_type as key and asset amount as value.
    """
    asset_type = NON_BLEND_FUND_ACCOUNT_TO_ASSET_TYPE_MAPPING[account_name]
    if asset_type == "mortgage":
        asset_amount = _estimate_mortgage_asset()
    else:
        asset_amount = float(
            input(f"Please enter the asset amount for the {account_name} fund.")
        )
    return {asset_type: asset_amount}


def _estimate_mortgage_asset() -> float:
    """
    This function takes current house value from redfin and subtracts the
    principal from the house to estimate the house asset amount.
    Returns:
        a float. Estimated house asset amount.
    """
    current_estimation = input(
        "Please enter the current house estimation from redfin.com."
    )
    principal = input("Please enter the current principal on the house.")
    return float(current_estimation) - float(principal)


def generate_combined_non_blend_fund_asset_allocation() -> Dict[str, float]:
    """
    This function creates the combined asset allocation for all non blend
    fund accounts.
    Returns:
    A dictionary with combined asset allocation for all accounts.
    """
    curr_portfolio = PORTFOLIO_BREAKDOWN.copy()
    for account_name in ALL_CURRENT_NON_BLEND_ACCOUNTS:
        curr_portfolio = combine_portfolios(
            portfolio_a=curr_portfolio,
            portfolio_b=_create_non_blend_fund_asset_allocation(
                account_name=account_name,
            ),
        )
    return curr_portfolio
