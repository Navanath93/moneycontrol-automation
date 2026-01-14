from pages.home_page import HomePage

def test_search_stock(driver):
    home = HomePage(driver)
    home.open_home_page()
    home.search_stock("Reliance")

    assert "Reliance" in driver.page_source
