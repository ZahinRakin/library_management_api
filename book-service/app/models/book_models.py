from beanie import Document
from datetime import datetime, timezone
from pydantic import Field

class Book(Document):
    title: str
    author: str
    isbn: str
    genre: str
    copies: int
    available_copies: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    async def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return await super().save(*args, **kwargs)

    class Settings:
        name = "Book"
