from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class LoginPage:
    """
    Page Object for Login Modal only
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ===== Login Modal Locators =====
    LOGIN_MODAL = (
        By.XPATH,
        "//div[contains(@class,'modal') and .//h2[text()='Login']]"
    )

    LOGIN_WITH_PASSWORD_TAB = (
        By.XPATH,
        "//button[normalize-space()='Login with Password']"
    )

    USERNAME_INPUT = (
        By.XPATH,
        "//input[contains(@placeholder,'Email') or contains(@placeholder,'Mobile')]"
    )

    PASSWORD_INPUT = (
        By.XPATH,
        "//input[@type='password']"
    )

    LOGIN_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Login']"
    )

    LOGIN_IFRAME = (
        By.XPATH,
        "//iframe[contains(@src,'login')]"
    )
    # ===== Actions =====
    def is_login_modal_displayed(self):
        try:
            # Case 1: input exists in main DOM
            self.wait.until(
                EC.visibility_of_element_located(self.USERNAME_INPUT)
            )
            return True

        except TimeoutException:
            pass

        # Case 2: input inside iframe (fallback)
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

        for iframe in iframes:
            try:
                self.driver.switch_to.frame(iframe)
                self.wait.until(
                    EC.visibility_of_element_located(self.USERNAME_INPUT)
                )
                return True
            except TimeoutException:
                self.driver.switch_to.default_content()

        return False

    def switch_to_password_login(self):
        self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_WITH_PASSWORD_TAB)
        ).click()

    def login_with_password(self, username, password):
        """
        Password handling untouched, as requested
        """
        self.switch_to_password_login()

        self.wait.until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        ).send_keys(username)

        self.driver.find_element(
            *self.PASSWORD_INPUT
        ).send_keys(password)

        self.driver.find_element(
            *self.LOGIN_BUTTON
        ).click()
