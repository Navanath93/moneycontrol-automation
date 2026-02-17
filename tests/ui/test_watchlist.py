import pytest
import csv
import os
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.watchlist_page import WatchlistPage
from utils.csv_reader import read_csv
from config.config import USERNAME, PASSWORD

CSV_PATH = "data/stocks.csv"


@pytest.mark.ui
def test_watchlist_flow(driver):

    # Step 1: Open homepage
    home = HomePage(driver)
    home.open_home_page()

    # Step 2: Open login
    home.open_login_ui()

    # Step 3: Login with credentials from config
    login = LoginPage(driver)
    login.login_with_password(USERNAME, PASSWORD)

    # Step 4: Open watchlist page
    watchlist = WatchlistPage(driver)
    watchlist.open_watchlist()

    # Step 5: Count existing stocks
    initial_count = watchlist.count_stocks()

    # Step 6: Read stocks from CSV
    stocks = read_csv(CSV_PATH)

    # Step 7: Add first 3 stocks
    for row in stocks[:3]:
        watchlist.add_stock(row["stock"])

    # Step 8: Validate new count
    final_count = watchlist.count_stocks()

    assert final_count >= initial_count + 3


@pytest.mark.ui
class TestWatchlistAssignment:

    def test_watchlist_workflow(self, driver):
        # Step 1: Login
        home = HomePage(driver)
        home.open_home_page()
        home.open_login_ui()

        login = LoginPage(driver)
        login.login_with_password(USERNAME, PASSWORD)

        # Step 2: Navigate to Watchlist
        watchlist = WatchlistPage(driver)
        watchlist.open_watchlist()

        # Step 3: Count initial stocks
        initial_count = watchlist.get_watchlist_count()
        print(f"Initial stocks in watchlist: {initial_count}")

        # Step 4: Add stocks from CSV
        csv_path = os.path.join(os.getcwd(), "data", "stocks.csv")
        stocks_to_add = []
        with open(csv_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stocks_to_add.append(row['symbol'])

        for symbol in stocks_to_add:
            print(f"Adding stock: {symbol}")
            watchlist.add_stock_from_search(symbol)

        # Step 5: Verify updated count and content
        final_count = watchlist.get_watchlist_count()
        print(f"Final stocks in watchlist: {final_count}")

        # Core Assertion: Verify the recently added stocks are actually in the UI
        # We check the page source or elements for the specific symbols
        page_source = driver.page_source.upper()
        for symbol in stocks_to_add:
            assert symbol.upper() in page_source, f"Symbol {symbol} not found in watchlist after adding."
        
        # Verify count increased logically
        assert final_count >= initial_count, f"Watchlist count should not decrease. Initial: {initial_count}, Final: {final_count}"
