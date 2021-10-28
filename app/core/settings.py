import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Class with validating project settings"""

    # Project info
    PROJECT_NAME: str = 'Node tree app'

    # DB
    DB_USER = os.getenv('DB_USER', 'nta')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'nta')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 5432)
    DB_NAME = os.getenv('DB_NAME', 'nta_db')
    DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    class Config:
        case_sensitive = True


settings = Settings()
