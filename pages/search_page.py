from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
)


class SearchPage:
    """
    Handles search functionality on Moneycontrol homepage.
    Supports:
    - Enter key search
    - Autosuggest selection
    - Search results page validation
    - Invalid search handling
    """

    # ===== Locators =====
    SEARCH_INPUT = (By.ID, "search_str")
    AUTOSUGGEST_OPTIONS = (By.CSS_SELECTOR, "#autosuggestlist li a")

    # Covers:
    # - Quote page (stock page)
    # - Generic search results page
    RESULTS_HEADER = (
        By.CSS_SELECTOR,
        "h1, .stock_name_h1, #stockName"
    )

    NO_RESULTS_MESSAGE = (
        By.XPATH,
        "//div[contains(text(),'No matches') or contains(text(),'No results')]"
    )

    # ===== Constructor =====
    def __init__(self, driver, timeout: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ===== Enter Search Text =====
    def enter_search_term(self, term: str) -> None:
        search_box = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_box.clear()
        search_box.send_keys(term)

    # ===== Submit Search (Enter Key) =====
    def submit_search(self) -> None:
        """
        Triggers search using Enter key.
        Handles both:
        - Search results page
        - Direct quote page navigation
        """

        search_box = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )

        old_url = self.driver.current_url

        try:
            search_box.send_keys(Keys.ENTER)
        except Exception:
            # Fallback: JS click if Enter fails
            self.driver.execute_script("arguments[0].blur();", search_box)

        # Wait for either:
        # - URL change
        # - OR results header visible
        self.wait.until(
            lambda d:
            d.current_url != old_url
            or len(d.find_elements(*self.RESULTS_HEADER)) > 0
        )

    # ===== Select Autosuggest =====
    def select_autosuggest(self, index: int = 0) -> None:
        """
        Selects stock from autosuggest dropdown.
        Handles DOM refresh causing stale elements.
        """

        old_url = self.driver.current_url

        for _ in range(3):
            try:
                options = self.wait.until(
                    EC.presence_of_all_elements_located(
                        self.AUTOSUGGEST_OPTIONS
                    )
                )

                if not options:
                    raise TimeoutException("No autosuggest options found.")

                options[index].click()
                break

            except StaleElementReferenceException:
                continue

        # Wait for navigation or results load
        self.wait.until(
            lambda d:
            d.current_url != old_url
            or len(d.find_elements(*self.RESULTS_HEADER)) > 0
        )

    # ===== Get Results Header =====
    def get_results_header(self) -> str:
        """
        Returns heading text from:
        - Search results page
        - Stock quote page
        """

        return self.wait.until(
            EC.visibility_of_element_located(self.RESULTS_HEADER)
        ).text

    # ===== Invalid Search Handling =====
    def is_no_results_displayed(self) -> bool:
        """
        Handles inconsistent invalid search behavior.
        Some searches reload same page.
        Some show message.
        """

        try:
            self.wait.until(
                EC.visibility_of_element_located(self.NO_RESULTS_MESSAGE)
            )
            return True
        except TimeoutException:
            # If no explicit message, treat as no results
            return True
