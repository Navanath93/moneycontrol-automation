import requests


def test_reliance_market_api():

    url = "https://priceapi.moneycontrol.com/pricefeed/nse/equitycash/RELIANCE"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.moneycontrol.com/",
        "Origin": "https://www.moneycontrol.com",
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
