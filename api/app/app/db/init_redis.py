from typing import Generator
from redis.asyncio import Redis
from fastapi.logger import logger as fastAPI_logger
from app.config import settings


class RedisConnection:
    def __init__(self):
        self.db = Redis(host=settings.REDIS_URL, port=6379, db=0)

    async def __aenter__(self):
        return self.db

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.db.close()


async def get_redis_connection() -> Generator[Redis, None, None]:
    """Get redis session
    """
    async with RedisConnection() as db:
        fastAPI_logger.info("Create redis session")
        yield db
