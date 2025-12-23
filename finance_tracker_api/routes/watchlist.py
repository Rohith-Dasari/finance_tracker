from flask import Blueprint, jsonify, request
import services.symbol_finder as symbol_finder
from services.get_today_price import get_today_price_stats
from extensions import wl_repo
from concurrent.futures import ThreadPoolExecutor, as_completed

watchlist_bp = Blueprint("watchlist", __name__)


@watchlist_bp.route("/api/users/<username>/watchlist", methods=["GET", "POST"])
def add_or_list_watchlist(username):
    if request.method == "GET":
        watchlist = wl_repo.get_watchlist(username)
        return jsonify({"watchlist": watchlist})

    payload = request.get_json(silent=True) or {}
    stock_name = payload.get("stock_name") or payload.get("symbol")
    if not stock_name:
        return jsonify({"error": "stock_name is required"}), 400

    symbol = symbol_finder.find_ticker(stock_name)

    try:
        wl_repo.add_stock(username=username, stock_name=symbol)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

    return jsonify({"watchlist": wl_repo.get_watchlist(username)})


@watchlist_bp.route(
    "/api/users/<username>/watchlist/<symbol>", methods=["DELETE", "GET"]
)
def remove_or_status_watchlist(username, symbol):
    if request.method == "GET":
        watchlist = wl_repo.get_watchlist(username)
        return jsonify({"symbol": symbol, "in_watchlist": symbol in watchlist})

    try:
        wl_repo.remove_stock(username=username, stock_name=symbol)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

    return jsonify({"watchlist": wl_repo.get_watchlist(username)})


@watchlist_bp.route("/api/users/<username>/watchlist/summary", methods=["GET"])
def get_watchlist_summary(username):
    watchlist = wl_repo.get_watchlist(username)
    rows = []

    def fetch(symbol):
        stats = get_today_price_stats(symbol)
        if stats:
            return {"symbol": symbol, **stats}
        return None

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch, s) for s in watchlist]
        for f in as_completed(futures):
            result = f.result()
            if result:
                rows.append(result)

    return jsonify({"symbols": watchlist, "data": rows})
