# from fastapi import

from datetime import datetime
from fastapi import APIRouter, Depends, status
from src.db.redis import add_jti_to_block_list
from src.users.service import UserService
from .schemas import User, UserCreateModel, UserLoginModel, UserWithBooksModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_db_session
from . import utils
from .dependency import AccessTokenBearer, RefreshTokenBearer, get_logged_user
from src.errors import InvalidCredentials, InvalidToken, UserAlreadyExits, UserNotFound


auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_db_session)
):
    user_exist = await user_service.user_exits(user_data.email, session)

    if user_exist:
        raise UserAlreadyExits()

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_db_session)
):
    data = await user_service.login_user(login_data, session)

    if data == -1:
        raise UserNotFound()

    if not data:
        raise InvalidCredentials()
    return data


@auth_router.get("/refresh_token")
async def get_new_access_token(
    token_details: dict = Depends(RefreshTokenBearer()),
    #  here calling the class to make object
):

    expiry_time_stamp = token_details["exp"]
    if not datetime.fromtimestamp(expiry_time_stamp) > datetime.now():
        raise InvalidToken()
    new_access_token = utils.generateAccessToken(user_data=token_details["user"])

    return {"content": {"access_token": new_access_token}}
    # or we could return


@auth_router.get("/me", response_model=UserWithBooksModel)
async def get_user_details(user_details: User = Depends(get_logged_user)):
    return user_details


@auth_router.get("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]

    await add_jti_to_block_list(jti)

    return {"message": "User logout Successfully"}


@auth_router.get("/{email}")
async def get_user_by_email(
    email: str, session: AsyncSession = Depends(get_db_session)
):
    user = await user_service.get_user_by_email(email, session)
    return user
