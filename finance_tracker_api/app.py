from flask import Flask, request, g
from routes.expenses import expenses_bp
from routes.stock_news import stock_bp
from routes.watchlist import watchlist_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(watchlist_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(stock_bp)

    return app


app = create_app()
if __name__ == "__main__":
    app.run(port=8000)
