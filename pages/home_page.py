import logging
from pages.base_page import BasePage
from config.config import BASE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from utils.common_utils import handle_alert_if_present

logger = logging.getLogger(__name__)

class HomePage(BasePage):

    PUSH_NO_THANKS_BTN = (
        By.XPATH, "//button[normalize-space()='No thanks']"
    )

    SEARCH_INPUT = (By.ID, "search_str")

    RESULT_LINKS = (
        By.XPATH,
        "//div[@id='autosuggestlist']//ul//li//a"
    )

    SEARCH_SUGGESTIONS = (
        By.CSS_SELECTOR,
        "ul.srch_rslt li, .srch_cat li, div.sugbox li, #autosuggestlist ul li"
    )

    HELLO_LOGIN = (
        By.XPATH,
        "//a[contains(@class,'user_account') or @title='Hello, Login'] | "
        "//div[contains(@class,'login')]//a[contains(text(),'Hello')] | "
        "//span[contains(text(),'Hello, Login')]"
    )

    SIGN_IN_OPTION = (
        By.XPATH,
        "//div[contains(@class,'login')]//a[text()='Log-in'] | "
        "//a[contains(@class,'btnLogin')] | "
        "//div[contains(@class,'user_account')]//a[contains(@href,'login')] | "
        "//button[contains(text(),'Log-in')] | "
        "//a[contains(text(),'Log-in')]"
    )

    SIGN_UP_OPTION = (
        By.XPATH,
        "//a[contains(text(),'Sign Up')]"
    )

    LOGIN_IFRAME = (
        By.XPATH,
        "//iframe[contains(@src,'login') or contains(@id,'login') or contains(@src,'accounts.moneycontrol')]"
    )

    LEFT_PANEL_TABS = (
        By.XPATH,
        "//a[normalize-space()='Quotes' or "
        "normalize-space()='Charts' or "
        "normalize-space()='News' or "
        "normalize-space()='Financials']"
    )

    def __init__(self, driver):
        super().__init__(driver)

    def open_home_page(self):
        self.driver.get(BASE_URL)
        # Wait for a core element to ensure page has started rendering meaningfully
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.SEARCH_INPUT)
            )
        except:
            pass
        self.handle_push_notification()
        self.popup_handler.handle_potential_popups()

    def handle_push_notification(self):
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.PUSH_NO_THANKS_BTN)
            )
            self.driver.execute_script("arguments[0].click();", btn)
        except Exception:
            pass

    # ================= LOGIN =================

    def open_login_ui(self):
        """
        Complete login flow:
        1. Click/Hover 'Hello, Login' button
        2. Wait for dropdown to appear
        3. Click 'Log-in' option from dropdown
        """
        logger.info("Starting Login UI flow...")
        self.popup_handler.handle_potential_popups()
        
        # Step 1: Hover/Click 'Hello, Login'
        try:
            login_btn = self.wait.until(EC.element_to_be_clickable(self.HELLO_LOGIN))
            # Scroll into view just in case
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_btn)
            
            # Use ActionChains for hover, but fallback to click if dropdown doesn't appear
            ActionChains(self.driver).move_to_element(login_btn).perform()
            
            # Check if dropdown visible, if not, click it
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.SIGN_IN_OPTION))
            except:
                logger.debug("Dropdown didn't appear on hover, clicking 'Hello Login'...")
                self.driver.execute_script("arguments[0].click();", login_btn)
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.SIGN_IN_OPTION))
                
        except Exception as e:
            logger.warning(f"Could not trigger login dropdown: {e}. Trying direct click.")
            self.click(self.HELLO_LOGIN)

        # Step 2: Click 'Log-in'
        try:
            login_option = self.wait.until(EC.element_to_be_clickable(self.SIGN_IN_OPTION))
            # Try JS click as it's more reliable for elements inside hover-menus
            self.driver.execute_script("arguments[0].click();", login_option)
            logger.info("Clicked 'Log-in' via JS.")
        except Exception:
            # Fallback to standard click
            self.click(self.SIGN_IN_OPTION)
            logger.info("Clicked 'Log-in' via standard click.")

        # Wait for iframe or modal to stabilize and be VISIBLE
        try:
            # Using any_of for multiple possible indicators of a successful login popup load
            WebDriverWait(self.driver, 20).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='login'], iframe[src*='auth'], iframe[src*='iam'], iframe[src*='accounts.moneycontrol']")),
                    EC.visibility_of_element_located((By.XPATH, "//*[(contains(@class,'modal') or contains(@class,'popup')) and .//input]")),
                    EC.visibility_of_element_located((By.ID, "login_form")),
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-form, .auth-form")),
                    EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(),'Login') or contains(text(),'Sign')]"))
                )
            )
            logger.info("Login UI stabilized.")
        except TimeoutException:
            logger.warning("Stabilization criteria not fully met. LoginPage will attempt deeper context scanning.")

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

    # ================= SEARCH =================

    def search_stock(self, stock_name):
        self.handle_push_notification()
        self.popup_handler.handle_potential_popups()

        self.click(self.SEARCH_INPUT)
        self.send_keys(self.SEARCH_INPUT, stock_name)

        handle_alert_if_present(self.driver)

        # Wait for suggestions to appear and be visible
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_any_elements_located(self.RESULT_LINKS)
        )

        results = self.get_elements(self.RESULT_LINKS)

        if not results:
            raise AssertionError(f"No result for {stock_name}")

        # Click the first result using the robust click method if possible, or JS as it's an autosuggest item
        try:
            self.driver.execute_script("arguments[0].click();", results[0])
            print(f"Selected first search result for: {stock_name}")
        except Exception:
            results[0].click()

        WebDriverWait(self.driver, 20).until(
            lambda d: stock_name.lower() in d.current_url.lower()
            or "stock" in d.current_url.lower()
            or "quotes" in d.current_url.lower()
        )

        return True

    def trigger_search_suggestions(self, keyword):
        try:
            self.handle_push_notification()
            self.popup_handler.handle_potential_popups()

            # Using robust BasePage methods
            self.click(self.SEARCH_INPUT)
            self.send_keys(self.SEARCH_INPUT, keyword)

            # handle alert if triggered
            handle_alert_if_present(self.driver)

            # ensure suggestions container present and visible
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_any_elements_located(self.SEARCH_SUGGESTIONS)
            )

            results = self.get_search_suggestions()
            return len(results) > 0

        except Exception as e:
            print(f"Trigger search suggestions failed for '{keyword}': {e}")
            return False

    def get_search_suggestions(self):
        """Returns only VISIBLE search suggestions"""
        try:
            all_suggestions = self.driver.find_elements(*self.SEARCH_SUGGESTIONS)
            # Filter to return only visible elements
            return [item for item in all_suggestions if item.is_displayed()]
        except:
            return []

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

    # ================= LEFT PANEL =================

    def are_left_panel_options_clickable(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.LEFT_PANEL_TABS)
        )

        tabs = self.driver.find_elements(*self.LEFT_PANEL_TABS)

        if not tabs:
            return False

        enabled_tabs = [tab for tab in tabs if tab.is_enabled()]
        return len(enabled_tabs) >= 2
