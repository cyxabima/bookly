# alternative to oauth2PasswordBearer and it is general
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from src.db.redis import token_in_block_list
from src.users.utils import decode_token
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_db_session
from .service import UserService

user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(
        self,
        auto_error=True,
    ):
        super().__init__(
            auto_error=auto_error,
        )

    async def __call__(self, request: Request):
        creds = await super().__call__(request)

        if creds is None or creds.credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing Authorization token",
            )

        token = creds.credentials

        if not self.is_token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expire token"
            )

        token_data = decode_token(token)

        if await token_in_block_list(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token is revoked"
            )

        self.verify_token_data(token_data)
        return token_data

    def is_token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return True if token_data else False

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in child class")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data):
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Token is required not refresh token ",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data):
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh Token is required",
            )


async def get_logged_user(
    token_data: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_db_session),
):
    email = token_data["user"]["email"]
    user = await user_service.get_user_by_email(email, session)
    return user
