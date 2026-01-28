import pytest
from pages.home_page import HomePage

@pytest.mark.ui
def test_search_autosuggest_hover_and_click(driver):
    home = HomePage(driver)
    home.open_home_page()

    if not home.trigger_search_suggestions("Reliance"):
        pytest.xfail("Autosuggest not available in this session")

    assert home.search_with_hover("Reliance")




def test_search_hover_left_and_right_panels(driver):
    home = HomePage(driver)
    home.open_home_page()

    suggestions_loaded = home.trigger_search_suggestions("Reliance")

    if not suggestions_loaded:
        pytest.xfail(
            "Autosuggest panels are inconsistent on Moneycontrol "
            "(known production behavior)"
        )

    suggestions = home.get_search_suggestions()
    assert suggestions, "Suggestions list empty when panel appeared"

    for item in suggestions:
        assert item.is_displayed()

# Business expectation: autosuggest must appear for valid keywords
# Known instability exists, but this test enforces requirement

@pytest.mark.strict
def test_search_hover_panels_must_appear(driver):
    home = HomePage(driver)
    home.open_home_page()

    assert home.trigger_search_suggestions("Reliance"), (
        "Search autosuggest panels did not appear"
    )


