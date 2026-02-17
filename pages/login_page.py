import logging
import time
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """
    LoginPage handles the authentication flow with specific support for 
    Moneycontrol's multi-step iframe-based login.
    """

    # --- Locators ---
    USERNAME_INPUT = (By.CSS_SELECTOR, "input#email, input#mobile, input[name='email'], input#user_id")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#pwd, input#password, input[name='password'], input#user_password")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Login'] | //input[@id='login_btn'] | //button[contains(@class,'btnLogin')]")
    PROCEED_BTN = (By.ID, "proceed_btn")
    PASSWORD_TAB = (By.XPATH, "//li[contains(text(),'Password')] | //a[contains(text(),'Password')] | //div[text()='Password']")

    def __init__(self, driver, timeout=15):
        super().__init__(driver, timeout=timeout)

    def _switch_to_login_context(self):
        """Recursively scans iframes to find the login form."""
        self.driver.switch_to.default_content()
        indicators = [self.USERNAME_INPUT, self.PASSWORD_TAB]
        
        def scan(depth=0):
            if depth > 2: return False
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for frame in iframes:
                try:
                    src = (frame.get_attribute("src") or "").lower()
                    if "ads" in src or "google" in src: continue
                    
                    self.driver.switch_to.frame(frame)
                    if any(self.driver.find_elements(*loc) for loc in indicators):
                        logger.info(f"Switched to login context: {src[:50]}")
                        return True
                    if scan(depth + 1): return True
                    self.driver.switch_to.parent_frame()
                except:
                    continue
            return False
        
        return scan()

    def login_with_password(self, username, password):
        """
        Step-by-step login automation as requested.
        """
        # Step 3: Switch context
        if not self._switch_to_login_context():
            logger.warning("Context not found, waiting for load...")
            WebDriverWait(self.driver, 10).until(lambda d: self._switch_to_login_context())

        # Step 4: Choose 'Login with Password'
        try:
            logger.info("Selecting Password tab...")
            tab = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_TAB))
            self.driver.execute_script("arguments[0].click();", tab)
            # Small wait for UI flip
            self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        except:
            logger.debug("Password tab selection failed or already active.")

        # Step 5: Enter Email/Username
        logger.info(f"Entering username: {username}")
        self.send_keys(self.USERNAME_INPUT, username)

        # Step 5a: Handle 'Proceed' button if present
        try:
            proceed = self.driver.find_element(*self.PROCEED_BTN)
            if proceed.is_displayed():
                logger.info("Clicking Proceed...")
                self.driver.execute_script("arguments[0].click();", proceed)
                self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        except:
            pass

        # Step 6: Enter Password
        logger.info("Entering password...")
        # Re-verify context in case of internal iframe refresh
        if not self.is_visible(self.PASSWORD_INPUT, timeout=3):
            self._switch_to_login_context()
            
        password_field = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT))
        password_field.clear()
        password_field.send_keys(password)

        # Step 7: Click Submit Button
        logger.info("Submitting login form...")
        submit = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        self.driver.execute_script("arguments[0].click();", submit)

        # Step 7a: Success Verification
        self.driver.switch_to.default_content()
        logger.info("Login flow completed. Verifying session...")
        # (Verification logic managed by test cases)
