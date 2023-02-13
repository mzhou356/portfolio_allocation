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

    loaded_pdf = PyPDF2.PdfReader(file_path)
    return loaded_pdf.pages


def parse_pdf_tables(
    file_path: str,
    page_num: int,
    pandas_options: Dict[str, Any],
    table_index_number: int,
) -> pd.DataFrame:
    """
    Reads in tables from a PDF file on a specific page.
    Args:
        file_path (str): statement filepath.
        page_num (int): the page number for the tables to parse, page one is 0.
        pandas_options (Dict[str, Any]): optional argument for the pandas method
        pd.read_csv.
        table_index_number (int): the table number after read in the tables as a list.
        table 1 is 0.

    Returns:
        a pandas dataframe with the parsed PDF table.
    """
    return tabula.read_pdf(
        input_path=file_path,
        pages=page_num,
        multiple_tables=False,
        pandas_options=pandas_options,
    )[table_index_number]
