import toml
from pydantic import BaseSettings, SecretStr
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
    api_v1_str: str = "/api/v1"

    # db settings
    mongodb_url: str
    db_name: str
    test_mongodb_url: Optional[str] = None
    access_token_expires_minites: Optional[int] = None
    expyred_by_seconds: int = 5256000
    CELERY_BROKER_URL_DEV: Optional[str] = None
    REDIS_URL_DEV: str = None

    # hhru settings
    HHRU_API_TOKEN: SecretStr = None
    HHRU_CLIENT_EMAIL: Optional[str] = None

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

    size_pool_http: int = 100
    timeout_aiohttp: int = 2
    query_sleep: float = 0.05


    def get_hhru_auth(self):
        return {
            'Authorization': f"Bearer {self.HHRU_API_TOKEN.get_secret_value()}",
            'User-Agent': f'wzzzz/1.0 ({self.HHRU_CLIENT_EMAIL})',
                }


settings = Settings()
