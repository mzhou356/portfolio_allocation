"""This module tests all functions from module generate_html_outputs."""
import builtins
from unittest.mock import call

import pytest
from portfolio_allocation.generate_html_outputs import (
    open_local_html,
    webbrowser,
    _convert_df_to_html_table,
    _update_asset_allocation_table,
    update_asset_allocation_html,
    AssetTableType,
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


@pytest.mark.parametrize(
    "asset_table_lines, asset_table_type, expected",
    [
        (
            "asset_allocation_by_asset_class_html_table_lines",
            AssetTableType.NON_REGION,
            "html_asset_class_table_output",
        ),
        (
            "asset_allocation_by_asset_class_and_region_html_table_lines",
            AssetTableType.REGION,
            "html_asset_class_region_table_output",
        ),
    ],
)
def test_update_asset_allocation_table_succeeds(
    asset_table_lines,
    asset_table_type,
    expected,
    request,
    html_data,
) -> None:
    """Test update_asset_allocation_table."""
    asset_table_lines = request.getfixturevalue(asset_table_lines)
    expected = request.getfixturevalue(expected)

    actual = _update_asset_allocation_table(
        html_data=html_data,
        asset_table_lines=asset_table_lines,
        asset_table_type=asset_table_type,
    )

    assert actual == expected


def test_update_asset_allocation_html(
    asset_allocation_by_asset_class_table,
    asset_allocation_by_asset_class_and_region_table,
    mocker,
) -> None:
    """Test update_asset_allocation_html."""
    local_path = "test_path"
    mock_open_method = mocker.patch.object(builtins, "open")
    mock_convert_df_to_html = mocker.patch(
        "portfolio_allocation.generate_html_outputs._convert_df_to_html_table",
    )
    mock_update_allocation_table = mocker.patch(
        "portfolio_allocation.generate_html_outputs._update_asset_allocation_table",
    )

    update_asset_allocation_html(
        asset_table_with_region=asset_allocation_by_asset_class_and_region_table,
        asset_table_without_region=asset_allocation_by_asset_class_table,
        file_path=local_path,
    )

    mock_convert_df_to_html.has_calls(
        [
            call(asset_table=asset_allocation_by_asset_class_table),
            call(asset_table=asset_allocation_by_asset_class_and_region_table),
        ]
    )
    mock_update_allocation_table.assert_called()
    mock_open_method.assert_called()
