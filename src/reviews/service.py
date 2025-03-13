from sqlmodel.ext.asyncio.session import AsyncSession
from src.users.service import UserService
from src.books.service import BookService
from .schemas import ReviewCreateModel
from src.db.models import Review

book_service = BookService()
user_service = UserService()


class ReviewService:
    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        book = await book_service.get_book(book_uid, session)
        user = await user_service.get_user_by_email(user_email, session)

        new_review = Review(**review_data.model_dump())
        new_review.user = user
        new_review.book = book

        session.add(new_review)
        await session.commit()
        return new_review
