from datetime import datetime
from typing import List

import requests

from models.news_article import NewsArticle

HEADERS = {"User-Agent": "Mozilla/5.0"}
SEARCH_URL = "https://query2.finance.yahoo.com/v1/finance/search"


def _parse_publish_time(timestamp):
    if not timestamp:
        return None

    try:
        return datetime.fromtimestamp(timestamp)
    except (ValueError, OSError, TypeError):
        return None


def get_market_headlines(count: int = 10) -> List[NewsArticle]:
    params = {
        "q": "stock market",
        "newsCount": count,
        "quotesCount": 0,
    }

    response = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()

    articles = []
    for entry in response.json().get("news", []):
        articles.append(
            NewsArticle(
                headline=entry.get("title") or "Untitled",
                publisher=entry.get("publisher") or "Unknown",
                url=entry.get("link") or "",
                published_at=_parse_publish_time(entry.get("providerPublishTime")),
            )
        )

    articles.sort(
        key=lambda item: item.published_at or datetime.min,
        reverse=True,
    )

    return articles

