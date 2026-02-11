import requests


def test_reliance_market_api():

    url = "https://priceapi.moneycontrol.com/pricefeed/nse/equitycash/RELIANCE"

    # Important: mimic Postman/browser headers
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Connection": "keep-alive"
    }

    response = requests.get(url, headers=headers, timeout=20)

    # Step 1: HTTP validation
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"

    # Step 2: JSON validation
    data = response.json()

    assert "code" in data
    assert "message" in data
    assert "data" in data

    # Step 3: Business response validation
    # Based on your Postman result
    assert data["code"] in ["200", "201"]
