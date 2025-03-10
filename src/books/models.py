import uuid
from sqlmodel import Column, Field, SQLModel
from datetime import date, datetime
import sqlalchemy.dialects.postgresql as pg


class Book(SQLModel, table=True):
    # __tablename__ = "books" sql model doesnot support __tablename__ instead better it will derive from class name

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4()
        )
    )
    title: str
    author: str
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

    def __repr__(self) -> str:
        return f"<Book {self.title}>"
