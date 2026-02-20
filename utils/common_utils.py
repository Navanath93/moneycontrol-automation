import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

def handle_alert_if_present(driver, action="accept"):
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        logger.info(f"Alert detected: {alert.text}")
        if action == "accept":
            alert.accept()
        else:
            alert.dismiss()
    except Exception:
        pass
