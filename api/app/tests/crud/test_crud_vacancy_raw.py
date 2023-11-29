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
        crud = request.getfixturevalue(fixname)

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
        crud = request.getfixturevalue(fixname)

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
