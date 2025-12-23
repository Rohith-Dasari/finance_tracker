import requests
import yfinance as yf

def find_ticker(company_name):
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {
        "q": company_name,
        "quotesCount": 5,
        "newsCount": 0
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    for q in data["quotes"]:
        return q.get("symbol")

# quotes=find_ticker(input("Enter the company name: "))
# for q in quotes:
#     symbol=q.get("symbol")