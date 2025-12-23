from fastmcp import FastMCP
import requests

API_BASE = "http://127.0.0.1:8000/"

mcp = FastMCP("FinanceMCP")


def _handle(resp):
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
def add_to_watchlist(username: str, stock_name: str):
    """Add a stock to the user's watchlist by name or symbol."""
    r = requests.post(
        f"{API_BASE}/api/users/{username}/watchlist",
        json={"stock_name": stock_name},
        timeout=15,
    )
    return _handle(r)


@mcp.tool()
def remove_from_watchlist(username: str, symbol: str):
    """Remove a stock from the user's watchlist by symbol."""
    r = requests.delete(
        f"{API_BASE}/api/users/{username}/watchlist/{symbol}",
        timeout=15,
    )
    return _handle(r)


@mcp.tool()
def watchlist_summary(username: str):
    """Get today's snapshot for all symbols in the user's watchlist."""
    r = requests.get(f"{API_BASE}/api/users/{username}/watchlist/summary", timeout=15)
    return _handle(r)


@mcp.tool()
def watchlist_symbol_status(username: str, symbol: str):
    """Check if a symbol is in the user's watchlist."""

    r = requests.get(
        f"{API_BASE}/api/users/{username}/watchlist/{symbol}",
        timeout=15,
    )
    return _handle(r)


@mcp.tool()
def stock_performance(stock_name: str):
    """Get today's performance for a stock by name or symbol."""
    r = requests.get(
        f"{API_BASE}/api/stocks/{stock_name}/performance",
        timeout=15,
    )
    return _handle(r)


@mcp.tool()
def stock_news(stock_name: str, count: int = 5):
    """Fetch recent news for a stock by name or symbol."""
    r = requests.get(
        f"{API_BASE}/api/stocks/{stock_name}/news",
        params={"count": count},
        timeout=15,
    )
    return _handle(r)


@mcp.tool()
def get_stock_history(ticker: str, start_date: str, end_date: str):
    """
    Retrieve historical OHLCV stock data.

    If the user mentions:
    - "start of the month" → assume first day of current month
    - If end_date is missing → assume today

    Date format: YYYY-MM-DD
    """

    r = requests.get(
        f"{API_BASE}/api/stocks/{ticker}/history",
        params={"start": start_date, "end": end_date},
        timeout=15,
    )
    return _handle(r)


@mcp.tool()
def add_expense(username: str, amount: float, category: str):
    """
    Add an expense with category for a user.
    """
    r = requests.post(
        f"{API_BASE}/api/users/{username}/expenses",
        json={"amount": amount, "category": category},
        timeout=10,
    )
    return _handle(r)


@mcp.tool()
def get_expenses_by_category(username: str, category: str):
    """
    Get expenses and total for a specific category.
    """
    r = requests.get(
        f"{API_BASE}/api/users/{username}/expenses",
        params={"category": category},
        timeout=10,
    )
    return _handle(r)


@mcp.tool()
def get_expense_summary(username: str):
    """
    Get all category-wise expense totals.
    """
    r = requests.get(
        f"{API_BASE}/api/users/{username}/expenses/summary",
        timeout=10,
    )
    return _handle(r)


if __name__ == "__main__":
    mcp.run()
