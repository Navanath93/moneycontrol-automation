from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import BASE_URL


class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ===== Push Notification =====
    PUSH_NO_THANKS_BTN = (
        By.XPATH,
        "//button[normalize-space()='No thanks']"
    )

    # ===== Header Login =====
    HELLO_LOGIN_BTN = (
        By.XPATH,
        "//span[contains(text(),'Hello')]"
    )

    LOGIN_DROPDOWN = (
        By.XPATH,
        "//div[contains(@class,'login')]"
    )

    LOGIN_OPTION = (
        By.XPATH,
        "//a[normalize-space()='Log-in']"
    )

    SIGNUP_OPTION = (
        By.XPATH,
        "//a[normalize-space()='Sign-Up']"
    )

    MY_ACCOUNT_SECTION = (
        By.XPATH,
        "//div[contains(text(),'My Account')]"
    )

    FOLLOW_US_SECTION = (
        By.XPATH,
        "//div[contains(text(),'Follow us')]"
    )
    SEARCH_INPUT = (
        By.ID, "search_str"
    )

    SEARCH_BUTTON = (
        By.ID, "search_btn"
    )

    # ===== Actions =====
    def search_stock(self, stock_name):
        self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        ).clear()
        self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        ).send_keys(stock_name)

        self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        ).click()

    def open_home_page(self):
        self.driver.get(BASE_URL)
        self.handle_push_notification()

    def handle_push_notification(self):
        try:
            self.wait.until(
                EC.element_to_be_clickable(self.PUSH_NO_THANKS_BTN)
            ).click()
        except:
            pass  # popup may not appear every time

    def click_hello_login(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.HELLO_LOGIN_BTN)
        )
        self.driver.execute_script("arguments[0].click();", element)

    def is_login_dropdown_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.LOGIN_DROPDOWN)
        ).is_displayed()

    def validate_login_dropdown_options(self):
        assert self.wait.until(
            EC.visibility_of_element_located(self.LOGIN_OPTION)
        )
        assert self.wait.until(
            EC.visibility_of_element_located(self.SIGNUP_OPTION)
        )
        assert self.wait.until(
            EC.visibility_of_element_located(self.MY_ACCOUNT_SECTION)
        )
        assert self.wait.until(
            EC.visibility_of_element_located(self.FOLLOW_US_SECTION)
        )

    def click_login_option(self):
        self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_OPTION)
        ).click()
