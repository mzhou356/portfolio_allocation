"""This module tests all functions from module combined_asset_allocation."""
import pandas as pd
import pytest
from portfolio_allocation.combined_asset_allocation import (
    _assign_asset_type_breakdown,
    _calculate_asset_percentage_column,
    combine_all_asset_allocation,
    generate_asset_allocation_by_asset_class_table,
    generate_asset_allocation_by_region_and_asset_class_table,
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


def test_combine_all_asset_allocation_succeeds() -> None:
    """Test combine_all_asset_allocation."""
    blend_fund = {
        "a": 1000.0,
        "b": 2000.0,
        "c": 1000.0,
    }
    non_blend_fund = {
        "a": 2000.0,
        "d": 500.0,
        "c": 2000.0,
    }
    expected = {
        "a": 3000.0,
        "b": 2000.0,
        "c": 3000.0,
        "d": 500.0,
    }

    actual = combine_all_asset_allocation(
        blend_fund_asset_allocation=blend_fund,
        non_blend_fund_asset_allocation=non_blend_fund,
    )

    assert actual == expected


def test_generate_asset_allocation_by_asset_class_table_succeeds(
    asset_allocation_by_asset_class_table,
) -> None:
    """Test generate_asset_allocation_by_asset_class_table."""
    all_asset_allocation = {
        "us_stock": 7500.0,
        "international_stock": 2500.0,
        "fixed_income": 5000.0,
        "cash": 500.0,
        "mortgage": 2000.0,
        "other": 50.0,
        "not_classified": 100.0,
    }

    actual = generate_asset_allocation_by_asset_class_table(
        all_asset_allocation=all_asset_allocation
    )

    pd.testing.assert_frame_equal(
        left=actual,
        right=asset_allocation_by_asset_class_table,
    )


def test_generate_asset_allocation_by_region_and_asset_class_table(
    asset_allocation_by_asset_class_table,
) -> None:
    """Test generate_asset_allocation_by_region_and_asset_class_table."""
    expected = pd.DataFrame(
        {
            "cash": [2.832861, 0.0, 0.0, 2.832861],
            "fixed_income": [0.0, 0.0, 28.328612, 28.328612],
            "stock": [42.492918, 14.164306, 0.0, 56.657224],
            "mortgage": [11.331445, 0.0, 0.0, 11.331445],
            "other": [0.283286, 0.0, 0.0, 0.283286],
            "not_classified": [0.566572, 0.0, 0.0, 0.566572],
        },
        index=["us", "international", "us_international", "total"],
    )

    actual = generate_asset_allocation_by_region_and_asset_class_table(
        asset_allocation_by_asset_class_table=asset_allocation_by_asset_class_table,
    )

    pd.testing.assert_frame_equal(
        left=actual,
        right=expected,
    )
