# pylint: disable = too-many-locals, duplicate-code
"""This module tests all functions from module pdf_parser."""
import pandas as pd

from portfolio_allocation.pdf_parser import (
    load_pdf_statements,
    parse_pdf_tables,
    PyPDF2,
    tabula,
)


def test_load_pdf_statements_succeeds(pdf_statement_pages, mocker) -> None:
    """Test load_pdf_statements."""
    pdfreader_return_mock = mocker.Mock()
    pdfreader_return_mock.pages = pdf_statement_pages
    pdfreader_mock_method = mocker.patch.object(
        PyPDF2, "PdfReader", return_value=pdfreader_return_mock
    )
    file_path = "test_file_path"

    actual = load_pdf_statements(file_path=file_path)

    assert actual == pdf_statement_pages
    pdfreader_mock_method.assert_called_once_with(
        stream=file_path,
    )


def test_parse_pdf_tables_succeeds(blend_fund_table_one, mocker) -> None:
    """Test parse_pdf_tables."""
    tabula_read_pdf_mock_method = mocker.patch.object(
        tabula,
        "read_pdf",
        return_value=[blend_fund_table_one],
    )
    file_path = "test_file_path"
    multiple_tables = False
    pages = 0
    pandas_options = {"headers": None}
    table_index_number = 0

    actual = parse_pdf_tables(
        file_path=file_path,
        page_num=pages,
        multiple_table_flag=multiple_tables,
        table_index_number=table_index_number,
        pandas_options=pandas_options,
    )

    pd.testing.assert_frame_equal(left=actual, right=blend_fund_table_one)
    tabula_read_pdf_mock_method.assert_called_once_with(
        input_path=file_path,
        multiple_tables=multiple_tables,
        pages=pages,
        pandas_options=pandas_options,
    )
