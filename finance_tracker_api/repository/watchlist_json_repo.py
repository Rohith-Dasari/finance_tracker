import os
import json
class WatchlistRepository:
    def __init__(self, path: str="data.json"):
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

    def get_watchlist(self,username):
        data=self._load()
        for record in data:
            if record["username"] == username: 
               return record["watchlist"]
        return []
    
    def add_stock(self, username, stock_name):
        data = self._load()

        for record in data:
            if record["username"] == username:
                if stock_name not in record["watchlist"]:
                    record["watchlist"].append(stock_name)
                break
        else:
            raise ValueError("User not found")

        self._save(data)


    def remove_stock(self, username, stock_name):
        data = self._load()

        for record in data:
            if record["username"] == username:
                if stock_name in record["watchlist"]:
                    record["watchlist"].remove(stock_name)
                break
        else:
            raise ValueError("User not found")

        self._save(data)

