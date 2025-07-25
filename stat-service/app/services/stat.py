from typing import List
from beanie.operators import In
from beanie import PydanticObjectId
from fastapi import HTTPException


from app.models.overview_schemas import OverviewModel
from app.models.stat_schemas import PopularBookResponseModel, MostActiveUserResponseModel
from ..utils.book import get_book, get_total_book_count, get_available_book_count
from ..utils.loan import (
    get_loan_per_book, 
    get_active_counts, 
    from_loan_calc_usr_total_borrows, 
    get_overdue_loan_count, # prb
    get_loans_today_count,
    get_returns_today
)
from ..utils.user import get_user, get_total_user_count


async def fetch_popular_books(limit: int = 10) -> List[PopularBookResponseModel]:
    try:
        loan_counts = await get_loan_per_book(limit)
        book_ids = [PydanticObjectId(item["_id"]) for item in loan_counts]
        books = [await get_book(id) for id in book_ids]
        book_map = {str(book["_id"]): book for book in books}

        return [
            PopularBookResponseModel(
                book_id=item["_id"],
                title=book_map[item["_id"]]["title"],
                author=book_map[item["_id"]]["author"],
                borrow_count=item["borrow_count"]
            )
            for item in loan_counts
            if item["_id"] in book_map
        ]

    except Exception as e:
        print(f"Error fetching popular books: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch popular books")

async def fetch_active_users(limit: int = 10) -> List[MostActiveUserResponseModel]:
    try:
        active_counts = await get_active_counts(limit)

        if not active_counts:
            return []

        result = []

        for item in active_counts:
            user_id_str = item["_id"]
            try:
                user = await get_user(user_id_str)
            except Exception:
                continue 

            if user:
                total_borrows = await from_loan_calc_usr_total_borrows(str(user["_id"]))
                result.append(MostActiveUserResponseModel(
                    user_id=user_id_str,
                    name=user["name"],
                    books_borrowed=total_borrows,
                    current_borrows=item["current_borrows"]
                ))

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def calculate_overview() -> OverviewModel:
    total_books = await get_total_book_count()
    total_users = await get_total_user_count()
    books_available = await get_available_book_count()

    overdue_loans = await get_overdue_loan_count()

    loans_today = await get_loans_today_count()

    returns_today = await get_returns_today()

    return OverviewModel(
        total_books=total_books,
        total_users=total_users,
        books_available=books_available,
        overdue_loans=overdue_loans,
        loans_today=loans_today,
        returns_today=returns_today
    )

