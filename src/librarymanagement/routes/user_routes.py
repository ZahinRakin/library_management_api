from fastapi import APIRouter, Body
from librarymanagement.models.user_models import User
from librarymanagement.models.user_schemas import UpdateProfile

from librarymanagement.controllers.user_controllers import (
    register_user,
    update_user,
    fetch_user_info,
    delete_user
)

router = APIRouter()

@router.post("/")
async def register(user_data: User):
    return await register_user(user_data)

@router.put("/{user_id}")
async def update_profile(user_id: str, updated_data: UpdateProfile):
    return await update_user(user_id, updated_data)

@router.delete("/{user_id}")
async def delete_user_from_db(user_id):
    return await delete_user(user_id)

@router.get("/{user_id}", response_model=User)
async def get_user_info(user_id: str):
    print("here inside fetch profile")      # debugging log
    return await fetch_user_info(user_id)