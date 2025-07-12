import requests

async def get_user(user_id):
    url = f"http://user-service:8003/api/v1/users/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json()) # log
        return response.json()
    else:
        response.raise_for_status()
