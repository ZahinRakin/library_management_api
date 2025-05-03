from pydantic import BaseModel
from typing import Optional


class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    genre: Optional[str] = None
    copies: Optional[int] = None
    available_copies: Optional[int] = None


class BookAvailability(BaseModel):
    available_copies: int
