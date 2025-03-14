from fastapi import FastAPI
from src.books.routes import book_router
from src.errors import register_all_error
from src.middleware import register_middleware
from src.users.routes import auth_router

# from contextlib import asynccontextmanager
from src.reviews.routes import review_router

# from src.db.main import init_db


# @asynccontextmanager
# async def life_span(app: FastAPI):
#     print("Server starts")
#     await init_db()
#     yield
#     print("Server ends")


version = "v1"
app = FastAPI(
    title="Bookly",
    version=version,
    description="REST Api for Book review Service",
    # lifespan=life_span,
)
register_all_error(app)
register_middleware(app)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["BOOKS"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/review", tags=["Review"])
