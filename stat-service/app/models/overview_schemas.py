from pydantic import BaseModel


class OverviewModel(BaseModel):
    total_books: int
    total_users: int
    books_available: int
    overdue_loans: int
    loans_today: int
    returns_today: int