from typing import Generator
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.client_session import ClientSession
from fastapi.logger import logger as fastAPI_logger
from app.config import settings
from app.schemas.constraint import Collections


def get_client(mongodb_url: str) -> AsyncIOMotorClient:
    """Get mongo db

    Args:
        mongodb_url (str): url to mongo

    Returns:
        AsyncIOMotorClient: client exemplar
    """
    fastAPI_logger.info("Create mongo client")
    return AsyncIOMotorClient(mongodb_url)


async def create_collections(
    client: AsyncIOMotorClient,
    db_name: str = settings.db_name,
        ) -> None:
    """Create collections

    Args:
        client (AsyncIOMotorClient): client
        db_name (str, optional): collection name.
                                 Defaults to settings.db_name.
    """
    async for collection in Collections.get_values():
        try:
            await client[db_name].create_collection(collection)
        except:
            continue


client = get_client(settings.mongodb_url)


async def create_collections() -> None:
    """Create collections
    """
    for collection in Collections.get_values():
        try:
            await client[settings.db_name].create_collection(collection)
            if collection == Collections.VACANCIES:
                await client[settings.db_name][collection].create_index('v_id', unique=True)
        except:
            continue


async def get_session() -> Generator[ClientSession, None, None]:
    """Get mongo session
    """
    try:
        fastAPI_logger.info("Create mongo session")
        session: ClientSession = await client.start_session()
        yield session
    finally:
        await session.end_session()