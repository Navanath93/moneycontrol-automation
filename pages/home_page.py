from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import BASE_URL


class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # Push notification
    PUSH_NO_THANKS_BTN = (
        By.XPATH, "//button[normalize-space()='No thanks']"
    )

    # Search
    SEARCH_INPUT = (By.ID, "search_str")

    # Autosuggest anchor links (this is the key fix)
    SEARCH_RESULT_LINKS = (
        By.XPATH,
        "//ul[contains(@class,'srch_lst')]//li//a"
    )

    # Left panel categories
    LEFT_PANEL_OPTIONS = (
        By.XPATH,
        "//ul[@id='ul_srchCat_DDL']//li"
    )

    # ---------------- Actions ----------------

    def open_home_page(self):
        try:
            self.driver.get(BASE_URL)
        except TimeoutException:
            pass

        self.handle_push_notification()

    def handle_push_notification(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.PUSH_NO_THANKS_BTN)
            ).click()
        except TimeoutException:
            pass

    def search_stock(self, stock_name):
        # Step 1: type stock name
        search_box = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )
        search_box.click()
        search_box.clear()
        search_box.send_keys(stock_name)

        # Step 2: wait for ANY suggestion link
        results = self.wait.until(
            EC.presence_of_all_elements_located(
                self.SEARCH_RESULT_LINKS
            )
        )

        # Step 3: click first valid visible link
        for link in results:
            text = link.text.strip()
            if text:
                self.driver.execute_script(
                    "arguments[0].click();", link
                )
                return

        raise AssertionError(
            f"No search suggestions found for stock: {stock_name}"
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
