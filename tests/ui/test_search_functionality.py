import pytest
import os
from pages.home_page import HomePage
from utils.csv_reader import read_csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "stocks.csv")


@pytest.mark.ui
def test_search_stock_by_name(driver):
    home = HomePage(driver)
    home.open_home_page()

    stock_name = "Reliance"
    home.search_stock(stock_name)

    assert stock_name.lower() in driver.current_url.lower()


@pytest.mark.ui
def test_search_stocks_from_csv(driver):
    test_data = read_csv(CSV_PATH)

    if not test_data:
        pytest.skip("No stock data available in CSV")

    home = HomePage(driver)
    home.open_home_page()

    for row in test_data:
        stock = row.get("stock")
        if not stock:
            continue

        home.search_stock(stock)
        assert stock.lower() in driver.current_url.lower()
