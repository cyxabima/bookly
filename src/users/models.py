from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, SQLModel, Field
import uuid


class User(SQLModel, table=True):
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_name: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self) -> str:
        return f"<User {self.user_name}>"
