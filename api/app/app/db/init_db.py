from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.logger import logger as fastAPI_logger
from app.config import settings


class BdContext:
    def __init__(self, mongodb_url: str):
        self.client = AsyncIOMotorClient(mongodb_url)

    async def __aenter__(self):
        return self.client

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.client.close()


async def db_on_start_up():
    fastAPI_logger.info("Mongo db on start up")
    async with BdContext(settings.mongodb_url) as cont:
        global db
        db = cont[settings.db_name]
