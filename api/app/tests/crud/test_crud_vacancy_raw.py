import pytest
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult
from app.crud.crud_vacancy_raw import CRUDVacanciesRaw
from app.schemas.scheme_vacancy_raw import VacancyRawData
from app.schemas.constraint import Collections


@pytest.mark.skip("TODO: test me")
class TestCRUDVacancyRaw:
    """Test crud vacancy raw
    """

    async def test_crud_vacancy_raw_create(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacanciesRaw
            ) -> None:
        """"""

    async def test_crud_vacancy_raw_get_by_vacancy_id(
        self,
        db: ClientSession,
        crud_vacancy_raw: CRUDVacanciesRaw
            ) -> None:
        """Test crud vacancy raw get by id
        """

    async def test_crud_vacancy_raw_get_notexisted_id(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacanciesRaw
            ) -> None:
        """Test crud vacancy raw get notexisted id
        """

    async def test_crud_vacancy_raw_create_many(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacanciesRaw
            ) -> None:
        """Test vacancy raw create many
        """

    async def test_crud_vaсancy_create_many_error_if_double(
        self,
        db: ClientSession,
        crud_vacancy: CRUDVacanciesRaw
            ) -> None:
        """Test vacancy raw create many dublicate error
        """
