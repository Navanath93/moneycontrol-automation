from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from config.config import BASE_URL
from selenium.webdriver.common.action_chains import ActionChains


class HomePage(BasePage):

    # ===== Push Notification =====
    PUSH_NO_THANKS_BTN = (
        By.XPATH, "//button[normalize-space()='No thanks']"
    )

    # ===== Search =====
    SEARCH_INPUT = (By.ID, "search_str")
    QUOTES_TAB = (By.ID, "tab1")
    AUTOSUGGEST_CONTAINER = (By.ID, "autosuggestlist")

    RESULT_LINKS = (
        By.XPATH,
        "//div[@id='autosuggestlist']//ul//li//a"
    )


    # ===== Login =====
    HELLO_LOGIN = (
        By.XPATH,
        "//a[contains(text(),'Login') or contains(text(),'Hello')]"
    )

    # ===== Login =====
    HELLO_LOGIN_BTN = (
        By.XPATH,
        "//a[contains(normalize-space(), 'Login')]"
    )

    LOGIN_MENU_ITEM = (
        By.XPATH,
        "//a[contains(text(),'Login') or contains(text(),'Sign In')]"
    )
    # ===== Login Trigger (stable) =====
    LOGIN_TRIGGER = (
        By.XPATH,
        "//*[normalize-space()='Hello, Login' or normalize-space()='Login']"
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

    LOGIN_OPTION = (
        By.XPATH, "//a[normalize-space()='Login']"
    )

    # ===== Left Panel =====
    LEFT_PANEL_TABS = (
        By.XPATH,
        "//a[normalize-space()='Quotes' or "
        "normalize-space()='Charts' or "
        "normalize-space()='News' or "
        "normalize-space()='Financials']"
    )
    LOGIN_IFRAME = (
        By.XPATH,
        "//iframe[contains(@src,'login') or contains(@id,'login')]"
    )

    USERNAME_INPUT = (
        By.XPATH,
        "//input[@type='email' or @name='email']"
    )

    def __init__(self, driver):
        super().__init__(driver)

    # ===== Common actions =====
    def open_home_page(self):
        self.driver.get(BASE_URL)
        self.handle_push_notification()

    def open_login(self):
        wait = WebDriverWait(self.driver, 20)

        login_btn = wait.until(
            EC.element_to_be_clickable(self.HELLO_LOGIN)
        )

        self.driver.execute_script(
            "arguments[0].click();", login_btn
        )

    def handle_push_notification(self):
        try:
            btn = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(self.PUSH_NO_THANKS_BTN)
            )
            self.driver.execute_script(
                "arguments[0].click();", btn
            )
        except Exception:
            # popup not present – safe to ignore
            pass

    # ===== Login actions =====
    def click_hello_login(self):
        # wait for page shell
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # wait for login link in header
        btn = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.HELLO_LOGIN_BTN)
        )

        # JS click avoids hover / overlay issues
        self.driver.execute_script("arguments[0].click();", btn)

    def is_login_dropdown_displayed(self):
        return self.is_visible(self.LOGIN_DROPDOWN)

    def validate_login_dropdown_options(self):
        options = self.get_elements(
            (By.XPATH, "//div[contains(@class,'login_drop')]//a")
        )
        assert options, "Login dropdown options not found"

    def click_login_option(self):
        self.click(self.LOGIN_OPTION)

    def open_login_modal(self):
        wait = WebDriverWait(self.driver, 20)

        login_link = wait.until(
            EC.presence_of_element_located(self.HELLO_LOGIN)
        )

        self.driver.execute_script(
            "arguments[0].click();", login_link
        )

    # ===== Search actions =====
    def search_stock(self, stock_name):
        self.send_keys(self.SEARCH_INPUT, stock_name)

        wait = WebDriverWait(self.driver, 20)

        # Quotes tab may already be active, so guard click
        try:
            quotes_tab = wait.until(
                EC.element_to_be_clickable(self.QUOTES_TAB)
            )
            self.driver.execute_script(
                "arguments[0].click();", quotes_tab
            )
        except Exception:
            pass  # already active

        # Wait for at least one visible result
        results = wait.until(
            EC.visibility_of_any_elements_located(self.RESULT_LINKS)
        )

        for link in results:
            if link.is_displayed():
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", link
                )
                self.driver.execute_script(
                    "arguments[0].click();", link
                )
                return

        raise AssertionError(
            f"No clickable Quotes result found for stock: {stock_name}"
        )

    # ===== Left panel validation =====
    def are_left_panel_options_clickable(self):
        tabs = self.get_elements(self.LEFT_PANEL_TABS)

        assert tabs, "Left panel tabs not found"

        enabled_tabs = [tab for tab in tabs if tab.is_enabled()]

        assert len(enabled_tabs) >= 2, (
            "Less than expected enabled left panel tabs"
        )

        return True

    def open_login_dropdown(self):
        wait = WebDriverWait(self.driver, 20)
        actions = ActionChains(self.driver)

        login_container = wait.until(
            EC.presence_of_element_located(self.HELLO_LOGIN)
        )

        actions.move_to_element(login_container).perform()

    def is_login_options_visible(self):
        wait = WebDriverWait(self.driver, 10)

        sign_in = wait.until(
            EC.visibility_of_element_located(self.SIGN_IN_OPTION)
        )

        sign_up = wait.until(
            EC.visibility_of_element_located(self.SIGN_UP_OPTION)
        )

        return sign_in.is_displayed() and sign_up.is_displayed()

    def are_login_options_visible(self):
        wait = WebDriverWait(self.driver, 10)

        sign_in = wait.until(
            EC.visibility_of_element_located(self.SIGN_IN_OPTION)
        )

        sign_up = wait.until(
            EC.visibility_of_element_located(self.SIGN_UP_OPTION)
        )

        return sign_in.is_displayed() and sign_up.is_displayed()

