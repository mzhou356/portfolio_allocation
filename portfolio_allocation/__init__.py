# pylint: disable=missing-module-docstring
from typing import Dict

PORTFOLIO_BREAKDOWN: Dict[str, float] = {
    "us_stock": 0,
    "international_stock": 0,
    "fixed_income": 0,
    "not_classified": 0,
    "cash": 0,
    "other": 0,
}


def combine_portfolios(
    portfolio_a: Dict[str, float], portfolio_b: Dict[str, float]
) -> Dict[str, float]:
    """
    This function combines 2 financial portfolios into one.
    Args:
        portfolio_a (Dict[str, float]): portfolio of one financial account.
        portfolio_b (Dict[str, float]): portfolio of another financial account.

    Returns:
        Dict[str, float], a combined portfolio of 2 accounts.
    """
    all_keys = set(portfolio_a.keys()).union(portfolio_b.keys())
    return {
        asset_type: portfolio_a.get(asset_type, 0) + portfolio_b.get(asset_type, 0)
        for asset_type in all_keys
    }
