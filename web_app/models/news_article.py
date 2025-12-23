from datetime import datetime
from typing import Optional


class NewsArticle:
    def __init__(
        self,
        headline: str,
        publisher: str,
        url: str,
        published_at: Optional[datetime] = None,
    ):
        self.headline = headline
        self.publisher = publisher
        self.url = url
        self.published_at = published_at

    def __repr__(self):
        return f"NewsArticle({self.headline})"

    def __str__(self):
        return f"{self.headline}\n{self.publisher}\n{self.url}"

    @property
    def display_published_at(self) -> str:
        if isinstance(self.published_at, datetime):
            return self.published_at.strftime("%b %d, %Y %I:%M %p")
        return "Time unavailable"
