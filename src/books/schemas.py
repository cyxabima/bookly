from datetime import date, datetime
from typing import List
from pydantic import BaseModel
import uuid

from src.db.models import Review, Tag


class Book(BaseModel):
    uid: uuid.UUID
    user_uid: uuid.UUID | None
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime


class BookDetailsModel(Book):
    reviews: List[Review]
    tags: List[Tag]
    # here Review is sqlModel if it was sqlAlChemy we have to Schema with class config from_attribute  True


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
