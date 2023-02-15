# pylint: disable=import-error, too-many-locals
"""This module calculates asset_allocation for all accounts with just one or
more blend type funds or funds."""
from typing import Dict, Any, Set, Union, Callable, List, Optional

import pandas as pd

from portfolio_allocation import PORTFOLIO_BREAKDOWN, combine_portfolios
from portfolio_allocation.pdf_parser import parse_pdf_tables, load_pdf_statements
from portfolio_allocation.blend_fund_asset_allocation_generator import (
    blend_fund_asset_allocation_generator,
)
from portfolio_allocation.configuration import (
    ALL_CURRENT_BLEND_ACCOUNTS,
    BLEND_FUND_ACCOUNT_TO_ASSET_CALCULATION_MAPPING,
)

DEFAULT_CHARS_TO_STRIP: str = "USD$"


def generate_combined_blend_fund_asset_allocation() -> Dict[str, float]:
    """
    This function creates the combined asset allocation for all non blend
    fund accounts.
    Returns:
    A dictionary with combined asset allocation for all accounts.
    """
    combined_blend_fund_asset_allocation = PORTFOLIO_BREAKDOWN.copy()
    for blend_account in ALL_CURRENT_BLEND_ACCOUNTS:
        asset_information = BLEND_FUND_ACCOUNT_TO_ASSET_CALCULATION_MAPPING[
            blend_account
        ]
        file_path = asset_information["file_path"]
        fund_name_to_ticker_mapping = asset_information["fund_name_to_ticker_mapping"]
        page_nums = asset_information["page_nums"]
        fund_name_lists = asset_information["fund_name_lists"]
        mid_url = asset_information["mid_url"]
        if asset_information["pdf_table_parse"]:
            curr_account_portfolio = _process_all_pdf_table_funds(
                asset_information=asset_information,
                fund_name_to_ticker_mapping=fund_name_to_ticker_mapping,
                mid_url=mid_url,
                file_path=file_path,
                page_nums=page_nums,
                fund_name_lists=fund_name_lists,
            )
        else:
            curr_account_portfolio = _process_all_text_funds(
                asset_information=asset_information,
                fund_name_to_ticker_mapping=fund_name_to_ticker_mapping,
                mid_url=mid_url,
                file_path=file_path,
                page_nums=page_nums,
                fund_name_lists=fund_name_lists,
            )

        combined_blend_fund_asset_allocation = combine_portfolios(
            portfolio_a=combined_blend_fund_asset_allocation,
            portfolio_b=curr_account_portfolio,
        )
    return combined_blend_fund_asset_allocation


def _process_all_text_funds(
    asset_information: Dict[str, Any],
    fund_name_to_ticker_mapping: List[Dict[str, str]],
    mid_url: List[str],
    file_path: str,
    page_nums: List[int],
    fund_name_lists: List[List[str]],
) -> Dict[str, float]:
    """
    This function gathers all non pdf table funds and creates the combined
    asset allocation.
    Args:
        asset_information (Dict[str, Any]): asset and fund parse information for
        a specific account.
        fund_name_to_ticker_mapping (Dict[str, str]): A dictionary containing all funds
        in a blend account with
        ticker symbol mapping as value.
        mid_url (str): the base url that differentiates between etfs and mutual_funds.
        file_path (str): statement filepath.
        page_nums (List[int]): the page numbers for the tables to parse, page one is 0.
        fund_name_lists (List[List[str]]): a set of fund_names the PDF text has information for.
    Returns:
        Fund asset allocation in the standardized portfolio_breakdown
       format.
    """
    fund_value_index_number = asset_information["fund_value_index_number"]
    amount_str_filter = asset_information.get("asset_str_filter")
    for index, sub_account in enumerate(fund_name_lists):
        blend_fund_asset_allocation = blend_fund_asset_allocation_generator(
            fund_name_to_ticker_mapping=fund_name_to_ticker_mapping[index],
            mid_url=mid_url[index],
        )
        curr_account_portfolio = _process_blend_fund_texts(
            file_path=file_path,
            target_page_num=page_nums[index],
            blend_fund_asset_allocation=blend_fund_asset_allocation,
            fund_names=sub_account,
            fund_value_index_number=fund_value_index_number[index],
            amount_str_filter=amount_str_filter[index] if amount_str_filter else None,
        )
    return curr_account_portfolio


def _process_all_pdf_table_funds(
    asset_information: Dict[str, Any],
    fund_name_to_ticker_mapping: List[Dict[str, str]],
    mid_url: List[str],
    file_path: str,
    page_nums: List[int],
    fund_name_lists: List[List[str]],
) -> Dict[str, float]:
    """
    This function gathers all pdf table funds and creates the combined
    asset allocation.
    Args:
        asset_information (Dict[str, Any]): asset and fund parse information for
        a specific account.
        fund_name_to_ticker_mapping (Dict[str, str]): A dictionary containing all funds
        in a blend account with
        ticker symbol mapping as value.
        mid_url (str): the base url that differentiates between etfs and mutual_funds.
        file_path (str): statement filepath.
        page_nums (List[int]): the page numbers for the tables to parse, page one is 0.
        fund_name_lists (List[List[str]]): a set of fund_names the PDF text has information for.
    Returns:
        Fund asset allocation in the standardized portfolio_breakdown
       format.
    """
    all_processed_fund_tables = []
    pandas_parse_options = asset_information["pandas_parse_options"]
    table_index_numbers = asset_information["table_index_number"]
    fund_value_column_names = asset_information["fund_value_column_names"]
    fund_col_parse_function = asset_information["fund_col_parse_function"]
    fund_row_index_start = asset_information["fund_row_index_start"]
    for index, sub_account in enumerate(fund_name_lists):
        blend_fund_asset_allocation = blend_fund_asset_allocation_generator(
            fund_name_to_ticker_mapping=fund_name_to_ticker_mapping[index],
            mid_url=mid_url[index],
        )
        fund_information = _process_blend_fund_tables(
            file_path=file_path,
            page_num=page_nums[index],
            pandas_options=pandas_parse_options[index],
            table_index_number=table_index_numbers[index],
            fund_names=sub_account,
            fund_value_column_name=fund_value_column_names[index],
            fund_row_index_start=fund_row_index_start[index],
            fund_col_parse_function=_process_fund_name_columns
            if fund_col_parse_function[index]
            else None,
        )
        all_processed_fund_tables.append(fund_information)
    curr_account_portfolio = _create_asset_allocation_from_pdf_tables(
        blend_fund_asset_allocation=blend_fund_asset_allocation,
        fund_list=all_processed_fund_tables,
        vested_pct=asset_information["vested_pct"],
    )
    return curr_account_portfolio


def _create_blend_fund_asset_allocation(
    fund_name: str, fund_mapping: Dict[str, Dict[str, float]], total_fund_value: float
) -> Dict[str, float]:
    """
    This calculates the asset allocation for a specific blend fund.
    Args:
        fund_name (str): the name of the mutual fund in the specific financial
        account.
        total_fund_value (float): total asset amount in US dollar for the
        entire blend fund.
        fund_mapping (Dict[str, float]): mapping of the asset allocation
        for the specific fund.
    Returns:
         A dictionary with asset allocation calculated for the specific
         blend fund.
    """
    curr_portfolio = PORTFOLIO_BREAKDOWN.copy()
    for asset_type in curr_portfolio:
        curr_portfolio[asset_type] = (
            fund_mapping[fund_name].get(asset_type, 0) * total_fund_value
        )
    return curr_portfolio


def _extract_dollar_amount(
    asset_amount: str, chars_to_strip: str = DEFAULT_CHARS_TO_STRIP
) -> float:
    """
    Takes a string object and converts the input into a float value in
    unit of US Dollar.
    Args:
        asset_amount (str): the asset_amount extracted from PDF in a string format.
        chars_to_strip (str): characters to strip for parsing logic to work.

    Returns:
        A float in unit of US Dollar.
    """
    dollar_amount = asset_amount.strip(chars_to_strip).split(",")
    power = 0
    parsed_dollar_amount = 0
    for amount in dollar_amount[::-1]:
        parsed_dollar_amount += float(amount) * 10**power
        power += 3
    return parsed_dollar_amount


def _process_fund_name_columns(
    text_with_fund_name: str,
    fund_col_index_start: int,
    fund_col_index_end: int,
) -> str:
    """
    This function takes the text with fund name and does simple
    string process to get only the fund name as a string.
    Args:
        text_with_fund_name (str): a text containing fund name.
        fund_col_index_start (int): the starting index with fund name.
        fund_col_index_end (int): the ending index with fund name.

    Returns:
        fund name only as a string.
    """
    return " ".join(
        text_with_fund_name.split()[fund_col_index_start:fund_col_index_end]
    )


def _process_blend_fund_tables(
    file_path: str,
    page_num: int,
    pandas_options: Dict[str, Any],
    table_index_number: int,
    fund_names: List[str],
    fund_value_column_name: Union[str, int],
    fund_row_index_start: int = 0,
    fund_row_index_end: int = -1,
    fund_col_parse_function: Union[None, Callable[[str, int, int], str]] = None,
    fund_col_index_start: int = 0,
    fund_col_index_end: int = -1,
    fund_col_number: int = 0,
) -> pd.Series:
    """

    Args:
        file_path (str): statement filepath.
        page_num (int): the page number for the tables to parse, page one is 0.
        pandas_options (Dict[str, Any]): optional argument for the pandas method
        pd.read_csv.
        table_index_number (int): the table number after read in the tables as a list.
        table 1 is 0.
        fund_names (List[str]): a set of fund_names the PDF tables have information for.
        fund_value_column_name (Union[str, int]): fund column name as a string or an int
        depending on if the row is skipped after parsing. This column gives the asset
        amount as text.
        fund_row_index_start: which row to start for parsed pdf table. Default is 0.
        fund_row_index_end (int): which row to end for parsed pdf table. Default is -1.
        fund_col_parse_function (Callable[[str, int, int], str): Default None. If the rows are skipped and the table
        needs to be processed further to extract all fund names in proper format as table indices.
        fund_col_index_start (int): an argument for the fund_col_parse_function.
        fund_col_index_end (int): an argument for the fund_col_parse_function.
        fund_col_number (int): fund column number as an int after rows are skipped and only needed
        to get a list of funds as index for the table.
    Returns:
        A pandas series with index as the funds and series value as the total asset amount as
        text.
    """
    parsed_pdf_table = parse_pdf_tables(
        file_path=file_path,
        page_num=page_num,
        pandas_options=pandas_options,
        table_index_number=table_index_number,
    )
    if fund_col_parse_function:
        parsed_pdf_table = parsed_pdf_table.iloc[
            fund_row_index_start:fund_row_index_end
        ]
        fund_indices = parsed_pdf_table[fund_col_number].apply(
            lambda text_with_fund_name: fund_col_parse_function(
                text_with_fund_name,
                fund_col_index_start,
                fund_col_index_end,
            )
        )
        parsed_pdf_table.index = fund_indices
    return parsed_pdf_table.loc[fund_names][fund_value_column_name]


def _create_asset_allocation_from_pdf_tables(
    blend_fund_asset_allocation: Dict[str, Dict[str, float]],
    fund_list: List[pd.Series],
    vested_pct: float,
) -> Dict[str, float]:
    """
    This function extracts blend fund asset allocation from pdf tables
    after a list of pandas series were created from the pdf tables.

    Args:
        blend_fund_asset_allocation (Dict[str, Dict[str, float]]): asset
        allocation for a blend fund account with blend fund as name and
        asset allocation as value.
        fund_list (List[pd.Series]): A list of pandas series containing
        fund name as index and fund asset value as series value.
        vested_pct (float): a fraction. Amount that actually
        vested.
    Returns:
        Fund asset allocation in the standardized portfolio_breakdown
        format.
    """
    final_portfolio_breakdown = PORTFOLIO_BREAKDOWN.copy()
    combined_fund_information = pd.concat(fund_list)
    for fund_name in combined_fund_information:
        total_fund_value = _extract_dollar_amount(
            asset_amount=combined_fund_information.loc[fund_name] * vested_pct
        )
        fund_portfolio_breakdown = _create_blend_fund_asset_allocation(
            fund_name=fund_name,
            fund_mapping=blend_fund_asset_allocation,
            total_fund_value=total_fund_value,
        )
        final_portfolio_breakdown = combine_portfolios(
            portfolio_a=final_portfolio_breakdown,
            portfolio_b=fund_portfolio_breakdown,
        )

    return final_portfolio_breakdown


def _relevant_page_filter(
    page_number: int, target_page_num: Union[int, Set[int]]
) -> bool:
    """
    This function takes in page_number and decides if it is part of the
    target_page_num.
    Args:
        page_number (int): the page number on the PDF. page 1 is 0.
        target_page_num (Union[int, Set[int]]): could be a single page or
        a set of pages.
    Returns:
        true if it is part of the target page else false.
    """
    return (isinstance(target_page_num, int) and page_number == target_page_num) or (
        isinstance(target_page_num, set) and page_number in target_page_num
    )


def _extract_fund_value_from_text_line(
    text_line: str,
    fund_value_index_number: int,
    amount_str_filter: Optional[str] = None,
) -> float:
    """
    Extract fund value from text line as US dollars.
    Args:
        text_line:
        amount_str_filter (str): if the line containing the fund amount needs to
        have text filter, then this str filter is passed in. This returns all text
        containing the str.
        fund_value_index_number (int): the index for where the fund value is
        inside the text.
    Returns:
        US dollars amount for the specific fund.
    """
    if amount_str_filter:
        total_fund_value = _extract_dollar_amount(
            asset_amount=[
                char for char in text_line.split() if amount_str_filter in char
            ][fund_value_index_number]
        )
    else:
        total_fund_value = _extract_dollar_amount(
            asset_amount=text_line.split()[fund_value_index_number]
        )
    return total_fund_value


def _process_blend_fund_texts(
    file_path: str,
    target_page_num: Union[int, Set[int]],
    blend_fund_asset_allocation: Dict[str, Dict[str, float]],
    fund_names: List[str],
    fund_value_index_number: int,
    amount_str_filter: Optional[str] = None,
) -> Dict[str, float]:
    """
     This function extracts blend fund asset allocation from pdf text.

     Args:
         file_path (str): statement filepath.
         target_page_num (Union[int, Set[int]]): the page number or page number set
         for the text to parse, page 1 is 0.
         blend_fund_asset_allocation (Dict[str, Dict[str, float]]): asset
         allocation for a blend fund account with blend fund as name and
         asset allocation as value.
         fund_names (List[str]): a set of fund_names the PDF text has information for.
         fund_value_index_number (int): the index for where the fund value is
         inside the text.
         amount_str_filter (Optional[str]): if the line containing the fund amount needs to
         have text filter, then this str filter is passed in. This returns all text
         containing the str.
    Returns:
       Fund asset allocation in the standardized portfolio_breakdown
       format.
    """
    final_portfolio_breakdown = PORTFOLIO_BREAKDOWN.copy()
    num_of_funds = len(fund_names)
    fund_index = 0
    loaded_pdf_pages = load_pdf_statements(
        file_path=file_path,
    )
    for page_num, page_content in enumerate(loaded_pdf_pages):
        if _relevant_page_filter(
            page_number=page_num,
            target_page_num=target_page_num,
        ):
            for text_line in page_content.extract_text().split("\n"):
                if fund_index == num_of_funds:
                    return final_portfolio_breakdown
                fund_name = fund_names[fund_index]
                if fund_name in text_line:
                    total_fund_value = _extract_fund_value_from_text_line(
                        text_line=text_line,
                        amount_str_filter=amount_str_filter,
                        fund_value_index_number=fund_value_index_number,
                    )
                    fund_portfolio_breakdown = _create_blend_fund_asset_allocation(
                        fund_name=fund_name,
                        fund_mapping=blend_fund_asset_allocation,
                        total_fund_value=total_fund_value,
                    )
                    final_portfolio_breakdown = combine_portfolios(
                        portfolio_a=final_portfolio_breakdown,
                        portfolio_b=fund_portfolio_breakdown,
                    )
                    fund_index += 1
    return final_portfolio_breakdown
