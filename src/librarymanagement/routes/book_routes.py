from fastapi import APIRouter, Query
from typing import List

from librarymanagement.models.book_schemas import UpdateBook, BookAvailability
from librarymanagement.models.book_models import Book
from librarymanagement.controllers.book_controllers import (
    add_book,
    update_book,
    delete_book,
    check_book_availability,
    search_books,
    fetch_book_details
)

router = APIRouter()

@router.post("/")
async def add(book_data:Book):
    return await add_book(book_data)

@router.put("/{book_id}")
async def update(book_id: str, book_data: UpdateBook):
    return await update_book(book_id, book_data)

@router.delete("/{book_id}")
async def delete(book_id:str):
    return await delete_book(book_id)

@router.get("/", response_model=List[Book])
async def get_books(search: str = Query(...)):
    return await search_books(search)

@router.get("/{book_id}", response_model=Book)
async def get_book_details(book_id):
    return await fetch_book_details(book_id)
@router.get("/{book_id}/available", response_model=BookAvailability)
async def check(book_id: str):
    return await check_book_availability(book_id)

