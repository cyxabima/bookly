from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.service import BookService
from .schemas import Book, BookCreateModel, BookUpdateModel
from src.db.main import get_db_session


book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_db_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreateModel,
    session: AsyncSession = Depends(get_db_session),
):
    new_book = await book_service.create_book(book, session)
    return new_book


@book_router.get("/{book_uid}", response_model=Book)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_db_session),
):
    book = await book_service.get_book(book_uid, session)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return book


@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(
    book_uid: str,
    updatedBook: BookUpdateModel,
    session: AsyncSession = Depends(get_db_session),
):
    book = await book_service.update_book(book_uid, updatedBook, session)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return book


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_db_session)):
    book = await book_service.delete_book(book_uid, session)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return book
