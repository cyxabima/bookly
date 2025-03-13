from pydantic import BaseModel
from datetime import datetime

import uuid
from typing import Optional


class Review(BaseModel):
    uid: uuid.UUID

    rating: int
    review: str

    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    rating: int
    review: str
