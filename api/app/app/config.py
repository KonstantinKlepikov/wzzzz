import toml
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from typing import Optional, Type
from app.schemas.scheme_error import (
    HttpErrorMessage,
    HttpError400,
    HttpError404,
    HttpError409,
    HttpError429,
        )


ErrorType = dict[int, dict[str, Type[HttpErrorMessage]]]
poetry_data = toml.load('pyproject.toml')['tool']['poetry']


class Settings(BaseSettings):
    # api vars
    API_V1: str = "/api/v1"

    # db settings
    MONGODB_URL: str
    DB_NAME: str
    ACCES_TOKEN_EXPIRES_MINUTES: Optional[int] = None
    EXPIRED_BY_SECONDS: int = 5256000
    REDIS_URL: str = None

    # hhru settings
    HHRU_API_TOKEN: SecretStr = None
    HHRU_CLIENT_EMAIL: Optional[str] = None

    # def settings
    TEST_MONGODB_URL: Optional[str] = None

    # open-api settings
    title: str = poetry_data['name']
    descriprion: str = poetry_data['description']
    version: str = poetry_data['version']
    openapi_tags: list = [
        {
            "name": "users",
            "description": "Users api",
        },
        {
            "name": "templates",
            "description": "Search templates",
        },
        {
            "name": "vacancies",
            "description": "Transformed vacancies data from hh.ru",
        },
    ]
    ERRORS: ErrorType = {
        400: {'model': HttpError400},
        404: {'model': HttpError404},
        409: {'model': HttpError409},
        429: {'model': HttpError429}
            }

    SIZE_POOL_HTTP: int = 100
    TIMEOUT_AIOHTTP: int = 2
    QUERY_SLEEP: float = 0.05

    def get_hhru_auth(self):
        """Get auth headers for api query
        """
        return {
            'Authorization': f"Bearer {self.HHRU_API_TOKEN.get_secret_value()}",
            'User-Agent': f'wzzzz/1.0 ({self.HHRU_CLIENT_EMAIL})',
                }


settings = Settings()
