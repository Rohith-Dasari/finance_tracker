import json
import os
from typing import Optional

from models.user import User
from models.credentials import Credentials


class UserJSONRepository:
    def __init__(self, path: str = "data.json"):
        self.db = path
        if not os.path.exists(self.db):
            with open(self.db, "w") as f:
                json.dump([], f)

    def _load(self):
        with open(self.db, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.db, "w") as f:
            json.dump(data, f, indent=2)

    def add_user(self, user: User, creds: Credentials):
        data = self._load()

        for record in data:
            if record["username"] == user.username:
                raise ValueError("User already exists")

        data.append(
            {
                "username": user.username,
                "password": creds.password,
                "phonenumber": user.number,
                "watchlist": user.watchlist,
                "expenses": user.expenses,
            }
        )

        self._save(data)

    def get_user(self, username: str) -> Optional[User]:
        data = self._load()

        for record in data:
            if record["username"] == username:
                user = User(
                    record["username"],
                    record.get("phonenumber"),
                    record.get("watchlist"),
                    record.get("expenses"),
                )
                return user

        return None

    def get_all_users(self) -> Optional[User]:
        users = []
        data = self._load()
        for record in data:
            users.append(
                User(
                    record["username"],
                    record.get("phonenumber"),
                    record.get("watchlist"),
                    record.get("expenses"),
                )
            )
        return users

    def get_credentials(self, username: str) -> Optional[Credentials]:
        data = self._load()
        for record in data:
            if record["username"] == username:
                return Credentials(record["username"], record["password"])

        return None
