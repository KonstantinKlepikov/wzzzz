import pytest
from typing import Generator
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.main import app
from app.crud.crud_vacancy import CRUDVacancies
from app.crud.crud_template import CRUDTemplate
from app.schemas import (
    VacancyResponseSchemeDb,
    TemplateNameScheme,
    VacancyConstraintsScheme,
        )
from app.schemas.constraint import Collections


DB_NAME = 'test-db'


class BdTestContext:
    def __init__(self, mongodb_url: str, db_name: str):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db_name = db_name

    async def __aenter__(self):
        return self.client[self.db_name]

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.drop_database(self.db_name)
        self.client.close()


@pytest.fixture(scope="function")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
async def db() -> Generator:
    """Get mock mongodb
    """
    async with BdTestContext(settings.test_mongodb_url, DB_NAME) as db:

        for collection in Collections.get_values():
            await db.create_collection(collection)
            if collection == Collections.VACANCIES:
                await db[collection].create_index('v_id', unique=True)
            if collection == Collections.TEMPLATES.value:
                await db[collection].create_index('name', unique=True)

        # fill vacancies
        collection = db[Collections.VACANCIES.value]
        one = VacancyResponseSchemeDb.Config.schema_extra['example']
        another = {'v_id': 654321}
        await collection.insert_many([one, another])

        # fill template
        collection = db[Collections.TEMPLATES.value]
        one = TemplateNameScheme.Config.schema_extra['example']
        await collection.insert_one(one)
        yield db


@pytest.fixture(scope="function")
async def crud_vacancy() -> CRUDVacancies:
    """Get crud vacancies
    """
    return CRUDVacancies(
        schema=VacancyResponseSchemeDb,
        col_name=Collections.VACANCIES.value,
        db_name=DB_NAME
            )


@pytest.fixture(scope="function")
async def crud_template() -> CRUDTemplate:
    """Get crud template
    """
    return CRUDTemplate(
        schema=VacancyConstraintsScheme,
        col_name=Collections.TEMPLATES.value,
        db_name=DB_NAME
            )
