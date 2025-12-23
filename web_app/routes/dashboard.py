from flask import Blueprint, render_template
from service.movers import get_top_gainers, get_top_losers
from service.news import get_market_headlines

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    headlines = []
    top_gainers = []
    top_losers = []

    try:
        headlines = get_market_headlines(count=10)
    except Exception as exc:
        print(f"Failed to load market headlines: {exc}")

    try:
        top_gainers = get_top_gainers(count=5)
    except Exception as exc:
        print(f"Failed to load top gainers: {exc}")

    try:
        top_losers = get_top_losers(count=5)
    except Exception as exc:
        print(f"Failed to load top losers: {exc}")

    return render_template(
        "dashboard.jinja2",
        headlines=headlines,
        top_gainers=top_gainers,
        top_losers=top_losers,
    )
