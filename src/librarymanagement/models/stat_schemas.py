from pydantic import BaseModel


class MostActiveUserResponseModel(BaseModel):
    user_id: str
    name: str
    books_borrowed: int
    current_borrows: int


class PopularBookResponseModel(BaseModel):
    book_id: str
    title: str
    author: str
    borrow_count: int
