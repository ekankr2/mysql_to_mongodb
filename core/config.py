import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    MYSQL_HOST: str = os.getenv('MYSQL_HOST')
    MYSQL_DATABASE: str = os.getenv('MYSQL_DATABASE')
    MYSQL_USER: str = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD: str = os.getenv('MYSQL_PASSWORD')
    MONGO_URI: str = os.getenv('MONGO_URI')

    class Config:
        env_file = ".env"


settings = Settings()