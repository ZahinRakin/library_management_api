from fastapi import APIRouter

from app.models.user_models import User
from app.models.user_schemas import UpdateProfile

from app.services.users import (
    register_user,
    update_user,
    fetch_user_info,
    delete_user,
    get_total_user_count
)

router = APIRouter()

@router.post("/")
async def register(user_data: User):
    return await register_user(user_data)

@router.get("/count", response_model=int)
async def get_user_count():
    return await get_total_user_count()

@router.get("/{user_id}", response_model=User)
async def get_user_info(user_id: str):
    print("here inside fetch profile")      # debugging log
    return await fetch_user_info(user_id)

@router.put("/{user_id}")
async def update_profile(user_id: str, updated_data: UpdateProfile):
    return await update_user(user_id, updated_data)

@router.delete("/{user_id}")
async def delete_user_from_db(user_id):
    return await delete_user(user_id)


