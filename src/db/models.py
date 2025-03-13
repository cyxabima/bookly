from typing import Optional
import uuid
from sqlmodel import Column, Field, Relationship, SQLModel
from datetime import date, datetime
import sqlalchemy.dialects.postgresql as pg
from typing import List


class Book(SQLModel, table=True):
    # __tablename__ = "books" sql model does not support __tablename__ instead better it will derive from class name

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True),
        default_factory=uuid.uuid4,
    )
    title: str
    author: str
    user_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="user.uid", unique=False
    )
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now(), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now(), nullable=False)
    )

    user: Optional["User"] = Relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"<Book {self.title}>"


class User(SQLModel, table=True):
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True),
        default_factory=uuid.uuid4,
    )
    user_name: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, server_default="user", nullable=False)
    )
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"<User {self.user_name}>"
