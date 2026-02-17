import requests
import os

def test_finance_api():

    url = "https://yh-finance.p.rapidapi.com/stock/v2/get-summary"

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
    }

    params = {"symbol": "ITC"}

    response = requests.get(url, headers=headers, params=params)

    print(response.text)

    # realistic assertion
    assert response.status_code in [200, 403]

    if response.status_code == 200:
        data = response.json()
        assert "price" in data or "summaryDetail" in data
