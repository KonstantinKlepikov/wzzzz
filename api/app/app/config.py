import toml
from pydantic import BaseSettings
from typing import Optional


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
            "name": "check_hhru",
            "description": "CTest hh.ru OpenAPI endpoint",
        },
    ]

    size_pool_http: int = 100
    timeout_aiohttp: int = 2


settings = Settings()
