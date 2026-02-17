from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class WatchlistPage(BasePage):

    WATCHLIST_MENU = (
        By.XPATH,
        "//a[contains(@href,'watchlist')]"
    )

    STOCK_SYMBOLS = (
        By.CSS_SELECTOR,
        "table.tblwatchlist tbody tr td.txt12 a"
    )

    ADD_STOCK_INPUT = (
        By.ID,
        "ctatxtbox"
    )

    AUTOCOMPLETE_LIST = (
        By.ID,
        "suggest"
    )

    FIRST_SUGGESTION = (
        By.CSS_SELECTOR,
        "#suggest li:first-child"
    )

    def __init__(self, driver):
        super().__init__(driver)

    def open_watchlist(self):
        self.driver.get("https://www.moneycontrol.com/watchlist/stocks")
        # Handle potential login redirect or popups automatically
        self.popup_handler.handle_potential_popups()
    
    def get_watchlist_count(self):
        """Returns the number of unique stocks in the watchlist"""
        try:
            elements = self.get_elements(self.STOCK_SYMBOLS)
            stocks = [el.text.strip() for el in elements if el.text.strip()]
            return len(set(stocks))
        except Exception:
            return 0

    def add_stock_from_search(self, symbol):
        """Adds a stock by searching in the watchlist search box"""
        current_count = self.get_watchlist_count()
        self.click(self.ADD_STOCK_INPUT)
        self.send_keys(self.ADD_STOCK_INPUT, symbol)
        
        # Wait for autocomplete
        self.wait.until(
            EC.visibility_of_element_located(self.AUTOCOMPLETE_LIST)
        )
        
        # Click first result
        self.click(self.FIRST_SUGGESTION)
        
        # Wait for either the count to increase or a specific time-out (dynamic wait)
        # In real-time UI, we wait for the table to refresh
        try:
            self.wait.until(lambda d: self.get_watchlist_count() > current_count)
        except TimeoutException:
            print(f"Count didn't increase for {symbol}. It might already be in the list.")

    # Added missing method used in test_watchlist_flow
    def count_stocks(self):
        return self.get_watchlist_count()

    def add_stock(self, symbol):
        self.add_stock_from_search(symbol)
