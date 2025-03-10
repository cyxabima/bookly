from typing import List
from fastapi import FastAPI, HTTPException, status
from data import books
from pydantic import BaseModel

app = FastAPI()


# schema
class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdate(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


@app.get("/", response_model=List[Book])
async def root():
    return {"Message": "Hello, Welcome to Bookly"}


# | Get all books|
@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books


@app.post("/book", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book


@app.get("/book/{id}", response_model=Book)
async def get_book(id: int):
    for book in books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.patch("/book/{id}")
async def update_book(id: int, updatedBook: BookUpdate):
    for book in books:
        if book["id"] == id:
            book["title"] = updatedBook.title
            book["author"] = updatedBook.author
            book["publisher"] = updatedBook.publisher
            book["page_count"] = updatedBook.page_count
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int):
    for book in books:
        if book["id"] == id:
            books.remove(book)
            return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
