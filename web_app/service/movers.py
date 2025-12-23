import requests

from models.stock_mover import StockMover

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"


def _fetch_screener(scr_id, count=10, region="US"):
    params = {
        "scrIds": scr_id,
        "count": count,
        "region": region
    }

    r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()

    return r.json()["finance"]["result"][0]["quotes"]


def _extract_required_fields(quotes):
    cleaned = []

    for q in quotes:
        cleaned.append(
            StockMover(
                symbol=q.get("symbol", "Unknown"),
                name=q.get("longName") or q.get("shortName") or "Unavailable",
                price=q.get("regularMarketPrice"),
                change=q.get("regularMarketChange"),
                change_percent=q.get("regularMarketChangePercent"),
                volume=q.get("regularMarketVolume"),
                avg_volume_3m=q.get("averageDailyVolume3Month"),
                market_cap=q.get("marketCap"),
            )
        )

    return cleaned


def get_top_losers(count=2, region="US"):
    raw = _fetch_screener("day_losers", count, region)
    return _extract_required_fields(raw)


def get_top_gainers(count=2, region="US"):
    raw = _fetch_screener("day_gainers", count, region)
    return _extract_required_fields(raw)
