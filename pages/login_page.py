from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ===== Login Modal =====
    LOGIN_MODAL = (
        By.XPATH,
        "//div[contains(@class,'modal') and .//h2[text()='Login']]"
    )

    LOGIN_WITH_OTP_TAB = (
        By.XPATH,
        "//button[normalize-space()='Login with OTP']"
    )

    LOGIN_WITH_PASSWORD_TAB = (
        By.XPATH,
        "//button[normalize-space()='Login with Password']"
    )

    USERNAME_INPUT = (
        By.XPATH,
        "//input[contains(@placeholder,'Email')]"
    )

    PASSWORD_INPUT = (
        By.XPATH,
        "//input[@type='password']"
    )

    LOGIN_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Login']"
    )

    # ===== Actions =====

    def is_login_modal_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.LOGIN_MODAL)
        ).is_displayed()

    def switch_to_password_login(self):
        self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_WITH_PASSWORD_TAB)
        ).click()

    def login_with_password(self, username, password):
        self.switch_to_password_login()
        self.wait.until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        ).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
