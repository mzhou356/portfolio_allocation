"""This module turns dataframe into tables inside html and opens a local tab in the default
browser with allocation information."""

import webbrowser
from pathlib import Path

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
