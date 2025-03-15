# from fastapi import

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from src.config import Config
from src.db.redis import add_jti_to_block_list
from src.users.service import UserService
from .schemas import (
    EmailModel,
    ResetPasswordEmailModel,
    ResetPasswordModel,
    User,
    UserCreateModel,
    UserLoginModel,
    UserWithBooksModel,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_db_session
from . import utils
from .dependency import AccessTokenBearer, RefreshTokenBearer, get_logged_user
from src.errors import InvalidCredentials, InvalidToken, UserAlreadyExits, UserNotFound
from src.email import mail, create_mail


auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/send_email")
async def send_mail(emails_data: EmailModel):
    emails = emails_data.address
    html = "<h1>WELCOME TO APP</h1>"
    message = create_mail(recipients=emails, subject="Welcome", body=html)

    await mail.send_message(message=message)

    return {"Message": "email send successfully"}


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_db_session)
):
    user_exist = await user_service.user_exits(user_data.email, session)

    if user_exist:
        raise UserAlreadyExits()

    new_user = await user_service.create_user(user_data, session)

    # email sending logic
    token = utils.create_url_safe_token({"email": user_data.email})

    link = f"http://{Config.domain}/api/v1/auth/verify/{token}"

    html = f"""<h1>Welcome to Bookly</h1> <p>Plz click this <a href="{link}">link<a/> to verify your account</p>"""
    message = create_mail(
        recipients=[user_data.email], subject="Verify Your Bookly Account", body=html
    )
    await mail.send_message(message)
    return new_user


@auth_router.get("/verify/{token}")
async def verify_user_email(
    token: str, session: AsyncSession = Depends(get_db_session)
):
    token_data = utils.verify_url_safe_token(token)
    email = token_data.get("email")

    if not email:
        raise InvalidToken()

    user = await user_service.get_user_by_email(email, session)

    if not user:
        raise UserNotFound()

    await user_service.update_user(user, {"is_verified": True}, session)
    return JSONResponse(
        content={"message": "Account Verified successFully"},
        status_code=status.HTTP_200_OK,
    )


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


@auth_router.post("/reset-password-email")
async def reset_password_email(
    email_data: ResetPasswordEmailModel, session: AsyncSession = Depends(get_db_session)
):

    user = await user_service.get_user_by_email(email_data.email, session)
    if not user:
        raise UserNotFound()

    # email sending logic
    token = utils.create_url_safe_token({"email": email_data.email})

    link = f"http://{Config.domain}/api/v1/auth/reset-password/{token}"

    html = f"""<h1>Reset Your Password</h1> <p>Plz click this <a href="{link}">link<a/> to reset your password </p>"""
    message = create_mail(
        recipients=[email_data.email],
        subject="Alert Password Reset! of your Bookly Account",
        body=html,
    )
    await mail.send_message(message)
    return JSONResponse(
        content="Check your email to reset your password",
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/reset-password/{token}")
async def reset_password(
    token: str,
    password: ResetPasswordModel,
    session: AsyncSession = Depends(get_db_session),
):
    token_data = utils.verify_url_safe_token(token)
    email = token_data.get("email")

    if not email:
        raise InvalidToken()

    user = await user_service.get_user_by_email(email, session)

    if not user:
        raise UserNotFound()

    new_password = password.new_password
    confirm_password = password.confirm_password

    if new_password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="password and confirm password does not match ",
        )
    hashed_password = utils.hash_password(new_password)
    await user_service.update_user(user, {"password_hash": hashed_password}, session)
    return JSONResponse(
        content={"message": "Password Reset Successfully"},
        status_code=status.HTTP_200_OK,
    )


@auth_router.get("/{email}")
async def get_user_by_email(
    email: str, session: AsyncSession = Depends(get_db_session)
):
    user = await user_service.get_user_by_email(email, session)
    return user
