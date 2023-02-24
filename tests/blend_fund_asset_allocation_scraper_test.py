"""This module tests all functions from module blend_fund_asset_allocation scraper."""
import pytest
from requests.exceptions import RequestException

from portfolio_allocation.blend_fund_asset_allocation_scraper import (
    _create_api_url_for_asset_allocation,
    _get_asset_allocation,
    _process_asset_allocation,
    requests,
)


def test__create_api_url_for_asset_allocation_succeeds(mocker) -> None:
    """Test create_api_url_for_asset_allocation."""
    fund_ticker = "test_fund_ticker"
    mid_url = "test_mid_url"
    content = """
    <sal-components tab="funds-portfolio" security-id="id" content-type="e7FDDltrTy+tA2"
    security-type="FE" data-v-23f1d76c data-v-d599d022></sal-components></section></div>
    """
    expected = (
        "https://api-global.morningstar.com/sal-service/v1/test_mid_ur/process/asset/"
        "v2/id/data?languageId=en&locale=en&clientId=MDC&benchmarkId=mstarorcat&"
        "component=sal-components-mip-asset-allocation&version=3.79.0"
    )
    mock_response = mocker.Mock()
    mock_response.content = content
    mocker.patch.object(requests, "get", return_value=mock_response)

    actual = _create_api_url_for_asset_allocation(
        fund_ticker=fund_ticker,
        mid_url=mid_url,
    )

    assert actual == expected


def test_get_asset_allocation_succeeds(mocker) -> None:
    """Test function get_asset_allocation."""
    asset_allocation_url = "test_url"
    api_key = "test_key"
    text = '{"allocationMap": "test"}'
    expected = "test"

    mock_response = mocker.Mock()
    mock_response.text = text
    mocker.patch.object(requests, "get", return_value=mock_response)

    actual = _get_asset_allocation(
        morningstar_asset_allocation_url=asset_allocation_url,
        api_key=api_key,
    )

    assert actual == expected


def test_get_asset_allocation_raises_request_exception(mocker, caplog) -> None:
    """Test function get_asset_allocation."""
    asset_allocation_url = "test_url"
    api_key = "test_key"
    mocker.patch.object(requests, "get", side_effect=RequestException)
    expected_log = (
        "Please go to morningstar to retrieve an updated api key "
        "for asset allocation and update default api key."
    )

    with pytest.raises(RequestException):
        _get_asset_allocation(
            morningstar_asset_allocation_url=asset_allocation_url,
            api_key=api_key,
        )
    assert expected_log in caplog.text


def test_process_asset_allocation() -> None:
    """Test process_asset_allocation."""
    raw_asset_allocation_map = {
        "AssetAllocCash": {"netAllocation": "2.21496"},
        "AssetAllocNotClassified": {"netAllocation": "2.1495699999999998"},
        "AssetAllocNonUSEquity": {"netAllocation": "14.48973"},
        "AssetAllocOther": {"netAllocation": "0.00000"},
        "AssetAllocUSEquity": {"netAllocation": "51.33144"},
        "AssetAllocBond": {"netAllocation": "29.81429"},
    }

    expected = {
        "cash": 0.022149600000000002,
        "fixed_income": 0.2981429,
        "international_stock": 0.1448973,
        "not_classified": 0.021495699999999996,
        "other": 0.0,
        "us_stock": 0.5133144000000001,
    }

    actual = _process_asset_allocation(
        raw_asset_allocation_mapping=raw_asset_allocation_map,
    )

    assert actual == expected
