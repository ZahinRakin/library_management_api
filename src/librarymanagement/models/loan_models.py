from typing import Optional
from beanie import Document, Link
from pydantic import model_validator, ConfigDict
from datetime import datetime


class Loan(Document):
    user_id: str
    book_id: str
    issue_date: datetime
    due_date: Optional[datetime]
    status: str  # "ACTIVE" or "RETURNED"
    return_date: Optional[datetime] = None
    extension_count: Optional[int] = 0

    class Settings:
        name = "Loan"


#       {
#     "id": 985,
#     "user": {
#       "id": 15,
#       "name": "John Smith",
#       "email": "john@example.com"
#     },
#     "book": {
#       "id": 23,
#       "title": "The Pragmatic Programmer",
#       "author": "Andrew Hunt, David Thomas"
#     },
#     "issue_date": "2025-03-15T10:30:00Z",
#     "due_date": "2025-03-29T23:59:59Z",
#     "days_overdue": 29
#   }
