import requests

def call_search_api(query):
    url = "https://www.moneycontrol.com/mc/widget/mc_autosuggest.php"
    response = requests.get(url, params={"query": query}, headers={"User-Agent": "Mozilla/5.0"})
    if "application/json" in response.headers.get("Content-Type", ""):
        try:
            return response.json()
        except ValueError:
            return {"error": response.text}
    return {"error": response.text}

