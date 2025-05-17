import httpx


async def get_book(book_id):
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8000/api/v1/books/{book_id}")
  return response


async def get_total_book_count() -> int:
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8000/api/v1/books")
  return len(response)

async def get_available_book_count() -> int:
  async with httpx.AsyncClient() as client:
    response = await client.get(f"http://localhost:8000/api/v1/books/available/count")
  return len(response)
