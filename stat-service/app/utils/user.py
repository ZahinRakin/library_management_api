import httpx


async def get_user(user_id):
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8003/api/v1/users/{user_id}")
  return response

async def get_total_user_count() -> int:
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8003/api/v1/users/count")
  return response