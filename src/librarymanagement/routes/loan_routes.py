from fastapi import APIRouter
from typing import List

from librarymanagement.models.loan_models import Loan
from librarymanagement.models.loan_schemas import (
    OverdueLoanResponseModel,
    LoanReturnRequestModel,
    LoanResponseModel,
    LoanExtensionRequestModel
)
from librarymanagement.models.loan_schemas import LoanExtensionResponseModel
from librarymanagement.models.loan_schemas import LoanRequestModel

from librarymanagement.controllers.loan_controllers import (
    issue_book,
    return_book,
    view_loans,
    view_user_loans,
    fetch_overdue_loans,
    extend_loan
)

router = APIRouter()


@router.post("/add", response_model=Loan)
async def book_issue(issue_data: LoanRequestModel):
    return await issue_book(issue_data)

@router.get("/get", response_model=List[Loan])
async def get_all_loans():
    return await view_loans()

@router.post("/return", response_model=Loan)
async def user_return_book(request: LoanReturnRequestModel):
    return await return_book(request.loan_id)

@router.get("/overdue", response_model=List[OverdueLoanResponseModel])
async def get_overdue_loans():
    print("inside overdue route") # debugging log
    return await  fetch_overdue_loans()

@router.get("/{user_id}", response_model=List[LoanResponseModel])
async def get_user_loans(user_id):
    return await view_user_loans(user_id)

@router.put("/{loan_id}/extend", response_model=LoanExtensionResponseModel)
async def loan_extend(loan_id: str, request: LoanExtensionRequestModel):
    print("inside extend route") # debugging log
    return await extend_loan(loan_id, request.extension_days)