from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # api vars
    API_V1: str = "http://wzzzz-api:8000/api/v1"
    TG_API_TOKEN: SecretStr = None
    REDIS_URL: str = None


settings = Settings()
