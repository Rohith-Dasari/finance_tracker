from dataclasses import dataclass

@dataclass
class StockStats:
    open: float
    high: float
    low: float
    close: float
    volume: int

    @classmethod
    def from_dict(cls, data: dict) -> "StockStats":
        return cls(
            open=float(data.get("open", 0.0)),
            high=float(data.get("high", 0.0)),
            low=float(data.get("low", 0.0)),
            close=float(data.get("close", 0.0)),
            volume=int(data.get("volume", 0)),
        )

    @property
    def change(self) -> float:
        return self.close - self.open

    @property
    def change_percent(self) -> float:
        return (self.change / self.open) * 100 if self.open else 0.0
