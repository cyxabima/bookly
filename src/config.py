from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_uri: str
    secret_key: str
    algorithm: str
    redis_host: str
    redis_port: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
