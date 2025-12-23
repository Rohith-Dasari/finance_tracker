import os
import json
from typing import List, Dict


class ExpensesRepository:
    def __init__(self, path: str = "data.json"):
        self.db = path
        if not os.path.exists(self.db):
            with open(self.db, "w") as f:
                json.dump([], f)

    def _load(self) -> list:
        with open(self.db, "r") as f:
            return json.load(f)

    def _save(self, data: list):
        with open(self.db, "w") as f:
            json.dump(data, f, indent=2)

    def _find_user(self, data: list, username: str):
        for idx, record in enumerate(data):
            if record.get("username") == username:
                return idx, record
        return None, None

    def add_expense(self, username: str, amount: float, category: str):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if not category:
            raise ValueError("Category is required")

        data = self._load()
        idx, record = self._find_user(data, username)
        if record is None:
            raise ValueError("User not found")

        expenses = record.get("expenses") or []
        expenses.append({"amount": amount, "category": category})

        record["expenses"] = expenses
        data[idx] = record
        self._save(data)
        return expenses

    def get_expenses_by_category(self, username: str, category: str) -> List[dict]:
        data = self._load()
        _, record = self._find_user(data, username)
        if record is None:
            raise ValueError("User not found")

        expenses = record.get("expenses") or []
        return [
            exp
            for exp in expenses
            if exp.get("category", "").lower() == category.lower()
        ]

    def get_category_total(self, username: str, category: str) -> float:
        expenses = self.get_expenses_by_category(username, category)
        return sum(exp["amount"] for exp in expenses)

    def get_all_category_totals(self, username: str) -> Dict[str, float]:
        data = self._load()
        _, record = self._find_user(data, username)
        if record is None:
            raise ValueError("User not found")

        expenses = record.get("expenses") or []
        totals: Dict[str, float] = {}

        for exp in expenses:
            cat = exp.get("category")
            totals[cat] = totals.get(cat, 0) + exp.get("amount", 0)

        return totals
