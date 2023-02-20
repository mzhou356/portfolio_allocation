"""This module tests all functions from module blend_fund_asset_allocation."""
import pytest

from portfolio_allocation.blend_fund_asset_allocation import _relevant_page_filter


@pytest.mark.parametrize(
    "page_num, target_page_num, expected",
    [
        (7, 5, False),
        (7, {4, 5}, False),
        (6, 6, True),
        (6, {4, 5, 6}, True),
    ],
)
def test_relevant_page_filter_succeeds(page_num, target_page_num, expected):
    """Test relevant_page_filter function."""
    actual = _relevant_page_filter(
        page_number=page_num,
        target_page_num=target_page_num,
    )

    assert expected == actual
