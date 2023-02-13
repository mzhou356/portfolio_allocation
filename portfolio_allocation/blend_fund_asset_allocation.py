from typing import Dict, Any, Set, Union, Callable

import pandas as pd

from portfolio_allocation import PORTFOLIO_BREAKDOWN
from portfolio_allocation.pdf_parser import parse_pdf_tables, load_pdf_statements

# combine_portfolios

# import pandas as pd
# import PyPDF2

# import tabula


DEFAULT_CHARS_TO_STRIP: str = "USD$"


def generate_blend_fund_asset_allocations():
    """Combine all"""


def _create_blend_fund_asset_allocation(
    fund_name: str, fund_mapping: Dict[str, Dict[str, float]], total_fund_value: float
) -> Dict[str, float]:
    """
    This prompts the user to enter the asset type and asset amount for
    a specified account_name for a non blend fund account.
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


# def generate_combined_blend_fund_asset_allocation() -> Dict[str, float]:
#     """
#     This function creates the combined asset allocation for all non blend
#     fund accounts.
#     Returns:
#     A dictionary with combined asset allocation for all accounts.
#     """
#     curr_portfolio: Dict[str, float] = {}
#     for account_name in ALL_CURRENT_ACCOUNTS:
#         curr_portfolio = combine_portfolios(
#             portfolio_a=curr_portfolio,
#             portfolio_b=create_blend_fund_asset_allocation(
#                 account_name=account_name,
#             ),
#         )
#     return curr_portfolio


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


def process_blend_fund_tables(
    file_path: str,
    page_num: int,
    pandas_options: Dict[str, Any],
    table_index_number: int,
    fund_names: Set[str],
    fund_column_name: Union[str, int],
    fund_row_index_start: int = 0,
    fund_row_index_end: int = -1,
    fund_col_parse_function: Union[None, Callable[[str], str]] = None,
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
        fund_names (Set[str]): a set of fund_names the PDF tables have information for.
        fund_column_name (Union[str, int]): fund column name as a string or an int depending
        on if the row is skipped after parsing.
        fund_row_index_start: which row to start for parsed pdf table. Default is 0.
        fund_row_index_end (int): which row to end for parsed pdf table. Default is -1.
        fund_col_parse_function (Callable[[str], str): Default None. If the rows are skipped and the table
        needs to be processed further to extract all fund names in proper format.
        fund_col_index_start (int): an argument for the fund_col_parse_function.
        fund_col_index_end (int): an argument for the fund_col_parse_function.
        fund_col_number (int): fund column number as an int after rows are skipped and only needed
        to get a list of funds as index for the table.
    Returns:
        A pandas series with index as the funds and series value as the total asset amount as
        text.
    """


def process_blend_fund_texts():
    """other funds"""
