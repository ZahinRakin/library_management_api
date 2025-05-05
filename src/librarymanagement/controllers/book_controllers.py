from librarymanagement.models.book_models import Book
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from beanie.operators import Or, RegEx, And

from librarymanagement.models.book_schemas import BookAvailability


async def add_book(book_data):
    try:
        existing_book = await Book.find_one(Book.isbn == book_data.isbn)
        if existing_book:
            raise HTTPException(status_code=400, detail="Book already exists")

        book = await Book(**book_data.model_dump()).insert()
        return {"message": f"book added successfully book_id: {book.id}"}
    except Exception as e:
        print(f"something happened while adding the book.\n{e}")
        raise HTTPException(status_code=400, detail=str(e))

async def update_book(book_id, book_data):
    try:
        book = await Book.get(book_id)
        if not book:
            raise HTTPException(status_code=400, detail="book not found")

        book_data_dict = book_data.model_dump(exclude_unset=True)
        for field, value in book_data_dict.items():
            setattr(book, field, value)

        await book.save()

        return {"message": f"book {book_id} updated successfully.\n"}
    except Exception as e:
        print("something happened while updating the book")
        raise HTTPException(status_code=400, detail=str(e))

async def delete_book(book_id):
    try:
        book = await Book.get(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="book not found")
        await book.delete()
        res = JSONResponse(content={"message": "successfully deleted"}, status_code=200)
        return res
    except Exception as e:
        print(f"something happened while deleting the book.\n{e}")
        raise HTTPException(status_code=400, detail=str(e))

async def fetch_book_details(book_id):
    try:
        book = await Book.get(book_id)
        if not book:
            raise HTTPException(status_code=404, detail={"message": "book not found"})
        del book.created_at
        del book.updated_at
        return book
    except Exception as e:
        print(f"something happened while fetching the book.\n{e}")
        raise HTTPException(status_code=400, detail=str(e))

async def check_book_availability(book_id):
    try:
        book = await Book.get(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="book not found")
        if book.available_copies <= 0:
            raise HTTPException(status_code=400, detail=f"{book.title} isn't available")
        return BookAvailability(available_copies=book.available_copies)
    except Exception as e:
        print(f"something happened while checking availability.\n{e}")
        raise HTTPException(status_code=400, detail=str(e))

async def search_books(search_key) -> List[Book]:
    print(f"{search_key} is searching...")  # debugging log
    try:
        words = search_key.strip().split()
        query = And(*[
            Or(
                RegEx(Book.title, f".*{word}.*", options="i"),
                RegEx(Book.author, f".*{word}.*", options="i"),
                RegEx(Book.genre, f".*{word}.*", options="i"),
            )
            for word in words
        ])
        books = await Book.find(query).to_list()
        return books
    except Exception as e:
        print(f"something happened while fetching the books.\n{e}")
        raise HTTPException(status_code=400, detail=str(e))


async def get_book(book_id) -> Book:
    return await Book.get(book_id)


async def get_total_book_count():
    return await Book.find({}).count()


async def get_available_book_count():
    return await Book.find({"available_copies": {"$gt": 0}}).count()
