import pytest
from pages.home_page import HomePage


@pytest.mark.ui
def test_search_left_panel_options_are_clickable(driver):
    home = HomePage(driver)
    home.open_home_page()

    home.search_stock("Reliance")

    assert home.are_left_panel_options_clickable(), \
        "One or more left panel search options are not clickable"
