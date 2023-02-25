"""This module tests all functions from module combined_asset_allocation."""
import pandas as pd
import pytest
from portfolio_allocation.combined_asset_allocation import (
    _assign_asset_type_breakdown,
    _calculate_asset_percentage_column,
)


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


@pytest.mark.parametrize(
    "all_asset_allocation_df, expected",
    [
        (
            pd.DataFrame(
                {"asset_value($)": [100, 25, 75]},
            ),
            pd.Series([50, 12.5, 37.5], name="asset_value($)"),
        ),
        (
            pd.DataFrame(
                {"asset_value($)": [200, 0, 100]},
            ),
            pd.Series([2 / 3 * 100, 0.0, 1 / 3 * 100], name="asset_value($)"),
        ),
        (
            pd.DataFrame(
                {"asset_value($)": [0, 0, 75]},
            ),
            pd.Series([0.0, 0.0, 100.0], name="asset_value($)"),
        ),
    ],
)
def test_calculate_asset_percentage_column_succeeds(
    all_asset_allocation_df, expected
) -> None:
    """Test _calculate_asset_percentage_column."""
    actual = _calculate_asset_percentage_column(
        all_asset_allocation_df=all_asset_allocation_df
    )

    pd.testing.assert_series_equal(left=actual, right=expected)
