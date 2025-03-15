from typing import List
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from .config import Config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

conf = ConnectionConfig(
    MAIL_USERNAME=Config.mail_username,
    MAIL_PASSWORD=Config.mail_password,
    MAIL_FROM=Config.mail_from,
    MAIL_PORT=Config.mail_port,
    MAIL_SERVER=Config.mail_server,
    MAIL_FROM_NAME=Config.mail_from_name,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR, "templates"),
)

mail = FastMail(conf)


def create_mail(recipients: List[str], subject: str, body: str):
    return MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )
