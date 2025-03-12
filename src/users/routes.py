# from fastapi import

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from src.db.redis import add_jti_to_block_list
from src.users.service import UserService
from .schemas import UserCreateModel, UserLoginModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_db_session
from . import utils
from .dependency import AccessTokenBearer, RefreshTokenBearer


auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_db_session)
):
    user_exist = await user_service.user_exits(user_data.email, session)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already exits"
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_db_session)
):
    data = await user_service.login_user(login_data, session)

    if data == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User With this email does not exit",
        )

    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
        )

    return data


@auth_router.get("/refresh_token")
async def get_new_access_token(
    token_details: dict = Depends(RefreshTokenBearer()),
    #  here calling the class to make object
):

    expiry_time_stamp = token_details["exp"]
    if not datetime.fromtimestamp(expiry_time_stamp) > datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expire Token"
        )
    new_access_token = utils.generateAccessToken(user_data=token_details["user"])

    return {"content": {"access_token": new_access_token}}
    # or we could return


@auth_router.get("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]

    await add_jti_to_block_list(jti)

    return {"message": "User logout Successfully"}
