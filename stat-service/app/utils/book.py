import requests

async def get_book(book_id):
    response = requests.get(f"http://book-service:8000/api/v1/books/{book_id}")
    return response.json()

async def get_total_book_count() -> int:
    response = requests.get(f"http://book-service:8000/api/v1/books")
    data = response.json()
    return len(data)

async def get_available_book_count() -> int:
    response = requests.get(f"http://book-service:8000/api/v1/books/available/count")
    data = response.json()
    return data

async def save_book(book_id, book):
    book.pop("_id", None)  # Safely remove _id if it exists
    url = f"http://book-service:8000/api/v1/books/{book_id}"
    response = requests.put(url, json=book)
    response.raise_for_status()  # Optional: raises error if response is not 2xx
    return response.json()
