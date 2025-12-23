import yfinance as yf
def get_today_price_stats(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1d")

    if df.empty:
        return None

    row = df.iloc[0]
    return {
        "open": float(row["Open"]),
        "high": float(row["High"]),
        "low": float(row["Low"]),
        "close": float(row["Close"]),
        "volume": int(row["Volume"])
    }
