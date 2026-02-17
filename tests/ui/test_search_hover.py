import pytest
from pages.home_page import HomePage


@pytest.mark.ui
def test_search_autosuggest_hover_and_click(driver):
    home = HomePage(driver)
    home.open_home_page()

    # Validate autosuggest loads
    assert home.trigger_search_suggestions("Reliance"), \
        "Autosuggest did not load"

    # Validate hover and click works
    assert home.search_with_hover("Reliance"), \
        "Autosuggest hover click failed"


@pytest.mark.ui
def test_search_hover_left_and_right_panels(driver):
    home = HomePage(driver)
    home.open_home_page()

    # Ensure autosuggest appears
    assert home.trigger_search_suggestions("Reliance"), \
        "Autosuggest panel did not appear"

    suggestions = home.get_search_suggestions()
    assert suggestions, "Suggestions list empty"

    for item in suggestions:
        assert item.is_displayed()


@pytest.mark.strict
def test_search_hover_panels_must_appear(driver):
    home = HomePage(driver)
    home.open_home_page()

    assert home.trigger_search_suggestions("Reliance"), (
        "Search autosuggest panels did not appear"
    )
