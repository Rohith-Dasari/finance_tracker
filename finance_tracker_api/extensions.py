from repository.watchlist_json_repo import WatchlistRepository
from repository.expenses_json_repo import ExpensesRepository

import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../web_app", "user_data.json")
wl_repo = WatchlistRepository(DATA_PATH)
expenses_repo = ExpensesRepository(DATA_PATH)
