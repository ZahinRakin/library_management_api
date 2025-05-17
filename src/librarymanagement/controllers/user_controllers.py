from fastapi import HTTPException

from librarymanagement.models.user_models import User


async def register_user(user_data):
    try:
        existing_user = await User.find_one(User.email == user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = await User(**user_data.model_dump()).insert()
        return {"message": f"user creation successful user_id: {user.id}"}
    except Exception as e:
        print(f"something happened while registering user. \n {e}")
        raise HTTPException(status_code=400, detail=str(e))

async def update_user(user_id, updated_data):
    try:
        user = await User.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail={"message": "user not found"})
        await user.set(updated_data.model_dump(exclude_unset=True))
        return {"message": f"user: {user_id} has been updated successfully"}
    except Exception as e:
        print(f"something happened while updating the user profile.\n{e}")
        raise HTTPException(status_code=400, detail=str(e))

async def delete_user(user_id):
    try:
        user = await User.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail={"message": "user not found"})
        await user.delete()
        return {"message": f"user: {user_id} has been deleted successfully"}
    except Exception as e:
        print(f"something happened while updating the user profile.\n{e}")
        raise HTTPException(status_code=400, detail=str(e))


async def fetch_user_info(user_id):
    try:
        user = await User.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail={"message": "user not found"})
        return user
    except Exception as e:
        print(f"something happened while viewing profile.\n{e}")
        raise HTTPException(status_code=400, detail=str(e))


async def get_user(user_id):
    return await User.get(user_id)


async def get_total_user_count():
    return await User.find({}).count()


