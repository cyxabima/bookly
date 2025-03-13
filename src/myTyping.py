from typing import TypedDict
import uuid


class UserDetails(TypedDict):
    user_uid: uuid.UUID


class TokenDetails(TypedDict):
    user: UserDetails
    exp: int
    jti: str
