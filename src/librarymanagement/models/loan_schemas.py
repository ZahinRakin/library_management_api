from beanie import Document
from typing import Optional
from datetime import datetime, timedelta

from pydantic import BaseModel, EmailStr

from librarymanagement.models.loan_models import Loan

# request models
class LoanRequestModel(BaseModel):
    user_id: str
    book_id: str
    due_date: Optional[datetime]

class LoanReturnRequestModel(BaseModel):
    loan_id: str

class LoanExtensionRequestModel(BaseModel):
    extension_days: int


# response models

class LoanExtensionResponseModel(BaseModel):
    id: str  # loan.id
    user_id: str
    book_id: str
    issue_date: datetime
    original_due_date: datetime
    extended_due_date: datetime
    status: str
    extensions_count: int



class BookMainAttributes(BaseModel):
    id: str # book id
    title: str
    author: str
class UserMainAttributes(BaseModel):
    id: str
    name: str
    email: EmailStr

class OverdueLoanResponseModel(BaseModel):
    id: str # loan id
    user: UserMainAttributes
    book: BookMainAttributes
    issue_date: datetime
    due_date: datetime
    days_overdue: int



class LoanResponseModel(BaseModel):
    id: str # loan id
    book: Optional[BookMainAttributes]
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str