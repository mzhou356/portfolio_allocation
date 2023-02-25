"""This module tests all functions from module generate_html_outputs."""

from portfolio_allocation.generate_html_outputs import open_local_html, webbrowser
from portfolio_allocation import ROOT_DIR


def test_open_local_html_succeeds(mocker) -> None:
    """Test open_local_html."""
    webbrowser_mock_method = mocker.patch.object(webbrowser, "open")
    local_path = "test_path"

    open_local_html(local_path=local_path)

    webbrowser_mock_method.assert_called_once_with(
        url="file://" + str(ROOT_DIR / local_path)
    )
