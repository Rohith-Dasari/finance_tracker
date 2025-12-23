from flask import Blueprint, render_template, request, redirect, url_for, make_response
from config import TOKEN_COOKIE
from extensions import auth_service

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.jinja2")

    username = request.form.get("username")
    password = request.form.get("password")

    try:
        user = auth_service.login(username, password)
    except ValueError:
        return render_template("login.jinja2", error="Invalid credentials"), 401

    token = auth_service.generate_token(user)
    resp = make_response(redirect(url_for("dashboard.dashboard")))
    resp.set_cookie(TOKEN_COOKIE, token, httponly=True, samesite="Lax")
    return resp


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.jinja2")

    username = request.form.get("username")
    password = request.form.get("password")
    phonenumber = request.form.get("phonenumber")

    try:
        user = auth_service.signup(username, password, phonenumber)
    except ValueError as ve:
        return render_template("signup.jinja2", error=str(ve)), 400

    token = auth_service.generate_token(user)
    resp = make_response(redirect(url_for("dashboard.dashboard")))
    resp.set_cookie(TOKEN_COOKIE, token, httponly=True, samesite="Lax")
    return resp
