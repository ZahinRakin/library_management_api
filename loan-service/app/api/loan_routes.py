from fastapi import APIRouter
from typing import List

from app.models.loan_models import Loan
from app.models.loan_schemas import (
    OverdueLoanResponseModel,
    LoanReturnRequestModel,
    LoanResponseModel,
    LoanExtensionRequestModel
)
from app.models.loan_schemas import LoanExtensionResponseModel
from app.models.loan_schemas import LoanRequestModel

from app.services.loan import (
    issue_book,
    return_book,
    view_loans,
    view_user_loans,
    fetch_overdue_loans,
    extend_loan,
    get_loan_per_book,
    get_active_counts,
    get_loans_today_count,
    get_returns_today
)

router = APIRouter()


@router.get("/", response_model=List[Loan])
async def get_all_loans():
    return await view_loans()

@router.post("/", response_model=Loan)
async def book_issue(issue_data: LoanRequestModel):
    return await issue_book(issue_data)

@router.get("/today", response_model=int)                                    # testing due
async def today_loan_count():
    return await get_loans_today_count()

@router.post("/return", response_model=Loan)
async def user_return_book(request: LoanReturnRequestModel):
    return await return_book(request.loan_id)

@router.get("/returns/today", response_model=int)
async def return_today():
    return await get_returns_today()

@router.get("/overdue", response_model=List[OverdueLoanResponseModel])
async def get_overdue_loans():
    print("inside overdue route") # debugging log
    return await  fetch_overdue_loans()

@router.get("/active/count/{limit}")                                         # testing due
async def active_counts(limit: int):
    return await get_active_counts(limit)

@router.get("/count-per-book/{limit}")                                       # testing due
async def get_per_book_borrow_count(limit:int):
    return await get_loan_per_book(limit)

@router.get("/{user_id}", response_model=List[LoanResponseModel])
async def get_user_loans(user_id):
    return await view_user_loans(user_id)

@router.put("/{loan_id}/extend", response_model=LoanExtensionResponseModel)
async def loan_extend(loan_id: str, request: LoanExtensionRequestModel):
    print("inside extend route") # debugging log
    return await extend_loan(loan_id, request.extension_days)