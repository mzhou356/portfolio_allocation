# pylint: disable = too-many-locals
"""This module tests all functions from module blend_fund_asset_allocation."""
import pandas as pd
import pytest

from portfolio_allocation.blend_fund_asset_allocation import (
    _relevant_page_filter,
    _process_fund_name_columns,
    _extract_dollar_amount,
    _extract_fund_value_from_text_line,
    _process_blend_fund_texts,
    _process_blend_fund_tables,
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
def test_relevant_page_filter_succeeds(page_num, target_page_num, expected) -> None:
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
def test_process_fund_name_columns_succeeds(
    text_line, start_index, end_index, expected
) -> None:
    """Test _process_fund_name_columns function."""
    actual = _process_fund_name_columns(
        text_with_fund_name=text_line,
        fund_col_index_start=start_index,
        fund_col_index_end=end_index,
    )

    assert expected == actual


@pytest.mark.parametrize(
    "asset_amount, chars_to_strip, expected",
    [
        ("$100,000", "$", 100000.0),
        ("USD125.00", "USD", 125.0),
        ("1000,000.25", "", 1000000.25),
        ("USD$6.25", "USD$", 6.25),
        (".25", "", 0.25),
    ],
)
def test_extract_dollar_amount_succeeds(asset_amount, chars_to_strip, expected) -> None:
    """Test extract_dollar_amount."""
    actual = _extract_dollar_amount(
        asset_amount=asset_amount,
        chars_to_strip=chars_to_strip,
    )
    assert expected == actual


@pytest.mark.parametrize(
    "text_line, index_number , str_filter, expected",
    [
        ("fund A $100,000.25", -1, None, 100000.25),
        ("info fund_B info $25,000.00 total 100.02", 0, "$", 25000.0),
        ("fund B 100.0 fund A 240.25", 2, None, 100.0),
    ],
)
def test_extract_fund_value_from_text_line(
    text_line, index_number, str_filter, expected
) -> None:
    """Test function extract_fund_value_from_text_line"""
    actual = _extract_fund_value_from_text_line(
        text_line=text_line,
        fund_value_index_number=index_number,
        amount_str_filter=str_filter,
    )
    assert expected == actual


def test_process_blend_fund_texts(
    pdf_statement_pages,
    blend_fund_asset_allocation_text_fund,
    expected_text_fund_asset_allocation,
    mocker,
) -> None:
    """Test _process_blend_fund_texts"""
    mocker.patch(
        "portfolio_allocation.blend_fund_asset_allocation.load_pdf_statements",
        return_value=pdf_statement_pages,
    )
    fund_names = ["A", "B", "C", "E", "F"]
    target_page_nums = {1, 2}
    file_path = "test_file_path"
    fund_value_index_number = -1

    actual = _process_blend_fund_texts(
        file_path=file_path,
        target_page_num=target_page_nums,
        blend_fund_asset_allocation=blend_fund_asset_allocation_text_fund,
        fund_names=fund_names,
        fund_value_index_number=fund_value_index_number,
    )

    assert expected_text_fund_asset_allocation == actual


def test_process_blend_fund_tables_without_col_parse_function_succeeds(
    blend_fund_table_one,
    blend_fund_table_one_output,
    mocker,
) -> None:
    """
    Test process_blend_fund_tables without col parse function.
    """
    mocker.patch(
        "portfolio_allocation.blend_fund_asset_allocation.parse_pdf_tables",
        return_value=blend_fund_table_one,
    )
    file_path = "test_file_path"
    page_num = 0
    pandas_options = {"headers": None}
    table_index_number = 0
    multiple_table_flag = False
    fund_names = ["fund_a", "fund_b", "fund_c"]
    fund_value_column_name = "balance"

    actual = _process_blend_fund_tables(
        file_path=file_path,
        page_num=page_num,
        pandas_options=pandas_options,
        table_index_number=table_index_number,
        multiple_table_flag=multiple_table_flag,
        fund_names=fund_names,
        fund_value_column_name=fund_value_column_name,
    )

    pd.testing.assert_series_equal(left=actual, right=blend_fund_table_one_output)


def test_process_blend_fund_tables_with_col_parse_function_succeeds(
    blend_fund_table_two,
    blend_fund_table_two_output,
    mocker,
) -> None:
    """
    Test process_blend_fund_tables with col parse function.
    """
    mocker.patch(
        "portfolio_allocation.blend_fund_asset_allocation.parse_pdf_tables",
        return_value=blend_fund_table_two,
    )

    file_path = "test_file_path"
    page_num = 0
    pandas_options = {"headers": None}
    table_index_number = 0
    multiple_table_flag = False
    fund_names = ["fund_e", "fund_f"]
    fund_value_column_name = 1
    fund_row_index_start = 1
    fund_row_index_end = 3
    fund_col_parse_function = _process_fund_name_columns
    fund_col_index_end = 1
    fund_col_number = 0

    actual = _process_blend_fund_tables(
        file_path=file_path,
        page_num=page_num,
        pandas_options=pandas_options,
        table_index_number=table_index_number,
        multiple_table_flag=multiple_table_flag,
        fund_names=fund_names,
        fund_value_column_name=fund_value_column_name,
        fund_row_index_start=fund_row_index_start,
        fund_row_index_end=fund_row_index_end,
        fund_col_parse_function=fund_col_parse_function,
        fund_col_index_end=fund_col_index_end,
        fund_col_number=fund_col_number,
    )

    pd.testing.assert_series_equal(left=actual, right=blend_fund_table_two_output)
