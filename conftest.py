import logging
import pytest
import os
import allure
from datetime import datetime
from utils.browser_factory import get_driver
from utils.cache_manager import CacheManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store_true", default=False)
    parser.addoption("--clear-cache", action="store_true", default=False, help="Clear cache before run")

def pytest_sessionstart(session):
    """Called before the first test starts."""
    logger.info("Starting Automation Test Session")
    CacheManager.clear_pytest_cache()
    
    # Ensure reports directory structure exists
    os.makedirs("reports", exist_ok=True)
    os.makedirs(os.path.join("reports", "screenshots"), exist_ok=True)

@pytest.fixture(scope="class")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    # Initialize driver
    _driver = get_driver(browser, headless)
    _driver.implicitly_wait(2) # Reduced safety net implicit wait
    
    # Attach driver to class if available
    if request.cls is not None:
        request.cls.driver = _driver
        
    yield _driver

    try:
        _driver.quit()
    except Exception:
        pass

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Only look at failed tests in the 'call' phase
    if rep.when != "call" or not rep.failed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    try:
        # Check if driver session is still active
        if driver.session_id is None:
            logger.error("Driver session is already closed. Cannot capture screenshot.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = item.name

        # 1. Attach Screenshot to Allure
        screenshot_bytes = driver.get_screenshot_as_png()
        allure.attach(
            screenshot_bytes, 
            name=f"Screenshot_{test_name}_{timestamp}", 
            attachment_type=allure.attachment_type.PNG
        )

        logger.error(f"Test Failed: {test_name}. Screenshot attached to report.")
        
        # Local backup for direct troubleshooting
        screenshot_path = os.path.join("reports", "screenshots", f"{test_name}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)

    except Exception as e:
        logger.error(f"Could not capture failure screenshot: {e}")
