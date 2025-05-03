import asyncio
import traceback

from fastapi import HTTPException

from librarymanagement.models.user_models import User
from librarymanagement.models.book_models import Book
from librarymanagement.models.loan_models import Loan
from librarymanagement.models.overview_schemas import OverviewModel
from librarymanagement.models.stat_schemas import PopularBookResponseModel, MostActiveUserResponseModel

from datetime import datetime, timezone
from typing import List
from beanie.operators import In
from beanie import PydanticObjectId


async def fetch_popular_books(limit: int = 10) -> List[PopularBookResponseModel]:
    try:
        # 1. Aggregation pipeline to count loans per book (Beanie style)
        pipeline = [
            {"$group": {
                "_id": "$book_id",
                "borrow_count": {"$sum": 1}
            }},
            {"$sort": {"borrow_count": -1}},
            {"$limit": limit}
        ]
        loan_counts = await Loan.aggregate(pipeline).to_list()

        # 2. Batch fetch books using Beanie's In operator
        book_ids = [PydanticObjectId(item["_id"]) for item in loan_counts]
        books = await Book.find(In(Book.id, book_ids)).to_list()

        # Create lookup dictionary (convert ID to string for consistency)
        book_map = {str(book.id): book for book in books}

        # 3. Build response maintaining sort order
        return [
            PopularBookResponseModel(
                book_id=item["_id"],
                title=book_map[item["_id"]].title,
                author=book_map[item["_id"]].author,
                borrow_count=item["borrow_count"]
            )
            for item in loan_counts
            if item["_id"] in book_map  # Handle potential data inconsistencies
        ]

    except Exception as e:
        print(f"Error fetching popular books: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch popular books")

async def fetch_active_users(limit: int = 10) -> List[MostActiveUserResponseModel]:
    try:
        active_counts = await Loan.aggregate([
            {"$match": {"status": "ACTIVE"}},
            {"$group": {
                "_id": "$user_id",
                "current_borrows": {"$sum": 1},
                "latest_activity": {"$max": "$issue_date"}
            }},
            {"$sort": {"current_borrows": -1, "latest_activity": -1}},
            {"$limit": limit}
        ]).to_list()

        if not active_counts:
            return []

        result = []

        for item in active_counts:
            user_id_str = item["_id"]
            try:
                user = await User.get(user_id_str)
            except Exception:
                continue  # skip if conversion or fetch fails

            if user:
                total_borrows = await Loan.find(Loan.user_id == user_id_str).count()
                result.append(MostActiveUserResponseModel(
                    user_id=user_id_str,
                    name=user.name,
                    books_borrowed=total_borrows,
                    current_borrows=item["current_borrows"]
                ))

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def calculate_overview() -> OverviewModel:
    now = datetime.now(timezone.utc)

    # Use find().count() instead of count_documents()
    total_books = await Book.find({}).count()
    total_users = await User.find({}).count()
    books_available = await Book.find({"available_copies": {"$gt": 0}}).count()

    overdue_loans = await Loan.find({
        "status": "ACTIVE",
        "due_date": {"$lt": now}
    }).count()

    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    loans_today = await Loan.find({
        "status": "ACTIVE",
        "issue_date": {"$gte": today_start}
    }).count()

    returns_today = await Loan.find({
        "status": "RETURNED",
        "return_date": {"$gte": today_start}
    }).count()

    return OverviewModel(
        total_books=total_books,
        total_users=total_users,
        books_available=books_available,
        overdue_loans=overdue_loans,
        loans_today=loans_today,
        returns_today=returns_today
    )

