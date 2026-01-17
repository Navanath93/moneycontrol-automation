import pytest
from pages.home_page import HomePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
def test_login_dropdown_and_modal(driver):
    home = HomePage(driver)
    home.open_home_page()

    home.open_login()

    wait = WebDriverWait(driver, 20)

    login_ui = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//*[contains(text(),'Login') or contains(text(),'Sign')]"
        ))
    )

    assert login_ui is not None
