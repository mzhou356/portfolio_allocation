# pylint: disable =
"""This module tests all functions from module non_blend_fund_asset_allocation."""

import builtins


from portfolio_allocation.non_blend_fund_asset_allocation import (
    _estimate_mortgage_asset,
)


def test_estimate_mortgage_asset(mocker):
    """Test function estimate_mortgage_asset."""
    input_mock_method = mocker.patch.object(builtins, "input")
    input_mock_method.side_effect = ["60000", "58000"]

    actual = _estimate_mortgage_asset()

    assert actual == 2000
