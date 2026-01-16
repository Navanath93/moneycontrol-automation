from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import BASE_URL
import time


class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # Search input
    SEARCH_INPUT = (By.ID, "search_str")

    # Quotes tab
    QUOTES_TAB = (By.ID, "tab1")

    # Autosuggest container (this is the KEY)
    AUTOSUGGEST_CONTAINER = (By.ID, "autosuggestlist")

    # All result links under autosuggest
    RESULT_LINKS = (
        By.XPATH,
        "//div[@id='autosuggestlist']//ul//li//a"
    )
    # Left panel container
    LEFT_PANEL = (By.ID, "mc_mainWrapper")

    # Left panel tabs (Quotes, Charts, News, etc.)
    LEFT_PANEL_TABS = (
        By.XPATH,
        "//ul[contains(@class,'tabs_list')]//li/a"
    )

    def open_home_page(self):
        try:
            self.driver.get(BASE_URL)
        except TimeoutException:
            pass

    def search_stock(self, stock_name):
        # Step 1: Type stock name
        search_box = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )
        search_box.click()
        search_box.clear()
        search_box.send_keys(stock_name)

        # Step 2: Ensure Quotes tab is active
        quotes_tab = self.wait.until(
            EC.presence_of_element_located(self.QUOTES_TAB)
        )

        self.driver.execute_script("""
            if (!arguments[0].classList.contains('active')) {
                arguments[0].click();
            }
        """, quotes_tab)

        # Step 3: Poll until a visible result is clickable
        end_time = time.time() + 15

        while time.time() < end_time:
            try:
                links = self.driver.find_elements(*self.RESULT_LINKS)

                for link in links:
                    if link.is_displayed():
                        text = link.get_attribute("textContent").strip()
                        if text:
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView(true);", link
                            )
                            self.driver.execute_script(
                                "arguments[0].click();", link
                            )
                            return
            except Exception:
                # DOM refreshed, retry
                pass

            time.sleep(0.3)

        raise AssertionError(
            f"No clickable Quotes result found for stock: {stock_name}"
        )

    def are_left_panel_options_clickable(self):
        # Step 1: Ensure result page loaded
        self.wait.until(
            EC.presence_of_element_located(self.LEFT_PANEL)
        )

        # Step 2: Fetch tabs safely
        tabs = self.wait.until(
            EC.presence_of_all_elements_located(self.LEFT_PANEL_TABS)
        )

        assert tabs, "No left panel options found"

        # Step 3: Validate each tab
        for tab in tabs:
            assert tab.is_displayed(), "Left panel option not visible"
            assert tab.is_enabled(), "Left panel option not enabled"

        return True

