from typing import List

from fastapi import APIRouter

from app.models.stat_schemas import MostActiveUserResponseModel
from app.models.overview_schemas import OverviewModel
from app.models.stat_schemas import PopularBookResponseModel
from app.services.stat import (
    fetch_popular_books,
    fetch_active_users,
    calculate_overview
)

router = APIRouter()

@router.get("/books/popular", response_model=List[PopularBookResponseModel])
async def get_popular_books():
    return await fetch_popular_books(limit=3)

@router.get("/users/active", response_model=List[MostActiveUserResponseModel])
async def get_most_active_users():
    return await fetch_active_users()

@router.get("/overview", response_model=OverviewModel)
async def get_system_overview():
    print("Fetching system overview") # debugging log
    return await calculate_overview()