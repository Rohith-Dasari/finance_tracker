from flask import Blueprint, jsonify, request
from extensions import expenses_repo

expenses_bp = Blueprint("expenses", __name__)


@expenses_bp.route("/api/users/<username>/expenses", methods=["POST"])
def add_expense(username):
    payload = request.get_json(silent=True) or {}

    amount = payload.get("amount")
    category = payload.get("category")

    if amount is None or not category:
        return jsonify({"error": "amount and category required"}), 400

    try:
        expenses = expenses_repo.add_expense(
            username=username, amount=float(amount), category=category
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"status": "expense added", "expenses": expenses}), 201


@expenses_bp.route("/api/users/<username>/expenses", methods=["GET"])
def get_expenses_by_category(username):
    category = request.args.get("category")
    if not category:
        return jsonify({"error": "category query param required"}), 400

    try:
        expenses = expenses_repo.get_expenses_by_category(username, category)
        total = expenses_repo.get_category_total(username, category)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify({"category": category, "expenses": expenses, "total": total})


@expenses_bp.route("/api/users/<username>/expenses/summary", methods=["GET"])
def get_all_category_summary(username):
    try:
        totals = expenses_repo.get_all_category_totals(username)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(totals)
