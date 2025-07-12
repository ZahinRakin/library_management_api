import requests

async def get_user(user_id):
    response = requests.get(f"http://user-service:8003/api/v1/users/{user_id}")
    return response.json()

async def get_total_user_count() -> int:
    response = requests.get(f"http://user-service:8003/api/v1/users/count")
    return response.json()
