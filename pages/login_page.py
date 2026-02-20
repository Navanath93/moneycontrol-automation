import logging
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """
    LoginPage handles the authentication flow with specific support for
    Moneycontrol's multi-step iframe-based login.
    """

    # --- Fallback Locators ---
    USERNAME_SELECTORS = [
        (By.ID, "email"),
        (By.ID, "mobile"),
        (By.NAME, "email"),
        (By.ID, "user_id"),
        (By.CSS_SELECTOR, "form input[type='text']"),
        (By.XPATH, "//form//input[@placeholder='Email' or @placeholder='Mobile']")
    ]

    PASSWORD_SELECTORS = [
        (By.ID, "pwd"),
        (By.ID, "password"),
        (By.NAME, "password"),
        (By.CSS_SELECTOR, "form input[type='password']"),
        (By.XPATH, "//form//input[@placeholder='Password']")
    ]

    LOGIN_BUTTON_SELECTORS = [
        (By.ID, "login_btn"),
        (By.CSS_SELECTOR, "button.btnLogin"),
        (By.CSS_SELECTOR, "form button[type='submit']"),
        (By.XPATH, "//form//button[contains(text(),'Login')]")
    ]

    PROCEED_BTN = (By.ID, "proceed_btn")
    PASSWORD_TAB = (By.XPATH, "//li[contains(text(),'Password')] | //a[contains(text(),'Password')] | //div[text()='Password']")

    def __init__(self, driver, timeout=15):
        super().__init__(driver, timeout=timeout)

    def _switch_to_login_context(self):
        """Recursively scans iframes to find the login form."""
        self.driver.switch_to.default_content()
        indicators = self.USERNAME_SELECTORS + self.PASSWORD_SELECTORS + [self.PASSWORD_TAB]

        def scan(depth=0):
            if depth > 2:
                return False
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for frame in iframes:
                try:
                    src = (frame.get_attribute("src") or "").lower()
                    if "ads" in src or "google" in src:
                        continue
                    self.driver.switch_to.frame(frame)
                    for loc in indicators:
                        if self.driver.find_elements(*loc):
                            logger.info(f"Switched to login context: {src[:50]}")
                            return True
                    if scan(depth + 1):
                        return True
                    self.driver.switch_to.parent_frame()
                except Exception:
                    continue
            return False

        return scan()

    def _resolve_locator(self, locators, timeout=10):
        """Try multiple locators until one resolves."""
        for locator in locators:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                logger.info(f"Resolved locator: {locator}")
                return element
            except TimeoutException:
                logger.debug(f"Locator failed: {locator}")
                continue
        raise TimeoutException(f"No valid locator found from {locators}")

    def login_with_password(self, username, password):
        # Handle popups before login
        try:
            self.popup_handler.handle_potential_popups()
        except Exception:
            logger.debug("No popup handler or no popups detected.")

        # Ensure we are in the correct iframe context
        if not self._switch_to_login_context():
            WebDriverWait(self.driver, 10).until(lambda d: self._switch_to_login_context())

        # Select Password tab if needed
        try:
            tab = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_TAB))
            self.driver.execute_script("arguments[0].click();", tab)
            # Re-scan iframe context after tab switch
            self._switch_to_login_context()
        except Exception:
            logger.debug("Password tab selection failed or already active.")

        # Enter username
        username_field = self._resolve_locator(self.USERNAME_SELECTORS, timeout=15)
        username_field.clear()
        username_field.send_keys(username)

        # Proceed button if present
        try:
            proceed = self.driver.find_element(*self.PROCEED_BTN)
            if proceed.is_displayed():
                self.driver.execute_script("arguments[0].click();", proceed)
                self.wait.until(EC.visibility_of_any_elements_located(self.PASSWORD_SELECTORS))
        except Exception:
            pass

        # Enter password
        password_field = self._resolve_locator(self.PASSWORD_SELECTORS, timeout=15)
        password_field.clear()
        password_field.send_keys(password)

        # Submit
        login_button = self._resolve_locator(self.LOGIN_BUTTON_SELECTORS, timeout=15)
        self.driver.execute_script("arguments[0].click();", login_button)

        self.driver.switch_to.default_content()
        logger.info("Login flow completed.")
