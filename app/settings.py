"""Module containing app settings."""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+mysqlconnector://user:password@db:3306/fastapi_db"
    SECRET_KEY: str = "SUPERSECRETJWTKEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    class Config:
        env_file = ".env"

settings = Settings()
