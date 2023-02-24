"""This module tests all functions from module blend_fund_asset_allocation scraper."""
from portfolio_allocation.blend_fund_asset_allocation_scraper import (
    _create_api_url_for_asset_allocation,
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
