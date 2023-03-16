import toml
from pydantic import BaseSettings
from typing import Optional, Type



class Settings(BaseSettings):
    # api vars
    api_v1_str: str = "http://wzzzz-api:8000/api/v1"
    API_TOKEN: str = None


settings = Settings()
