from flask import Blueprint, request, g
from config import GEMINI_API_KEY
import asyncio
from service.chat_service import run_chat

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
def api_chat():
    if not g.get("user"):
        return {"error": "unauthorized"}, 401

    if not GEMINI_API_KEY:
        return {"error": "GEMINI_API_KEY not set on server"}, 500

    payload = request.get_json(silent=True) or {}
    prompt = payload.get("message")
    if not prompt:
        return {"error": "message is required"}, 400

    try:
        reply = asyncio.run(run_chat(prompt, g.user["username"]))
    except Exception as exc:
        return {"error": str(exc)}, 500

    return {"reply": reply}
