import pytest
import os
from datetime import datetime
from utils.browser_factory import get_driver


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    driver = get_driver(browser)

    yield driver

    try:
        driver.quit()
    except Exception:
        pass



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Only act on real test failures
    if rep.when != "call" or not rep.failed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    # If browser session is already gone, do nothing
    if not hasattr(driver, "session_id") or driver.session_id is None:
        return

    try:
        screenshots_dir = os.path.join(
            os.getcwd(), "screenshots", "test_failures"
        )
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(
            screenshots_dir, f"{item.name}_{timestamp}.png"
        )

        # Hard timeout protection
        driver.set_script_timeout(5)
        driver.save_screenshot(screenshot_path)

    except Exception:
        # NEVER allow screenshot problems to crash pytest
        pass
