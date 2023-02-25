"""This module tests all functions from module combined_asset_allocation."""
import pytest
from portfolio_allocation.combined_asset_allocation import _assign_asset_type_breakdown


@pytest.mark.parametrize(
    "asset_type, expected",
    [
        ("mortgage", ["us", "mortgage"]),
        ("fixed_income", ["us_international", "fixed_income"]),
        ("international_stock", ["international", "stock"]),
    ],
)
def test_assign_asset_type_breakdown_succeeds(asset_type, expected) -> None:
    """Test _assign_asset_type_breakdown."""
    actual = _assign_asset_type_breakdown(asset_type=asset_type)

    assert expected == actual
