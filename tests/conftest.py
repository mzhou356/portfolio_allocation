# pylint: disable = missing-function-docstring, redefined-outer-name,
# pylint: disable = missing-module-docstring
from typing import List, Dict

import pandas as pd
import pytest


@pytest.fixture(scope="function")
def pdf_text_page_one() -> str:
    return """
    fund_A info_1 info_2 $250.27
    fund_B info_1 info_2 $36.28
    fund_C info_1 info_2 $.25
    """


@pytest.fixture(scope="function")
def pdf_text_page_two() -> str:
    return """
    fund_E info_3 info_4 $1,250.27
    fund_F info_3 info_4 $125,036.28
    """


@pytest.fixture(scope="function")
def pdf_statement_pages(pdf_text_page_one, pdf_text_page_two, mocker) -> List:
    page_zero = mocker.Mock()
    page_one = mocker.Mock()
    page_two = mocker.Mock()
    page_zero.extract_text.return_value = ""
    page_one.extract_text.return_value = pdf_text_page_one
    page_two.extract_text.return_value = pdf_text_page_two
    return [page_zero, page_one, page_two]


@pytest.fixture(scope="function")
def blend_fund_asset_allocation() -> Dict[str, Dict[str, float]]:
    return {
        "A": {"us_stock": 1},
        "B": {"international_stock": 0.75, "fixed_income": 0.25},
        "C": {"other": 0.25, "us_stock": 0.50, "fixed_income": 0.25},
        "E": {"not_classified": 0.5, "fixed_income": 0.5},
        "F": {"us_stock": 0.75, "international_stock": 0.25},
    }


@pytest.fixture(scope="function")
def expected_text_fund_asset_allocation() -> Dict[str, float]:
    return {
        "us_stock": 94027.605,
        "international_stock": 31286.28,
        "fixed_income": 634.2675,
        "other": 0.0625,
        "not_classified": 625.135,
        "cash": 0.0,
    }


@pytest.fixture(scope="function")
def blend_fund_table_one() -> pd.DataFrame:
    return pd.DataFrame(
        {"balance": [100, 000.25, 125.65, 3000.28], "change_in_value": [-10, 5, 0]},
        index=["fund_a", "fund_b", "fund_c"],
    )


@pytest.fixture(scope="function")
def blend_fund_table_one_output() -> pd.Series:
    return pd.Series(
        [100, 000.25, 125.65, 3000.28], index=["fund_a", "fund_b", "fund_c"]
    )


@pytest.fixture(scope="function")
def blend_fund_table_two() -> pd.DataFrame:
    return pd.DataFrame(
        {"name": ["fund_e yes", "fund_f no"], "value": [215.0, 1008.0]}, index=[0, 1]
    )


@pytest.fixture(scope="function")
def blend_fund_table_two_output() -> pd.Series:
    return pd.Series([215.0, 1008.0], index=["fund_e", "fund_f"])
