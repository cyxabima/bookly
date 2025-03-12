from datetime import datetime, timedelta
import uuid
from passlib.context import CryptContext
import jwt
import logging
from src.config import Config

passwd_context = CryptContext(schemes=["bcrypt"])
default_time_expiry = 60


def hash_password(password):
    return passwd_context.hash(password)


def verify_password(password, hashed):
    return passwd_context.verify(password, hashed)


def generateAccessToken(
    user_data,
    expiry: timedelta = timedelta(minutes=default_time_expiry),
    refresh: bool = False,
):
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.now() + expiry
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=Config.secret_key, algorithm=Config.algorithm
    )
    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            token, key=Config.secret_key, algorithms=Config.algorithm
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return {}
