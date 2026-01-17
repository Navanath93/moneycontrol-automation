from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def get_driver(browser):
    if browser == "chrome":
        options = webdriver.ChromeOptions()

        # Stability options
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")

        # Do not wait for full page load
        options.page_load_strategy = "eager"

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

        driver.set_page_load_timeout(60)
        return driver

    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(60)
        return driver

    raise ValueError(f"Browser '{browser}' is not supported")
