from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import BASE_URL


class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ===== Push Notification =====
    PUSH_NO_THANKS_BTN = (
        By.XPATH, "//button[normalize-space()='No thanks']"
    )

    # ===== Search =====
    SEARCH_INPUT = (By.ID, "search_str")

    # Autosuggest container
    SEARCH_SUGGESTION_CONTAINER = (
        By.ID, "autosugg_mc1"
    )

    # Left panel - Quotes tab
    QUOTES_TAB = (
        By.XPATH, "//ul[@id='ul_srchCat_DDL']//li[@id='tab1']"
    )

    # Right panel - Quotes result list
    QUOTES_RESULT_ITEMS = (
        By.XPATH, "//ul[contains(@class,'srch_lst')]//li"
    )

    # Left panel all options
    LEFT_PANEL_OPTIONS = (
        By.XPATH, "//ul[@id='ul_srchCat_DDL']//li"
    )

    # ===== Actions =====
    def open_home_page(self):
        self.driver.get(BASE_URL)
        self.handle_push_notification()

    def handle_push_notification(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.PUSH_NO_THANKS_BTN)
            ).click()
        except TimeoutException:
            pass

    def search_stock(self, stock_name):
        # Step 1: Type stock name
        search_box = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_box.clear()
        search_box.send_keys(stock_name)

        # Step 2: Wait for autosuggest container to be visible
        self.wait.until(
            EC.visibility_of_element_located(
                self.SEARCH_SUGGESTION_CONTAINER
            )
        )

        # Step 3: Click Quotes tab
        quotes_tab = self.wait.until(
            EC.presence_of_element_located(self.QUOTES_TAB)
        )
        self.driver.execute_script("arguments[0].click();", quotes_tab)

        # Step 4: Click first visible Quotes result
        results = self.wait.until(
            EC.presence_of_all_elements_located(
                self.QUOTES_RESULT_ITEMS
            )
        )

        for item in results:
            if item.is_displayed():
                item.click()
                return

        raise AssertionError(
            f"No Quotes results found for stock: {stock_name}"
        )

    def are_left_panel_options_clickable(self):
        options = self.wait.until(
            EC.presence_of_all_elements_located(
                self.LEFT_PANEL_OPTIONS
            )
        )

        for option in options:
            if not option.is_displayed() or not option.is_enabled():
                return False

        return True
