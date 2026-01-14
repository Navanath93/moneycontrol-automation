import pytest
import requests

@pytest.mark.skip(reason="API blocked by Moneycontrol, skipping for now")
def test_reliance_market_api():
    url = "https://priceapi.moneycontrol.com/pricefeed/nse/equitycash/RELIANCE"
    response = requests.get(url)
    assert response.status_code == 200
