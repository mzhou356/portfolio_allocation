# pylint: disable =
"""This module tests all functions from module non_blend_fund_asset_allocation."""

import builtins
import pytest

from portfolio_allocation.non_blend_fund_asset_allocation import (
    _estimate_mortgage_asset,
    _create_non_blend_fund_asset_allocation,
    generate_combined_non_blend_fund_asset_allocation,
)


def test_estimate_mortgage_asset(mocker) -> None:
    """Test function estimate_mortgage_asset."""
    input_mock_method = mocker.patch.object(builtins, "input")
    input_mock_method.side_effect = ["60000", "58000"]

    actual = _estimate_mortgage_asset()

    assert actual == 2000


@pytest.mark.parametrize(
    "account_name, expected",
    [
        ("t_rowe_price_group_stock", {"us_stock": 10000.0}),
        ("mortgage", {"mortgage": 2000}),
    ],
)
def test_create_non_blend_fund_asset_allocation(account_name, expected, mocker) -> None:
    """Test function create_non_blend_fund_asset_allocation."""
    input_mock_method = mocker.patch.object(builtins, "input")
    input_mock_method.side_effect = ["10000", "8000"]

    actual = _create_non_blend_fund_asset_allocation(account_name=account_name)

    assert actual == expected


def test_generate_combined_non_blend_fund_asset_allocation(mocker) -> None:
    """Test generate_combined_non_blend_fund_asset_allocation."""
    input_mock_method = mocker.patch.object(builtins, "input")
    input_mock_method.side_effect = ["1000", "1000", "1000", "1000", "1000"]
    mocker.patch(
        "portfolio_allocation.non_blend_fund_asset_allocation."
        "_estimate_mortgage_asset",
        return_value=2000.0,
    )
    expected = {
        "us_stock": 1000.0,
        "cash": 3000.0,
        "mortgage": 2000.0,
        "fixed_income": 1000.0,
        "international_stock": 0,
        "other": 0,
        "not_classified": 0,
    }

    actual = generate_combined_non_blend_fund_asset_allocation()

    assert actual == expected
