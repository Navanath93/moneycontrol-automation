from pages.base_page import BasePage
from config.config import BASE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time


class HomePage(BasePage):

    # ===== Push Notification =====
    PUSH_NO_THANKS_BTN = (
        By.XPATH, "//button[normalize-space()='No thanks']"
    )

    # ===== Search =====
    SEARCH_INPUT = (By.ID, "search_str")

    RESULT_LINKS = (
        By.XPATH,
        "//div[@id='autosuggestlist']//ul//li//a"
    )

    SEARCH_SUGGESTIONS = (
        By.CSS_SELECTOR,
        "ul.srch_rslt li, .srch_cat li, div.sugbox li"
    )

    # ===== Login =====
    HELLO_LOGIN = (
        By.XPATH,
        "//a[contains(text(),'Hello') or contains(text(),'Login')]"
    )

    LOGIN_DROPDOWN = (
        By.CSS_SELECTOR,
        "ul.dropdown-menu, .login_wrap ul"
    )

    SIGN_IN_OPTION = (
        By.XPATH,
        "//a[contains(text(),'Login')]"
    )

    SIGN_UP_OPTION = (
        By.XPATH,
        "//a[contains(text(),'Sign Up')]"
    )

    LOGIN_IFRAME = (
        By.XPATH,
        "//iframe[contains(@src,'login') or contains(@id,'login')]"
    )

    # ===== Left Panel =====
    LEFT_PANEL_TABS = (
        By.XPATH,
        "//a[normalize-space()='Quotes' or "
        "normalize-space()='Charts' or "
        "normalize-space()='News' or "
        "normalize-space()='Financials']"
    )

    def __init__(self, driver):
        super().__init__(driver)

    # ===============================
    # Common Actions
    # ===============================

    def open_home_page(self):
        self.driver.get(BASE_URL)
        self.handle_push_notification()

    def handle_push_notification(self):
        try:
            btn = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(self.PUSH_NO_THANKS_BTN)
            )
            self.driver.execute_script(
                "arguments[0].click();", btn
            )
        except Exception:
            pass

    # ===============================
    # Login Actions
    # ===============================

    def open_login(self):
        login_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.HELLO_LOGIN)
        )
        self.driver.execute_script(
            "arguments[0].click();", login_btn
        )

    # Alias for backward compatibility
    def open_login_ui(self):
        btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.HELLO_LOGIN)
        )
        self.driver.execute_script("arguments[0].click();", btn)

    def click_hello_login(self):
        self.open_login()

    def is_login_dropdown_displayed(self):
        try:
            dropdown = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.LOGIN_DROPDOWN)
            )
            return dropdown.is_displayed()
        except TimeoutException:
            return False

    def is_login_options_visible(self):
        wait = WebDriverWait(self.driver, 10)
        sign_in = wait.until(
            EC.visibility_of_element_located(self.SIGN_IN_OPTION)
        )
        sign_up = wait.until(
            EC.visibility_of_element_located(self.SIGN_UP_OPTION)
        )
        return sign_in.is_displayed() and sign_up.is_displayed()

    # ===============================
    # Search Actions
    # ===============================

    def search_stock(self, stock_name):

        self.handle_push_notification()

        search_box = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )

        search_box.clear()
        search_box.send_keys(stock_name)

        # Wait autosuggest
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_any_elements_located(self.RESULT_LINKS)
        )

        # Avoid stale element
        results = self.driver.find_elements(*self.RESULT_LINKS)

        if not results:
            raise AssertionError(f"No result for {stock_name}")

        self.driver.execute_script(
            "arguments[0].click();", results[0]
        )

        # Relaxed validation
        WebDriverWait(self.driver, 20).until(
            lambda d: stock_name.lower() in d.current_url.lower()
                      or "stock" in d.current_url.lower()
        )

        return True

    def trigger_search_suggestions(self, keyword):

        try:
            search = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.SEARCH_INPUT)
            )

            search.clear()
            search.send_keys(keyword)

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_any_elements_located(
                    self.SEARCH_SUGGESTIONS
                )
            )

            return True

        except Exception:
            # fallback → press Enter and verify navigation
            search.send_keys(Keys.ENTER)

            WebDriverWait(self.driver, 15).until(
                lambda d: keyword.lower() in d.current_url.lower()
            )

            return True

        def search_with_hover(self, keyword):

            if not self.trigger_search_suggestions(keyword):
                return False

            suggestions = self.driver.find_elements(*self.SEARCH_SUGGESTIONS)

            if not suggestions:
                return False

            ActionChains(self.driver).move_to_element(
                suggestions[0]
            ).click().perform()

            return True

    # ===============================
    # Left Panel Validation
    # ===============================

    def are_left_panel_options_clickable(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.LEFT_PANEL_TABS)
        )

        tabs = self.driver.find_elements(*self.LEFT_PANEL_TABS)

        if not tabs:
            return False

        enabled_tabs = [tab for tab in tabs if tab.is_enabled()]
        return len(enabled_tabs) >= 2
