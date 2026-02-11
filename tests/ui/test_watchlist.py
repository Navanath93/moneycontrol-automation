import pytest
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
