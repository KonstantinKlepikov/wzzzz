from typing import Generator
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.client_session import ClientSession
from fastapi.logger import logger as fastAPI_logger
from app.config import settings


def get_client(mongodb_url: str) -> AsyncIOMotorClient:
    """Get mongo db

    Args:
        mongodb_url (str): url to mongo

    Returns:
        AsyncIOMotorClient: client exemplar
    """
    fastAPI_logger.info("Create mongo client")
    return AsyncIOMotorClient(mongodb_url)


client = get_client(settings.mongodb_url)


async def get_session() -> Generator[ClientSession, None, None]:
    """Get mongo session
    """
    try:
        fastAPI_logger.info("Create mongo session")
        session: ClientSession = await client.start_session()
        yield session
    finally:
        await session.end_session()