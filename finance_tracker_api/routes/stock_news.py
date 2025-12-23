from flask import Blueprint, jsonify, request
from services.get_today_news import get_stock_headlines
from services.get_mentioned_date_price import get_price_stats
import services.symbol_finder as symbol_finder
from services.get_today_price import get_today_price_stats

stock_bp = Blueprint("stock_news", __name__)


@stock_bp.route("/api/stocks/<stock_name>/performance", methods=["GET"])
def get_stock_performance(stock_name):
    symbol = symbol_finder.find_ticker(stock_name)
    if not symbol:
        return jsonify({"error": "Could not resolve symbol"}), 400

    stats = get_today_price_stats(symbol)
    if not stats:
        return jsonify({"error": "No data"}), 404

    return jsonify({"symbol": symbol, **stats})


@stock_bp.route("/api/stocks/<stock_name>/news", methods=["GET"])
def get_stock_news(stock_name):
    symbol = symbol_finder.find_ticker(stock_name)
    if not symbol:
        return jsonify({"error": "Could not resolve symbol"}), 400

    count = request.args.get("count", default=5, type=int)
    articles = get_stock_headlines(symbol, count=count)
    return jsonify({"symbol": symbol, "articles": articles})


@stock_bp.route("/api/stocks/<ticker>/history", methods=["GET"])
def stock_history(ticker):
    start = request.args.get("start")
    end = request.args.get("end")
    symbol = symbol_finder.find_ticker(ticker)

    if not start or not end:
        return jsonify({"error": "start and end dates are required"}), 400

    data = get_price_stats(symbol, start, end)
    if not data:
        return jsonify({"error": "No data found"}), 404

    return jsonify({"ticker": ticker.upper(), "start": start, "end": end, "data": data})
