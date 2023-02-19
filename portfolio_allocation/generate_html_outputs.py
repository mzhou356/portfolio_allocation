"""This module turns dataframe into tables inside html and opens a local tab in
the default browser with allocation information."""

import webbrowser
from typing import List, Tuple
from enum import Enum

import pandas as pd

from portfolio_allocation import ROOT_DIR

DEFAULT_PATH: str = "asset_allocation.html"
ASSET_CLASS_TABLE_START_END_LINE_INDICES: Tuple[int, int] = (45, 79)
REGION_TABLE_START_END_LINE_INDICES: Tuple[int, int] = (93, 128)
DEFAULT_INDENT: str = 3 * "\t"
DEFAULT_END: str = "\n"


class AssetTableType(Enum):
    """
    This Enum Class ensures the html table lines can only be
    ASSET without region and Asset with Region.
    """

    REGION = 1
    NON_REGION = 2


def open_local_html(local_path: str = DEFAULT_PATH) -> None:
    """
    This function opens a local html file and opens a tab in the default browser.
    Args:
        local_path (str): the local path where the html file is. Defaults to the
        DEFAULT PATH.
    """
    webbrowser.open(url="file://" + str(ROOT_DIR / local_path))


def _convert_df_to_html_table(asset_table: pd.DataFrame) -> List[str]:
    """
    Returns a list of html text as a table.
    Args:
        asset_table (pd.DataFrame): asset allocation table.
    Returns:
        a list of html text for the html table.
    """
    output_html_table_lines = []
    for _, record in asset_table.iterrows():
        output_html_table_lines.append("\t\t<tr>\n")
        output_html_table_lines.append(
            f"{DEFAULT_INDENT}<td>{record.name}</td>{DEFAULT_END}"
        )
        for row_value in record:
            output_html_table_lines.append(
                f"{DEFAULT_INDENT}<td>{row_value}</td>{DEFAULT_END}"
            )
        output_html_table_lines.append("\t\t</tr>\n")
    return output_html_table_lines


def _update_asset_allocation_table(
    html_data: List[str],
    asset_table_lines: List[str],
    asset_table_type: AssetTableType,
) -> List[str]:
    """
    This function updates the asset allocation html file for a specific
    asset table dataframe.
    Args:
        html_data (List[str]): all the html file lines.
        asset_table_lines (List[str]): a list of html text for the html table.
        asset_table_type (AssetTableType, Enum): either REGION or NON_REGION.
    Returns:
        all the html file lines with the table lines updated.
    """
    html_data = html_data.copy()
    if asset_table_type is AssetTableType.REGION:
        start_index, end_index = REGION_TABLE_START_END_LINE_INDICES
    else:
        start_index, end_index = ASSET_CLASS_TABLE_START_END_LINE_INDICES
    html_data[start_index : (end_index + 1)] = asset_table_lines
    return html_data


def update_asset_allocation_html(
    asset_table_without_region: pd.DataFrame,
    asset_table_with_region: pd.DataFrame,
    file_path: str = DEFAULT_PATH,
) -> None:
    """
    This function updates the existing html table.
    Args:
        asset_table_without_region (pd.DataFrame): asset allocation table without region
        information.
        asset_table_with_region (pd.DataFrame): asset allocation table with region
        information.
        file_path (str): local file path for the html file. It uses default_path if
        not provided.
    """
    asset_table_without_region_lines = _convert_df_to_html_table(
        asset_table=asset_table_without_region
    )
    asset_table_with_region_lines = _convert_df_to_html_table(
        asset_table=asset_table_with_region
    )
    with open(ROOT_DIR / file_path, "r", encoding="utf-8") as html_file:
        html_data = html_file.readlines()

    html_data = _update_asset_allocation_table(
        html_data=html_data,
        asset_table_lines=asset_table_without_region_lines,
        asset_table_type=AssetTableType.NON_REGION,
    )

    html_data = _update_asset_allocation_table(
        html_data=html_data,
        asset_table_lines=asset_table_with_region_lines,
        asset_table_type=AssetTableType.REGION,
    )
    with open(ROOT_DIR / file_path, "w", encoding="utf-8") as html_file:
        html_file.writelines(html_data)
