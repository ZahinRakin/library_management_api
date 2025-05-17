import httpx


async def get_user(user_id):
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8003/api/v1/users/{user_id}")