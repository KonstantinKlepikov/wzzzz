from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    # api vars
    api_v1_str: str = "http://wzzzz-api:8000/api/v1"
    TG_API_TOKEN: SecretStr = None
    REDIS_URL_DEV: str = None


settings = Settings()
