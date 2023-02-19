# pylint: disable=no-name-in-module, import-error
"""This module contains functions that gets the more real time mutual fund or
etf fund asset allocations for the blend fund asset allocation calculation. """
import json
import logging
from typing import Dict

import requests
from bs4 import BeautifulSoup

from portfolio_allocation.configuration import DEFAULT_API_KEY
from portfolio_allocation import PORTFOLIO_BREAKDOWN

MORNINGSTAR_FRONT_URL: str = "https://www.morningstar.com"
MORNINGSTAR_END_URL: str = "portfolio"
BEAUTIFULSOUP_PARSER: str = "html.parser"
SECURITY_ID_HTML_TAG_NAME: str = "sal-components"
SECURITY_ID_HTML_ATTRIBUTE_NAME: str = "security-id"
MORNINGSTAR_API_FRONT_URL: str = "https://api-global.morningstar.com/sal-service/v1"
MORNINGSTAR_API_MID_URL: str = "process/asset/v2"
MORNINGSTAR_API_END_URL: str = (
    "data?languageId=en&locale=en&clientId=MDC&benchmarkId=mstarorcat&component="
    "sal-components-mip-asset-allocation&version=3.79.0"
)
REQUEST_TIME_OUT: int = 60

RAW_TO_STANDARDIZED_PORTFOLIO_KEY_MAPPING: Dict[str, str] = {
    "AssetAllocCash": "cash",
    "AssetAllocNotClassified": "not_classified",
    "AssetAllocNonUSEquity": "international_stock",
    "AssetAllocOther": "other",
    "AssetAllocUSEquity": "us_stock",
    "AssetAllocBond": "fixed_income",
}

DEFAULT_ALLOCATION_TYPE: str = "netAllocation"
PERCENT_FACTOR: float = 100.0

LOGGER = logging.getLogger(__name__)


def blend_fund_asset_allocation_generator(
    fund_name_to_ticker_mapping: Dict[str, str], mid_url: str
) -> Dict[str, Dict[str, float]]:
    """
    Creates asset allocation information for all funds for a given account.
    Args:
        fund_name_to_ticker_mapping (Dict[str, str]): A dictionary containing all funds
        in a blend account with
        ticker symbol mapping as value.
        mid_url (str): the base url that differentiates between etfs and mutual_funds.


    Returns:
        A dictionary containing asset allocation for all funds in a blend fund account.
    """
    blend_fund_account_mapping = {}
    for fund_name, ticker in fund_name_to_ticker_mapping.items():
        fund_api_url = _create_api_url_for_asset_allocation(
            fund_ticker=ticker,
            mid_url=mid_url,
        )
        raw_fund_asset_mapping = _get_asset_allocation(
            morningstar_asset_allocation_url=fund_api_url
        )
        blend_fund_account_mapping[fund_name] = _process_asset_allocation(
            raw_fund_asset_mapping
        )
    return blend_fund_account_mapping


def _create_api_url_for_asset_allocation(fund_ticker: str, mid_url: str) -> str:
    """
    Creates the api url to retrieve asset allocation information from morningstar.
    Args:
        fund_ticker (str): a ticker symbol for a specific ETF or mutual fund.
        mid_url (str): the base url that differentiates between etfs and mutual_funds.
    Returns:
        an api url that retrieves the asset allocation information.
    """
    response = requests.get(
        f"{MORNINGSTAR_FRONT_URL}/{mid_url}/{fund_ticker}/{MORNINGSTAR_END_URL}",
        timeout=REQUEST_TIME_OUT,
    )
    soup = BeautifulSoup(response.content, BEAUTIFULSOUP_PARSER)
    security_id = soup.find(SECURITY_ID_HTML_TAG_NAME)[SECURITY_ID_HTML_ATTRIBUTE_NAME]
    return (
        f"{MORNINGSTAR_API_FRONT_URL}/{mid_url.split('/')[0][:-1]}/"
        f"{MORNINGSTAR_API_MID_URL}/{security_id}/{MORNINGSTAR_API_END_URL}"
    )


def _get_asset_allocation(
    morningstar_asset_allocation_url: str, api_key: str = DEFAULT_API_KEY
) -> Dict[str, Dict[str, float]]:
    """
    Retrieves asset allocation for a specific blend fund from morningstar website.
    Args:
        morningstar_asset_allocation_url (str): api url to retrieve the asset allocation
        url.
        api_key (str): api key to retrieve asset allocation informatin.

    Returns:
        A dictionary of dictionary containing asset allocation information.
    """
    try:
        asset_content = requests.get(
            morningstar_asset_allocation_url,
            headers={
                "apikey": api_key,
            },
            timeout=REQUEST_TIME_OUT,
        )
    except requests.exceptions.RequestException as exc:
        LOGGER.error(
            "Please go to morningstar to retrieve an updated api key "
            "for asset allocation and update default api key."
        )
        raise exc
    return json.loads(asset_content.text)["allocationMap"]


def _process_asset_allocation(
    raw_asset_allocation_mapping: Dict[str, Dict[str, float]]
) -> Dict[str, float]:
    """
    Parse raw asset allocation into standardized format that follow
    PORTFOLIO_BREAKDOWN format.
    Args:
        raw_asset_allocation_mapping (Dict[str, Dict[str, float]]):
        Raw asset allocation from morning star api contains various asset
        value such net, long, short, historical benchmark as well.

    Returns:
        A standardized asset allocation that follow PORTFOLIO_BREAKDOWN format
        from init file.
    """
    standardized_portfolio_mapping = PORTFOLIO_BREAKDOWN.copy()
    for asset_type, allocation_mapping in raw_asset_allocation_mapping.items():
        standardized_portfolio_mapping[
            RAW_TO_STANDARDIZED_PORTFOLIO_KEY_MAPPING[asset_type]
        ] += (float(allocation_mapping[DEFAULT_ALLOCATION_TYPE]) / PERCENT_FACTOR)
    return standardized_portfolio_mapping
