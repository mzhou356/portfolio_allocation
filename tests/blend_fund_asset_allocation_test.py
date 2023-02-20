"""This module tests all functions from module blend_fund_asset_allocation."""
import pytest

from portfolio_allocation.blend_fund_asset_allocation import (
    _relevant_page_filter,
    _process_fund_name_columns,
)


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


@pytest.mark.parametrize(
    "text_line, start_index , end_index, expected",
    [
        ("fund A $100,00", 0, 2, "fund A"),
        ("info fund_B info $25,000.00 total", 1, 2, "fund_B"),
    ],
)
def test_process_fund_name_columns(text_line, start_index, end_index, expected):
    """Test _process_fund_name_columns function."""
    actual = _process_fund_name_columns(
        text_with_fund_name=text_line,
        fund_col_index_start=start_index,
        fund_col_index_end=end_index,
    )

    assert expected == actual
