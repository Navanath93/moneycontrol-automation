from pages.home_page import HomePage
from utils.csv_reader import read_csv

def test_search_stocks_from_csv(driver):
    home = HomePage(driver)
    home.open_home_page()

    test_data = read_csv("data/stocks.csv")

    for row in test_data:
        home.search_stock(row["stock"])
        assert row["stock"] in driver.page_source
