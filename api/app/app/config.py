import toml
from pydantic import BaseSettings
from typing import Optional, Type
from app.schemas.scheme_error import (
    HttpErrorMessage,
    HttpError400,
    HttpError409
        )


ErrorType = dict[int, dict[str, Type[HttpErrorMessage]]]
poetry_data = toml.load('pyproject.toml')['tool']['poetry']


class Settings(BaseSettings):
    # api vars
    api_v1_str: str = "/api/v1"

    # db settings
    mongodb_url: str
    db_name: str = 'prod-db'
    test_mongodb_url: Optional[str] = None
    access_token_expires_minites: Optional[int] = None

    # open-api settings
    title: str = poetry_data['name']
    descriprion: str = poetry_data['description']
    version: str = poetry_data['version']
    openapi_tags: list = [
        {
            "name": "user",
            "description": "Users api",
        },
        {
            "name": "vacancies",
            "description": "Get vacancy from hh.ru",
        },
    ]
    ERRORS: ErrorType = {
        400: {'model': HttpError400},
        409: {'model': HttpError409},
            }

    size_pool_http: int = 100
    timeout_aiohttp: int = 2


settings = Settings()
