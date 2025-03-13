from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src import myTyping
from src.books.service import BookService
from .schemas import Book, BookCreateModel, BookUpdateModel
from src.db.main import get_db_session
from src.users.dependency import AccessTokenBearer, RoleChecker


book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
# we can also inject dependency in router.get or any http method if we do not want to use its value in function
role_checker = Depends(RoleChecker(["admin", "user"]))


@book_router.get("/", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_db_session),
    user_details=Depends(access_token_bearer),
):
    print(user_details)
    books = await book_service.get_all_books(session)
    return books


@book_router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    dependencies=[role_checker],
)
async def create_book(
    book: BookCreateModel,
    session: AsyncSession = Depends(get_db_session),
    token_details: myTyping.TokenDetails = Depends(access_token_bearer),
):
    user_uid = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(book, user_uid, session)
    return new_book


@book_router.get("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_db_session),
    token_details=Depends(access_token_bearer),
):
    book = await book_service.get_book(book_uid, session)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return book


@book_router.patch("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def update_book(
    book_uid: str,
    updatedBook: BookUpdateModel,
    session: AsyncSession = Depends(get_db_session),
    token_details=Depends(access_token_bearer),
):
    book = await book_service.update_book(book_uid, updatedBook, session)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return book


@book_router.delete(
    "/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_db_session),
    token_details=Depends(access_token_bearer),
):
    book = await book_service.delete_book(book_uid, session)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return book
