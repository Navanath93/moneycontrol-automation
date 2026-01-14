import pytest
from pages.home_page import HomePage
from utils.csv_reader import read_csv


@pytest.mark.ui
def test_search_stock_by_name(driver):
    home = HomePage(driver)
    home.open_home_page()

    stock_name = "Reliance"
    home.search_stock(stock_name)

    # Strong assertion
    assert stock_name.lower() in driver.title.lower()


@pytest.mark.ui
def test_search_stocks_from_csv(driver):
    test_data = read_csv("data/stocks.csv")

    if not test_data:
        pytest.skip("No stock data available in CSV")

    home = HomePage(driver)
    home.open_home_page()

    for row in test_data:
        stock = row.get("stock")

        if not stock:
            continue

        home.search_stock(stock)

        assert stock.lower() in driver.title.lower()
