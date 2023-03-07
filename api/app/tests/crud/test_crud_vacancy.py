import pytest
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from pymongo.results import InsertOneResult, DeleteResult
from app.crud.crud_vacancy import CRUDVacancies
from app.schemas import VacancyDb
from app.schemas.constraint import Collections


class TestCRUDVacancy:
    """Test crud vacancy
    """

    async def test_crud_vacancy_get_by_vacancy_id(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacancies
            ) -> None:
        """Test crud vacancy get by id
        """
        data = VacancyDb.Config.schema_extra['example']
        vacancy = await crud_vacancy.get(db, {'v_id': data['v_id']})
        assert isinstance(vacancy, dict), 'wrong result type'
        assert vacancy['v_id'] == data['v_id'], 'wrong geted data'

    async def test_crud_vacancy_get_many_vacances(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacancies
            ) -> None:
        """Test crud vacancy get by id
        """
        vacancy = await crud_vacancy.get_many(db, {})
        assert isinstance(vacancy, list), 'wrong result type'
        assert len(vacancy) == 2, 'wrong result number'
        assert vacancy[0]['v_id'] == 123456, 'wrong geted data'
        assert vacancy[1]['v_id'] == 654321, 'wrong geted data'

    async def test_crud_vacancy_create(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacancies
            ) -> None:
        """Test vacancy create
        """
        result = await crud_vacancy.create(db, VacancyDb(v_id=444555))
        assert isinstance(result, InsertOneResult), 'wrong result'
        assert result.inserted_id, 'result hasnt _id'
        result = await db[Collections.VACANCIES.value].count_documents({})
        assert result == 3, 'not added'

    async def test_crud_vacancy_create_raise_error(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacancies
            ) -> None:
        """Test vacancy raise error if vacancy id isnt unique
        """
        with pytest.raises(DuplicateKeyError) as e:
            await crud_vacancy.create(db, VacancyDb(v_id=123456))
            assert 'duplicate key error collection' in e.value.detail, 'wrong error'

    async def test_crud_vacancy_remove(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacancies
            ) -> None:
        """Test vacancy remove
        """
        result = await crud_vacancy.remove(db, {'v_id': 123456})
        assert isinstance(result, DeleteResult), 'wrong result'
        result = await db[Collections.VACANCIES.value].count_documents({})
        assert result == 1, 'not added'
