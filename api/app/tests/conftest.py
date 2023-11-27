import pytest
from typing import Generator
from pymongo import ASCENDING, IndexModel
from pymongo.client_session import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient
from app.config import settings
from app.main import app
from app.crud.crud_vacancy import CRUDVacancies
from app.crud.crud_vacancy_raw import CRUDVacanciesRaw
from app.crud.crud_template import CRUDTemplate
from app.crud.crud_user import CRUDUser
from app.schemas.scheme_user import UserInDb
from app.schemas.scheme_templates import (
    TemplateInDb,
    TemplateConstraints,
        )
from app.schemas.scheme_vacanciy import VacancyResponseInDb
from app.schemas.scheme_vacancy_raw import VacancyRawData
from app.schemas.constraint import Collections
from app.db import get_session


DB_NAME = 'test-db'


class BdTestContext:
    def __init__(self, mongodb_url: str, db_name: str):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db_name = db_name

    async def __aenter__(self):
        await self.client.drop_database(self.db_name)
        return self.client[self.db_name]

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.drop_database(self.db_name)
        self.client.close()


@pytest.fixture(scope="function")
async def db() -> Generator:
    """Get mock mongodb
    """
    async with BdTestContext(settings.TEST_MONGODB_URL, DB_NAME) as d:

        for collection in Collections.get_values():
            await d.create_collection(collection)
            if collection == Collections.VACANCIES:
                index1 = IndexModel('v_id', unique=True)
                index2 = IndexModel(
                    'ts', expireAfterSeconds=settings.EXPIRED_BY_SECONDS
                        )
                await d[collection].create_indexes(
                    [index1, index2, ]
                        )
            if collection == Collections.VACANCIES_SIMPLE_RAW or \
                    Collections.VACANCIES_DEEP_RAW:
                index1 = IndexModel('v_id', unique=True)
                index2 = IndexModel(
                    'ts', expireAfterSeconds=settings.EXPIRED_BY_SECONDS
                        )
                await d[collection].create_indexes(
                    [index1, index2, ]
                        )
            if collection == Collections.TEMPLATES.value:
                await d[collection].create_index(
                        [('name', ASCENDING), ('user', ASCENDING), ],
                        unique=True
                            )
            if collection == Collections.USERS.value:
                await d[collection].create_index('user_id', unique=True)

        collection = d[Collections.USERS.value]
        u = await collection.find_one({'user_id': 45456897})
        print(u)

        # fill vacancies
        collection = d[Collections.VACANCIES.value]
        one = VacancyResponseInDb.Config.json_schema_extra['example']
        another = {'v_id': 654321}
        # FIXME: pymongo.errors.BulkWriteError: batch op errors occurred, full error:
        # {'writeErrors': [{'index': 1, 'code': 11000, 'errmsg': 'E11000 duplicate key error
        # collection: test-db.vacancies index: raw_id_1 dup key: { raw_id: null }', 'keyPattern':
        # {'raw_id': 1}, 'keyValue': {'raw_id': None}, 'op': {'v_id': 654321, '_id':
        # ObjectId('654ac2794b19c9471d2c8d9c')}}], 'writeConcernErrors': [], 'nInserted': 1,
        # 'nUpserted': 0, 'nMatched': 0, 'nModified': 0, 'nRemoved': 0, 'upserted': []}
        await collection.insert_many([one, another])

        # fill user
        collection = d[Collections.USERS.value]
        one = UserInDb.Config.json_schema_extra['example']
        in_db = await collection.insert_one(one)

        # fill template
        collection = d[Collections.TEMPLATES.value]
        one = TemplateInDb.Config.json_schema_extra['example']
        one['user'] = str(in_db.inserted_id)
        await collection.insert_one(one)

        yield d


@pytest.fixture(scope="function")
async def client(db) -> Generator:

    bd_test_client = AsyncIOMotorClient(settings.TEST_MONGODB_URL)

    async def mock_session() -> Generator[ClientSession, None, None]:
        """Get mongo session
        """
        try:
            session = await bd_test_client.start_session()
            yield session
        finally:
            await session.end_session()

    app.dependency_overrides[get_session] = mock_session

    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

    app.dependency_overrides = {}
    bd_test_client.close()


@pytest.fixture(scope="function")
async def crud_user() -> CRUDUser:
    """Get crud users
    """
    return CRUDUser(
        schema=UserInDb,
        col_name=Collections.USERS.value,
        db_name=DB_NAME
            )


# FIXME: remove me
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


@pytest.fixture(scope="function")
async def crud_vacancy_raw() -> CRUDVacanciesRaw:
    """Get crud vacancies raw
    """
    return CRUDVacanciesRaw(
        schema=VacancyRawData,
        col_name=Collections.VACANCIES.value,
        db_name=DB_NAME
            )
