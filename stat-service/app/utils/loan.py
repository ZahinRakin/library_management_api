import httpx

async def get_loan_per_book(limit: int):
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8001/api/v1/loans/count-per-book/{limit}")
  return response


async def get_active_counts(limit: int):
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8001/api/v1/loans/active/users/{limit}")
  return response

async def from_loan_calc_usr_total_borrows(user_id: str) -> int:
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8001/api/v1/loans/{user_id}")
  return len(response)


async def get_overdue_loan_count(user_id: str) -> int:
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8001/api/v1/loans/overdue")
  return len(response) 

async def get_loans_today_count() -> int:
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8001/api/v1/loans/today")
  return response

async def get_returns_today() -> int:
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8001/api/v1/loans/returns/today")
  return response