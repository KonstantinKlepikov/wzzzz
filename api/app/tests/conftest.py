import pytest
from typing import Generator
from fastapi.testclient import TestClient
from app.config import settings
from app.main import app, db_on_start_up


from motor.motor_asyncio import AsyncIOMotorClient


class BdTestContext:
    def __init__(self, mongodb_url: str, db_name: str):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db_name = db_name

    async def __aenter__(self):
        return self.client[self.db_name]

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.drop_database(self.db_name)
        self.client.close()


async def test_db_on_start_up():
    async with BdTestContext(settings.test_mongodb_url, 'test-db') as cont:
        global db
        db = cont[settings.db_name]


app.dependency_overrides[db_on_start_up] = test_db_on_start_up


@pytest.fixture(scope="function")
async def client() -> Generator:
    async with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
async def connection() -> Generator:
    """Get mock mongodb
    """
    async with BdTestContext(
        settings.test_mongodb_url,
        'test-db'
            ) as cont:
        yield cont
