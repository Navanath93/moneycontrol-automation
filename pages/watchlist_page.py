from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WatchlistPage:

    WATCHLIST_MENU = (
        By.XPATH,
        "//a[contains(@href,'watchlist')]"
    )

    STOCK_ROWS = (
        By.CSS_SELECTOR,
        "table tbody tr"
    )

    SEARCH_BOX = (
        By.XPATH,
        "//input[contains(@placeholder,'Search')]"
    )

    ADD_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Add')]"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open_watchlist(self):
        self.driver.get(
            "https://www.moneycontrol.com/watchlist/stocks"
        )

    def count_stocks(self):
        rows = self.wait.until(
            EC.presence_of_all_elements_located(self.STOCK_ROWS)
        )
        return len(rows)

    def add_stock(self, stock_name):
        search = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_BOX)
        )
        search.clear()
        search.send_keys(stock_name)

        self.wait.until(
            EC.element_to_be_clickable(self.ADD_BUTTON)
        ).click()
