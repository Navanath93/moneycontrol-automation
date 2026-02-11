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

    assert response.status_code == 200
