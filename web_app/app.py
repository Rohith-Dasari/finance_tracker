from flask import Flask, request, g
from config import TOKEN_COOKIE
from extensions import auth_service
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.chat import chat_bp


def create_app():
    app = Flask(__name__)

    @app.before_request
    def load_user():
        token = request.cookies.get(TOKEN_COOKIE)
        payload = auth_service.verify_token(token) if token else None
        g.user = {"username": payload["username"]} if payload else None

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(chat_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
