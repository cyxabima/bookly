from datetime import timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from . import utils

from src.users.models import User
from src.users.schemas import UserCreateModel, UserLoginModel


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def user_exits(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)
        new_user.password_hash = utils.hash_password(user_data_dict["password"])

        session.add(new_user)
        await session.commit()

        return new_user

    async def login_user(self, login_data: UserLoginModel, session: AsyncSession):
        user = await self.get_user_by_email(login_data.email, session)

        if user is None:
            return -1

        correct_password = utils.verify_password(
            login_data.password, user.password_hash
        )

        if not correct_password:
            return 0

        access_token = utils.generateAccessToken(
            user_data={
                "email": user.email,
                "user_uid": str(user.uid),
            }
        )

        refresh_token = utils.generateAccessToken(
            user_data={
                "email": user.email,
                "user_uid": str(user.uid),
            },
            refresh=True,
            expiry=timedelta(days=2),
        )

        return {
            "content": {
                "message": "login Successfully",
                "user": {"email": user.email, "uid": user.uid},
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        }
