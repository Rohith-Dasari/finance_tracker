class User:
    def __init__(self, username, number, watchlist=None,expenses=None):
        self.username=username
        self.number=number
        self.watchlist= watchlist if watchlist else []
        self.expenses=expenses if expenses else []
    
    
