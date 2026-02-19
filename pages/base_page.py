import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.popup_handler import PopupHandler
import os

logger = logging.getLogger(__name__)

class BasePage:
    """
    BasePage contains reusable Selenium actions and integrated diagnostic logic.
    """

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.popup_handler = PopupHandler(driver)

    def click(self, locator):
        try:
            # High-performance wait for clickability
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
        except Exception as e:
            logger.warning(f"Interaction failed for {locator}. Attempting recovery...")
            self.popup_handler.handle_potential_popups()
            
            # Retry mechanism
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].click();", element) # Use JS click for reliability on retry
                logger.info("Recovered and clicked via retry.")
            except Exception:
                raise e

    def send_keys(self, locator, value):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.clear()
            element.send_keys(value)
        except Exception as e:
            logger.warning(f"Input failed for {locator}. Attempting recovery...")
            self.popup_handler.handle_potential_popups()
            self.switch_to_default()  # ensure we’re not stuck in wrong iframe
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.clear()
                element.send_keys(value)
            except Exception:
                self.driver.save_screenshot("reports/screenshots/input_failure.png")
                logger.error(f"Failed to send keys to {locator} after recovery effort.")
                raise e

    def is_visible(self, locator, timeout=None):
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            return wait.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except:
            return False

    def switch_to_default(self):
        self.driver.switch_to.default_content()

    def get_element(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def get_elements(self, locator):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )
