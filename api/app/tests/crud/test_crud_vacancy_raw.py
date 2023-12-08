import pytest
import nest_asyncio
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult
from app.crud.crud_vacancy_raw import CRUDVacanciesRaw
from app.schemas.scheme_vacancy_raw import VacancyRawData
from app.schemas.constraint import Collections


nest_asyncio.apply()


class TestCRUDVacancyRaw:
    """Test crud vacancy raw
    """

    @pytest.mark.parametrize(
        'fixname', ['crud_vacancy_simple_raw', 'crud_vacancy_deep_raw']
            )
    async def test_crud_vacancy_raw_create(
        self,
        db: ClientSession,
        fixname,
        request
            ) -> None:
        """Test vacancy raw creation
        """
        crud: CRUDVacanciesRaw = request.getfixturevalue(fixname)
        result = await crud.create_raw(
            db,
            VacancyRawData(**VacancyRawData.Config.json_schema_extra["example"])
                )
        assert isinstance(result, InsertOneResult), 'wrong result'
        assert result.inserted_id, 'result hasnt _id'

    @pytest.mark.parametrize(
        'fixname', ['crud_vacancy_simple_raw', 'crud_vacancy_deep_raw']
            )
    async def test_crud_vacancy_raw_get_by_vacancy_id(
        self,
        db: ClientSession,
        fixname,
        request
            ) -> None:
        """Test crud vacancy raw get by id
        """
        crud: CRUDVacanciesRaw = request.getfixturevalue(fixname)
        result = await crud.get_many_by_v_ids(db, [54321, 654321])
        assert isinstance(result, list), 'wrong result'
        ids = [d['v_id'] for d in result]
        assert 654321 in ids, 'wrong id'
        assert 54321 in ids, 'wrong id'

    @pytest.mark.parametrize(
        'fixname', ['crud_vacancy_simple_raw', 'crud_vacancy_deep_raw']
            )
    async def test_crud_vacancy_raw_get_notexisted_id(
        self,
        db: ClientSession,
        fixname,
        request
            ) -> None:
        """Test crud vacancy raw get notexisted id
        """
        crud: CRUDVacanciesRaw = request.getfixturevalue(fixname)
        result = await crud.get_many_notexisted_v_ids(db, {54321, 99999})
        assert isinstance(result, set), 'wrong result'
        assert 99999 in result, 'wrong not existed id'
        assert 54321 not in result, 'wrong existed id'

    @pytest.mark.parametrize(
        'fixname', ['crud_vacancy_simple_raw', 'crud_vacancy_deep_raw']
            )
    async def test_crud_vacancy_raw_create_many(
        self,
        db: ClientSession,
        fixname,
        request
            ) -> None:
        """Test vacancy raw create many
        """
        crud = request.getfixturevalue(fixname)

    @pytest.mark.parametrize(
        'fixname', ['crud_vacancy_simple_raw', 'crud_vacancy_deep_raw']
            )
    async def test_crud_vaсancy_create_many_error_if_double(
        self,
        db: ClientSession,
        fixname,
        request
            ) -> None:
        """Test vacancy raw create many dublicate error
        """
        crud = request.getfixturevalue(fixname)
