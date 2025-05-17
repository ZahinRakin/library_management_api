from pydantic import EmailStr, Field
from typing import Optional
from beanie import Document

class User(Document):
    name: str
    email: EmailStr
    password: str
    role: str
    avatar: Optional[str] = None
    cover_image: Optional[str] = None

    class Settings:
        name = "User"
