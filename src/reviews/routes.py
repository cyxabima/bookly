from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_db_session
from src.db.models import User
from src.reviews.schemas import ReviewCreateModel
from src.users.dependency import get_logged_user
from .service import ReviewService

review_router = APIRouter()

review_service = ReviewService()


@review_router.post("/book/{book_uid}")
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    user_details: User = Depends(get_logged_user),
    session: AsyncSession = Depends(get_db_session),
):
    review = await review_service.add_review_to_book(
        user_details.email, book_uid, review_data, session
    )
    return review
