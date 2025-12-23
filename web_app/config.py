import os

SECRET = os.environ.get("SECRET_KEY", "dev-secret")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
TOKEN_COOKIE = "access_token"
