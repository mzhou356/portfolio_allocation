"""This module contain all functions that enable parsing a PDF file as a table
or text."""

from typing import Any, Dict, List
import pandas as pd
import PyPDF2
import tabula
from PyPDF2._page import PageObject


def load_pdf_statements(file_path: str) -> List[PageObject]:
    """
    Reads in statements in pdf formats.
    Args:
        file_path (str): statement filepath.

    Returns:
        a virtual list of page objects.
    """

    loaded_pdf = PyPDF2.PdfReader(stream=file_path)
    return loaded_pdf.pages


def parse_pdf_tables(
    file_path: str,
    page_num: int,
    pandas_options: Dict[str, Any],
    table_index_number: int,
    multiple_table_flag: bool,
) -> pd.DataFrame:
    """
    Reads in tables from a PDF file on a specific page.
    Args:
        file_path (str): statement filepath.
        page_num (int): the page number for the tables to parse,
        page one is 0.
        pandas_options (Dict[str, Any]): optional argument for the
        pandas method pd.read_csv.
        table_index_number (int): the table number after read in the tables
        as a list. table 1 is 0.
        multiple_table_flag (bool): only one table or multiple table in the page.

    Returns:
        a pandas dataframe with the parsed PDF table.
    """
    return tabula.read_pdf(
        input_path=file_path,
        multiple_tables=multiple_table_flag,
        pages=page_num,
        pandas_options=pandas_options,
    )[table_index_number]
