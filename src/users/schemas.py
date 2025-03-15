from typing import List
from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from src.books.schemas import Book


class User(BaseModel):
    uid: uuid.UUID
    user_name: str
    email: str
    # password: str = Field(exclude=True)
    first_name: str
    last_name: str
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime


class UserWithBooksModel(User):
    books: List[Book]


class UserCreateModel(BaseModel):
    user_name: str = Field(max_length=12)
    email: str = Field(max_length=42)
    first_name: str
    last_name: str
    password: str = Field(min_length=6)


class UserLoginModel(BaseModel):
    user_name: str = Field(max_length=12)
    email: str = Field(max_length=42)
    password: str = Field(min_length=6)


class EmailModel(BaseModel):
    address: List[str]


class ResetPasswordEmailModel(BaseModel):
    email: str


class ResetPasswordModel(BaseModel):
    new_password: str
    confirm_password: str
