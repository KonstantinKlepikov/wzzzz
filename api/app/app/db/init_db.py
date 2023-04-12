from typing import Generator
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, IndexModel
from pymongo.client_session import ClientSession
from pymongo.errors import CollectionInvalid
from fastapi.logger import logger as fastAPI_logger
from app.config import settings
from app.schemas import Collections


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


async def create_collections() -> None:
    """Create collections
    """
    for collection in Collections.get_values():
        try:
            await client[settings.db_name].create_collection(collection)
            if collection == Collections.VACANCIES:
                index1 = IndexModel('v_id', unique=True)
                index2 = IndexModel('ts', expireAfterSeconds=settings.expyred_by_seconds)
                await client[settings.db_name][collection].create_indexes(
                    [index1, index2]
                        )
            if collection == Collections.TEMPLATES.value:
                await client[settings.db_name][collection].create_index(
                    [('name', ASCENDING), ('user', ASCENDING), ],
                    unique=True
                        )
            if collection == Collections.USERS.value:
                await client[settings.db_name][collection].create_index(
                    'user_id',
                    unique=True
                        )
        except CollectionInvalid:
            continue


async def get_session() -> Generator[ClientSession, None, None]:
    """Get mongo session
    """
    try:
        fastAPI_logger.info("Create mongo session")
        session = await client.start_session()
        yield session
    finally:
        await session.end_session()
