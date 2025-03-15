from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_uri: str
    secret_key: str
    algorithm: str
    redis_host: str
    redis_port: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    mail_username: str
    mail_password: SecretStr
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    use_credentials: bool = True
    validate_certs: bool = True
    domain: str


Config = Settings()
