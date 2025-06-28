import requests

async def get_loan_per_book(limit: int):
    response = requests.get(f"http://localhost:8001/api/v1/loans/count-per-book/{limit}")
    return response.json()

async def get_active_counts(limit: int):
    response = requests.get(f"http://localhost:8001/api/v1/loans/active/count/{limit}")
    return response.json()

async def from_loan_calc_usr_total_borrows(user_id: str) -> int:
    response = requests.get(f"http://localhost:8001/api/v1/loans/{user_id}")
    data = response.json()
    return len(data)

async def get_overdue_loan_count() -> int:
    response = requests.get(f"http://localhost:8001/api/v1/loans/overdue")
    data = response.json()
    return len(data)

async def get_loans_today_count() -> int:
    response = requests.get(f"http://localhost:8001/api/v1/loans/today")
    return response.json()

async def get_returns_today() -> int:
    response = requests.get(f"http://localhost:8001/api/v1/loans/returns/today")
    return response.json()
