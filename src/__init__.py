from fastapi import FastAPI
from src.books.routes import book_router

version = "v1"
app = FastAPI(version=version, description="REST Api for Book review Service")

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["BOOKS"])
