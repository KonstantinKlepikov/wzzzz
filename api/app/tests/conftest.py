import pytest
from typing import Generator
from fastapi.testclient import TestClient
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.main import app
from app.crud.crud_vacancy import CRUDVacancies
from app.crud.crud_template import CRUDTemplate
from app.schemas import (
    VacancyResponseInDb,
    TemplateName,
    Template,
    TemplateConstraints,
    UserInDb,
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
                await db[collection].create_index(
                        [('name', ASCENDING), ('user', ASCENDING),],
                        unique=True
                            )
            if collection == Collections.USERS.value:
                await db[collection].create_index('login', unique=True)

        # fill vacancies
        collection = db[Collections.VACANCIES.value]
        one = VacancyResponseInDb.Config.schema_extra['example']
        another = {'v_id': 654321}
        await collection.insert_many([one, another])

        # fill user
        collection = db[Collections.USERS.value]
        one = UserInDb.Config.schema_extra['example']
        in_db = await collection.insert_one(one)

        # fill template
        collection = db[Collections.TEMPLATES.value]
        one = Template.Config.schema_extra['example']
        one['user'] = in_db.inserted_id
        await collection.insert_one(one)
        yield db


@pytest.fixture(scope="function")
async def crud_vacancy() -> CRUDVacancies:
    """Get crud vacancies
    """
    return CRUDVacancies(
        schema=VacancyResponseInDb,
        col_name=Collections.VACANCIES.value,
        db_name=DB_NAME
            )


@pytest.fixture(scope="function")
async def crud_template() -> CRUDTemplate:
    """Get crud template
    """
    return CRUDTemplate(
        schema=TemplateConstraints,
        col_name=Collections.TEMPLATES.value,
        db_name=DB_NAME
            )
