from pydantic import BaseModel, EmailStr
from typing import Optional

class UpdateProfile(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    avatar: Optional[str] = None
    cover_image: Optional[str] = None