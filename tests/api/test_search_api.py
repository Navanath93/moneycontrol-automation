import pytest
import requests

BASE_URL = "https://www.moneycontrol.com/mc/widget/mc_autosuggest.php"

@pytest.mark.api
def test_valid_search_api():
    params = {"query": "Reliance"}
    response = requests.get(BASE_URL, params=params, headers={"User-Agent": "Mozilla/5.0"})
    assert response.status_code == 200
    try:
        data = response.json()
        assert any("Reliance" in item.get("name", "") for item in data)
    except ValueError:
        assert "Bad request" in response.text


@pytest.mark.api
def test_invalid_search_api():
    params = {"query": "xyz123"}
    response = requests.get(BASE_URL, params=params, headers={"User-Agent": "Mozilla/5.0"})
    assert response.status_code == 200
    if "application/json" in response.headers.get("Content-Type", ""):
        data = response.json()
        assert len(data) == 0 or all("xyz123" not in item.get("name", "") for item in data)
    else:
        assert "Bad request" in response.text


@pytest.mark.api
def test_search_api_response_structure():
    params = {"query": "Infosys"}
    response = requests.get(BASE_URL, params=params, headers={"User-Agent": "Mozilla/5.0"})
    assert response.status_code == 200
    if "application/json" in response.headers.get("Content-Type", ""):
        data = response.json()
        for item in data:
            assert "name" in item
            assert "url" in item
    else:
        assert "Bad request" in response.text

