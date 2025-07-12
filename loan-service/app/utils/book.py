import requests

async def get_book(book_id):
    url = f"http://localhost:8000/api/v1/books/{book_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


async def save_book(book_id, book):
    book.pop("_id", None)  # Safely remove _id if it exists
    url = f"http://localhost:8000/api/v1/books/{book_id}"
    response = requests.put(url, json=book)
    response.raise_for_status()  # Optional: raises error if response is not 2xx
    return response.json()

#  File "/home/zahin-abdullah-rakin/Documents/6th semester/library_management_api/loan-service/app/services/loan.py", line 3, in <module>
#    from app.utils.book import get_book, save_book
#  File "/home/zahin-abdullah-rakin/Documents/6th semester/library_management_api/loan-service/app/utils/book.py", line 1, in <module>
#    import requests
#ModuleNotFoundError: No module named 'requests'