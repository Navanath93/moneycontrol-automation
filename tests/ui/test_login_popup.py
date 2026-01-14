from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_login_dropdown_and_modal(driver):
    home = HomePage(driver)
    home.open_home_page()

    home.click_hello_login()
    assert home.is_login_dropdown_displayed()

    home.validate_login_dropdown_options()

    home.click_login_option()

    login = LoginPage(driver)
    assert login.is_login_modal_displayed()
