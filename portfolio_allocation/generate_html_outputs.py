"""This module turns dataframe into tables inside html and opens a local tab in the default
browser with allocation information."""

import webbrowser
from pathlib import Path
from typing import List

import pandas as pd

ROOT_DIR: Path = Path(__file__).parent

DEFAULT_PATH: str = "asset_allocation.html"


def open_local_html(local_path: str = DEFAULT_PATH) -> None:
    """
    This function opens a local html file and opens a tab in the default browser.
    Args:
        local_path (str): the local path where the html file is. Defaults to the
        DEFAULT PATH.
    """
    webbrowser.open(url="file://" + str(ROOT_DIR / local_path))


def _convert_pdf_to_html_table(asset_table: pd.DataFrame) -> List[str]:
    """
    Returns a list of html text as a table.
    Args:
        asset_table (pd.DataFrame): asset allocation table.
    Returns:
        a list of html text for the html table.
    """
    return ["a", "b"]


def update_asset_allocation_html(
    asset_table_without_region: pd.DataFrame,
    asset_table_with_region: pd.DataFrame,
    file_path: str,
) -> None:
    """
    This function updates the existing html table.
    Args:
        asset_table_without_region (pd.DataFrame): asset allocation table without region information.
        asset_table_with_region (pd.DataFrame): asset allocation table with region information.
        file_path (str): local file path for the html file.
    """
