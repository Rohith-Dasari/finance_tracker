class StockMover:
    def __init__(
        self,
        symbol: str,
        name: str,
        price: float,
        change: float,
        change_percent: float,
        volume: int,
        avg_volume_3m: int,
        market_cap: int,
    ):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.change = change
        self.change_percent = change_percent
        self.volume = volume
        self.avg_volume_3m = avg_volume_3m
        self.market_cap = market_cap

    def __repr__(self):
        return (
            f"StockMover(symbol={self.symbol}, price={self.price}, "
            f"change={self.change}, change_percent={self.change_percent}%)"
        )
