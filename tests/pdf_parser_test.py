# pylint: disable = too-many-locals, duplicate-code
"""This module tests all functions from module pdf_parser."""
from portfolio_allocation.pdf_parser import load_pdf_statements, parse_pdf_tables


def test_load_pdf_statements_succeeds(mocker, pdf_statement_pages) -> None:
    """Test load_pdf_statements."""


def test_parse_pdf_tables_succeeds(mocker, blend_fund_table_one) -> None:
    """Test parse_pdf_tables."""
