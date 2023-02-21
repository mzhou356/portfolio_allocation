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
    _create_asset_allocation_from_pdf_tables,
    _create_blend_fund_asset_allocation,
    _process_all_pdf_table_funds,
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
def test_extract_fund_value_from_text_line_succeeds(
    text_line, index_number, str_filter, expected
) -> None:
    """Test function extract_fund_value_from_text_line"""
    actual = _extract_fund_value_from_text_line(
        text_line=text_line,
        fund_value_index_number=index_number,
        amount_str_filter=str_filter,
    )
    assert expected == actual


def test_process_blend_fund_texts_succeeds(
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
        fund_col_parse_function=fund_col_parse_function,
        fund_col_index_end=fund_col_index_end,
        fund_col_number=fund_col_number,
    )

    pd.testing.assert_series_equal(left=actual, right=blend_fund_table_two_output)


def test_create_asset_allocation_from_pdf_tables_succeeds(
    blend_fund_asset_allocation_table_fund,
    expected_table_fund_asset_allocation,
    blend_fund_table_one_output,
    blend_fund_table_two_output,
) -> None:
    """
    Test create_asset_allocation_from_pdf_tables.
    """
    fund_list = [blend_fund_table_one_output, blend_fund_table_two_output]
    vested_pct = 0.8

    actual = _create_asset_allocation_from_pdf_tables(
        blend_fund_asset_allocation=blend_fund_asset_allocation_table_fund,
        fund_list=fund_list,
        vested_pct=vested_pct,
    )

    assert expected_table_fund_asset_allocation == actual


@pytest.mark.parametrize(
    "fund_name, fund_mapping , total_fund_value, expected",
    [
        (
            "A",
            {"A": {"international_stock": 0.75, "fixed_income": 0.15, "cash": 0.1}},
            1000,
            {
                "us_stock": 0.0,
                "international_stock": 750.0,
                "fixed_income": 150.0,
                "other": 0.0,
                "not_classified": 0.0,
                "cash": 100.0,
            },
        ),
        (
            "B",
            {"B": {"us_stock": 0.8, "other": 0.05, "cash": 0.15}},
            2000,
            {
                "us_stock": 1600.0,
                "international_stock": 0.0,
                "fixed_income": 0.0,
                "other": 100.0,
                "not_classified": 0.0,
                "cash": 300.0,
            },
        ),
    ],
)
def test_create_blend_fund_asset_allocation_succeeds(
    fund_name, fund_mapping, total_fund_value, expected
) -> None:
    """Test function create blend fund asset allocation."""
    actual = _create_blend_fund_asset_allocation(
        fund_name=fund_name,
        fund_mapping=fund_mapping,
        total_fund_value=total_fund_value,
    )
    assert actual == expected


def test_process_all_pdf_table_funds_succeeds(
    blend_fund_table_two_output,
    blend_fund_asset_allocation_table_fund,
    mocker,
) -> None:
    """Test process_all_pdf_table_funds"""
    asset_information = {
        "pandas_parse_options": [{}],
        "table_index_number": [0],
        "fund_value_column_names": [1],
        "fund_col_parse_function": [True],
        "fund_row_index_start": [1],
        "multiple_table_flags": [False],
        "vested_pct": 1.0,
    }
    fund_name_lists = [["fund_e", "fund_f"]]
    fund_name_to_ticker_mapping = [{"fund_e": "ticker_e"}]
    mid_url = ["url"]
    page_nums = [0]
    file_path = "test_file_path"
    mocker.patch(
        "portfolio_allocation.blend_fund_asset_allocation."
        "blend_fund_asset_allocation_generator",
        return_value=blend_fund_asset_allocation_table_fund,
    )
    mocker.patch(
        "portfolio_allocation.blend_fund_asset_allocation._process_blend_fund_tables",
        return_value=blend_fund_table_two_output,
    )
    expected = {
        "international_stock": 151.2,
        "cash": 86.0,
        "fixed_income": 107.5,
        "us_stock": 856.8,
        "not_classified": 21.5,
        "other": 0.0,
    }

    actual = _process_all_pdf_table_funds(
        asset_information=asset_information,
        fund_name_to_ticker_mapping=fund_name_to_ticker_mapping,
        mid_url=mid_url,
        file_path=file_path,
        page_nums=page_nums,
        fund_name_lists=fund_name_lists,
    )

    assert actual == expected
