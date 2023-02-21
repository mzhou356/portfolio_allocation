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
def blend_fund_asset_allocation_text_fund() -> Dict[str, Dict[str, float]]:
    return {
        "A": {"us_stock": 1},
        "B": {"international_stock": 0.75, "fixed_income": 0.25},
        "C": {"other": 0.25, "us_stock": 0.50, "fixed_income": 0.25},
        "E": {"not_classified": 0.5, "fixed_income": 0.5},
        "F": {"us_stock": 0.75, "international_stock": 0.25},
    }


@pytest.fixture(scope="function")
def blend_fund_asset_allocation_table_fund() -> Dict[str, Dict[str, float]]:
    return {
        "fund_a": {"us_stock": 0.95, "cash": 0.05},
        "fund_b": {"international_stock": 0.9, "fixed_income": 0.1},
        "fund_c": {"other": 0.05, "us_stock": 0.70, "fixed_income": 0.25},
        "fund_e": {"not_classified": 0.1, "fixed_income": 0.5, "cash": 0.4},
        "fund_f": {"us_stock": 0.85, "international_stock": 0.15},
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
def expected_table_fund_asset_allocation() -> Dict[str, float]:
    return {
        "us_stock": 831.8040000000001,
        "cash": 72.8,
        "international_stock": 2281.1400000000003,
        "fixed_income": 351.15000000000003,
        "other": 5.026000000000001,
        "not_classified": 17.2,
    }


@pytest.fixture(scope="function")
def blend_fund_table_one() -> pd.DataFrame:
    return pd.DataFrame(
        {"balance": ["100", "3000.25", "125.65"], "change_in_value": [-10, 5, 0]},
        index=["fund_a", "fund_b", "fund_c"],
    )


@pytest.fixture(scope="function")
def blend_fund_table_one_output() -> pd.Series:
    return pd.Series(
        ["100", "3000.25", "125.65"],
        name="balance",
        index=["fund_a", "fund_b", "fund_c"],
    )


@pytest.fixture(scope="function")
def blend_fund_table_two() -> pd.DataFrame:
    return pd.DataFrame(
        {
            0: ["random", "fund_e yes", "fund_f no", "waste"],
            1: [-1, "215.0", "1008.0", "0"],
        },
        index=[0, 1, 2, 3],
    )


@pytest.fixture(scope="function")
def blend_fund_table_two_output() -> pd.Series:
    output = pd.Series(["215.0", "1008.0"], name=1, index=["fund_e", "fund_f"])
    output.index.name = 0
    return output
