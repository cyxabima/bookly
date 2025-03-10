from typing import List
from fastapi import APIRouter, HTTPException, status
from .data import books
from .schemas import Book, BookUpdate


book_router = APIRouter()


# | Get all books|
@book_router.get("/", response_model=List[Book])
async def get_all_books():
    return books


@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book


@book_router.get("/{id}", response_model=Book)
async def get_book(id: int):
    for book in books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@book_router.patch("/{id}")
async def update_book(id: int, updatedBook: BookUpdate):
    for book in books:
        if book["id"] == id:
            book["title"] = updatedBook.title
            book["author"] = updatedBook.author
            book["publisher"] = updatedBook.publisher
            book["page_count"] = updatedBook.page_count
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@book_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int):
    for book in books:
        if book["id"] == id:
            books.remove(book)
            return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
