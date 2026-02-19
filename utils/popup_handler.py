import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

class PopupHandler:
    """
    Handles random popups, ads, and overlays that block UI interaction.
    """

    # Combined selector for faster scanning
    COMBINED_POPUP_LOCATOR = (
        By.CSS_SELECTOR, 
        ".close-btn, div.cross_icon, #wzrk-cancel, .wzrk-alert-wiz-btn-close, .CT_interstitial_close_icon, #push_notification_close, .active .close"
    )
    
    # Combined XPath for buttons or text-based matches
    COMBINED_POPUP_XPATH = (
        By.XPATH,
        "//button[normalize-space()='No thanks'] | //div[@class='CT_interstitial_close_icon'] | "
        "//button[contains(@class, 'close')] | //div[contains(@class, 'close') and contains(@class, 'btn')]"
    )

    def __init__(self, driver):
        self.driver = driver

    def handle_potential_popups(self):
        closed = False

        def close_visible_popups():
            nonlocal closed
            for selector in [self.COMBINED_POPUP_LOCATOR, self.COMBINED_POPUP_XPATH]:
                try:
                    elements = self.driver.find_elements(*selector)
                    for element in elements:
                        if element.is_displayed():
                            logger.info("Popup found and closed.")
                            self.driver.execute_script("arguments[0].click();", element)
                            closed = True
                except Exception as e:
                    logger.debug(f"Popup handling error: {e}")
            return closed

        self.driver.switch_to.default_content()
        close_visible_popups()
        self.remove_blocking_overlays()
        return closed

    def handle_iframe_popups(self):
        """
        Switches only to suspected ad iframes and tries to close them.
        """
        ad_iframe_indicators = ["google_ads_iframe", "aswift", "webengage-notification"]
        try:
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for frame in iframes:
                try:
                    frame_id = frame.get_attribute("id") or ""
                    frame_name = frame.get_attribute("name") or ""
                    if any(ind in frame_id or ind in frame_name for ind in ad_iframe_indicators):
                        self.driver.switch_to.frame(frame)
                        # Quick check inside iframe
                        self.handle_potential_popups()
                        self.driver.switch_to.default_content()
                except Exception:
                    self.driver.switch_to.default_content()
        except Exception:
            pass

    def remove_blocking_overlays(self):
        """
        Removes persistent overlays and suppresses forced scroll-locks.
        """
        overlay_classes = [
            'wzrk-overlay', 'webengage-widget-overlay', 'CT_shim', 
            'interstitial-wrapper', 'modal-backdrop', 'wzrk-alert-wizard'
        ]
        try:
            js_script = """
                var classes = arguments[0];
                classes.forEach(function(cls) {
                    var els = document.getElementsByClassName(cls);
                    for(var i=0; i<els.length; i++){ els[i].style.display='none'; }
                });
                document.body.style.overflow = 'auto';
                document.documentElement.style.overflow = 'auto';
            """
            self.driver.execute_script(js_script, overlay_classes)
        except Exception:
            pass
