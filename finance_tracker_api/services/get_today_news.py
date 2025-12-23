import requests
HEADERS = {"User-Agent": "Mozilla/5.0"}
def get_stock_headlines(symbol, count=5):
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {
        "q": symbol,
        "newsCount": count,
        "quotesCount": 0
    }

    r = requests.get(url, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()

    news = r.json().get("news", [])

    return [
        {
            "title": n.get("title"),
            "publisher": n.get("publisher"),
            "link": n.get("link"),
            "published_at": n.get("providerPublishTime")
        }
        for n in news
    ]
