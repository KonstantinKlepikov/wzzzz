import pytest
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult
from app.crud import CRUDVacancies
from app.schemas import VacancyResponseInDb, Collections


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
        data = VacancyResponseInDb.Config.json_schema_extra['example']
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
        result = await crud_vacancy.create(db, VacancyResponseInDb(v_id=444555))
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
            await crud_vacancy.create(db, VacancyResponseInDb(v_id=123456))
            assert 'duplicate key error collection' in e.value.detail, 'wrong error'

    async def test_crud_vacancy_replace(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacancies
            ) -> None:
        """Test vacancy replace
        """
        result = await crud_vacancy.replace(
            db,
            {'v_id': 123456},
            VacancyResponseInDb(v_id=999999)
                )
        assert isinstance(result, UpdateResult), 'wrong result'
        assert result.matched_count == 1, 'wrong matched count'
        assert result.modified_count == 1, 'wrong updated count'
        result = await db[Collections.VACANCIES.value].count_documents({})
        assert result == 2, 'wrong replace'

        result = await crud_vacancy.replace(
            db,
            {'v_id': 555555},
            VacancyResponseInDb(v_id=999999)
                )
        assert result.matched_count == 0, 'wrong matched count'
        assert result.modified_count == 0, 'wrong updated count'

        with pytest.raises(DuplicateKeyError) as e:
            await crud_vacancy.replace(
                db,
                {'v_id': 999999},
                VacancyResponseInDb(v_id=654321)
                    )
            assert 'duplicate key error collection' in e.value.detail, 'wrong error'

    async def test_crud_vacancy_delete(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacancies
            ) -> None:
        """Test vacancy delete
        """
        result = await crud_vacancy.delete(db, {'v_id': 123456})
        assert isinstance(result, DeleteResult), 'wrong result'
        assert result.deleted_count == 1, 'wrong matched count'
        result = await db[Collections.VACANCIES.value].count_documents({})
        assert result == 1, 'not removed'

        result = await crud_vacancy.delete(db, {'v_id': 555555})
        assert result.deleted_count == 0, 'wrong matched count'

    async def test_cкud_vaсancy_get_many_by_ids(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacancies
            ) -> None:
        """Test get many by ids
        """
        ids = [VacancyResponseInDb.Config.json_schema_extra['example']['v_id'], 555555]
        result = await crud_vacancy.get_many_by_ids(db, ids)

        assert isinstance(result, list), 'wromg result rype'
        assert len(result) == 1, 'wrong result len'
        assert result[0]['v_id'] == \
            VacancyResponseInDb.Config.json_schema_extra['example']['v_id'], \
            'wrong result object'

    async def test_cкud_vaсancy_create_many(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacancies
            ) -> None:
        """Test create many
        """
        vacancies = [
            VacancyResponseInDb(v_id=555555),
            VacancyResponseInDb(v_id=666666),
                ]
        result = await crud_vacancy.create_many(db, vacancies)

        assert isinstance(result, list), 'wromg result rype'
        assert len(result) == 2, 'wrong result len'

    async def test_crud_vaсancy_create_many_error_if_double(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacancies
            ) -> None:
        """Test create many dublicate error
        """
        vacancies = [
            VacancyResponseInDb(**VacancyResponseInDb.Config.json_schema_extra['example']),
                ]
        with pytest.raises(DuplicateKeyError) as e:
            await crud_vacancy.create_many(db, vacancies)
            assert 'duplicate key error collection' in e.value.detail, 'wrong error'
