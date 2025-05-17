from app.models.loan_extension_models import LoanExtension
from app.models.loan_models import Loan
from app.utils.book import get_book
from app.utils.user import get_user
from app.models.loan_schemas import (
    LoanRequestModel,
    LoanExtensionResponseModel,
    BookMainAttributes,
    LoanResponseModel,
    OverdueLoanResponseModel,
    UserMainAttributes
)


from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from beanie.operators import Set
from beanie.operators import And




async def issue_book(issue_data: LoanRequestModel):
    user = await get_user(issue_data.user_id)   
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    book = await get_book(issue_data.book_id)    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    if book.available_copies < 1:
        raise HTTPException(
            status_code=400,
            detail="No available copies of the book."
        )

    existing_loan = await Loan.find_one(
        Loan.user_id == issue_data.user_id,
        Loan.book_id == issue_data.book_id,
        Loan.status == "ACTIVE"
    )
    if existing_loan:
        raise HTTPException(
            status_code=400,
            detail="User already has an active loan for this book."
        )

    due_date = issue_data.due_date
    if not due_date:
        due_date = datetime.now(timezone.utc) + timedelta(days=14)

    try:
        loan = Loan(
            user_id=str(user.id),
            book_id=str(book.id),
            issue_date=datetime.now(timezone.utc),
            due_date=due_date,
            status="ACTIVE"
        )
        await loan.insert()

        book.available_copies -= 1
        await book.save()

        del loan.extension_count
        del loan.return_date

        return loan

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while issuing the book: {str(e)}"
        )

async def return_book(loan_id: str):
    print(f"inside return_book {loan_id}")  # debugging log
    loan = await Loan.get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan record not found")

    if loan.status == "RETURNED":
        raise HTTPException(
            status_code=400,
            detail="This book has already been returned"
        )

    book = await get_book(loan.book_id) 
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Associated book not found"
        )

    try:
        await loan.update(Set({
            "status": "RETURNED",
            "return_date": datetime.now(timezone.utc)
        }))

        book.available_copies += 1
        await book.save()

        del loan.extension_count

        return loan

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing return: {str(e)}"
        )

async def view_user_loans(user_id):
    user = await get_user(user_id)  
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    loans = await Loan.find(Loan.user_id == user_id).to_list()
    result = []

    for loan in loans:
        book = await get_book(loan.book_id) 
        lrm = LoanResponseModel(
            id = str(loan.id),
            book = BookMainAttributes(
                id = str(book.id),
                title = book.title,
                author = book.author
            ),
            issue_date = loan.issue_date,
            due_date = loan.due_date,
            return_date = loan.return_date,
            status = loan.status
        )
        result.append(lrm)


    return result

async def fetch_overdue_loans():
    print("inside fetch_overdue_loans")
    now = datetime.now(timezone.utc)  # Timezone-aware UTC

    try:
        overdue_loans = await Loan.find(
            And(Loan.due_date < now, Loan.status == "ACTIVE")
        ).to_list()

        results = []
        for loan in overdue_loans:
            # Ensure loan.due_date is timezone-aware (UTC)
            due_date_aware = loan.due_date.replace(tzinfo=timezone.utc) if loan.due_date else None
            days_overdue = (now - due_date_aware).days if due_date_aware else 0

            user = await get_user(loan.user_id)
            book = await get_book(loan.book_id)

            results.append(
                OverdueLoanResponseModel(
                    id=str(loan.id),
                    user=UserMainAttributes(
                        id=str(user.id),
                        name=user.name,
                        email=user.email
                    ),
                    book=BookMainAttributes(
                        id=str(book.id),
                        title=book.title,
                        author=book.author
                    ),
                    issue_date=loan.issue_date,
                    due_date=loan.due_date,
                    days_overdue=days_overdue
                )
            )

        return results
    except Exception as e:
        print("An error occurred while fetching overdue loans:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

async def view_loans():
    try:
        loans = await Loan.find_all().to_list()
        return loans
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

async def extend_loan(loan_id: str, extension_days: int):
    try:
        loan = await Loan.get(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found.")

        if loan.status != "ACTIVE":
            raise HTTPException(status_code=400, detail="Only ACTIVE loans can be extended.")

        # Ensure due_date is timezone-aware (UTC)
        original_due_date = loan.due_date.replace(tzinfo=timezone.utc) if loan.due_date else None
        if not original_due_date:
            raise HTTPException(status_code=400, detail="Loan due date is missing.")

        # Calculate extended due date
        extended_due_date = original_due_date + timedelta(days=extension_days)

        # Update loan
        loan.extension_count += 1

        # Create extension record
        extension = LoanExtension(
            loan_id=str(loan.id),
            extension_days=extension_days,
            original_due_date=original_due_date,
            extended_due_date=extended_due_date,
            extension_no=loan.extension_count
        )
        await extension.insert()

        # Update loan's due date
        loan.due_date = extended_due_date
        await loan.save()

        return LoanExtensionResponseModel(
            id=str(loan.id),
            user_id=loan.user_id,
            book_id=loan.book_id,
            issue_date=loan.issue_date.replace(tzinfo=timezone.utc) if loan.issue_date else None,
            original_due_date=original_due_date,
            extended_due_date=extended_due_date,
            status=loan.status,
            extensions_count=loan.extension_count
        )

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"Error extending loan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error extending loan: {str(e)}")

async def get_active_counts(limit: int):
    return await Loan.aggregate([
        {"$match": {"status": "ACTIVE"}},
        {"$group": {
            "_id": "$user_id",
            "current_borrows": {"$sum": 1},
            "latest_activity": {"$max": "$issue_date"}
        }},
        {"$sort": {"current_borrows": -1, "latest_activity": -1}},
        {"$limit": limit}
    ]).to_list()

async def get_loan_per_book(limit): # {"_id": {book_id}, {borrow_count}}
    pipeline = [
        {"$group": {
            "_id": "$book_id",
            "borrow_count": {"$sum": 1}
        }},
        {"$sort": {"borrow_count": -1}},
        {"$limit": limit}
    ]
    return await Loan.aggregate(pipeline).to_list()

# async def from_loan_calc_usr_total_borrows(user_id_str):
#     await Loan.find(Loan.user_id == user_id_str).count()

# async def get_overdue_loan_count():
#     return await Loan.find({
#         "status": "ACTIVE",
#         "due_date": {"$lt": datetime.now(timezone.utc)}
#     }).count()

async def get_loans_today_count():
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return await Loan.find({
        "status": "ACTIVE",
        "issue_date": {"$gte": today_start}
    }).count()

async def get_returns_today():
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return await Loan.find({
        "status": "RETURNED",
        "return_date": {"$gte": today_start}
    }).count()


