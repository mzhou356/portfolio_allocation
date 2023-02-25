"""This module tests all functions from module generate_html_outputs."""
import pytest

from portfolio_allocation.generate_html_outputs import (
    open_local_html,
    webbrowser,
    _convert_df_to_html_table,
)
from portfolio_allocation import ROOT_DIR


def test_open_local_html_succeeds(mocker) -> None:
    """Test open_local_html."""
    webbrowser_mock_method = mocker.patch.object(webbrowser, "open")
    local_path = "test_path"

    open_local_html(local_path=local_path)

    webbrowser_mock_method.assert_called_once_with(
        url="file://" + str(ROOT_DIR / local_path)
    )


@pytest.mark.parametrize(
    "asset_table, expected",
    [
        (
            "asset_allocation_by_asset_class_table",
            "asset_allocation_by_asset_class_html_table_lines",
        ),
        (
            "asset_allocation_by_asset_class_and_region_table",
            "asset_allocation_by_asset_class_and_region_html_table_lines",
        ),
    ],
)
def test_convert_df_to_html_table_succeeds(
    asset_table,
    expected,
    request,
) -> None:
    """Test convert_df_to_html_table"""

    asset_table = request.getfixturevalue(asset_table)
    expected = request.getfixturevalue(expected)

    actual = _convert_df_to_html_table(
        asset_table=asset_table,
    )

    assert actual == expected
