import pytest
import json
from functools import lru_cache
from typing import Any, Callable
from aiohttp.test_utils import TestClient
from pymongo.client_session import ClientSession
from fastapi import HTTPException
from app.core.queries import HhruBaseQueries
from app.core.http_session import SessionMaker
from app.schemas.scheme_vacancy_raw import VacancyRawData, VacancyRequest
from app.crud.crud_vacancy_raw import vacancies_deep_raw


@pytest.fixture
def base_queries(session: TestClient) -> HhruBaseQueries:
    """Make queries class
    """
    q = HhruBaseQueries(
        session,
        "https://api.hh.ru/vacancies",
        VacancyRequest(**VacancyRequest.Config.json_schema_extra['example'])
            )
    return q


@pytest.fixture
@lru_cache
def entry_data() -> dict[str, Any]:
    """Mock hhru vacancy entry page response
    """
    with open('./tests/core/vac_entry.json', 'r') as f:
        return json.loads(f.read())


@pytest.fixture
@lru_cache
def simple_data() -> list[dict[str, Any]]:
    """Mock hhru vacancy response
    """
    with open('./tests/core/vac_resp.json', 'r') as f:
        return json.loads(f.read())


@pytest.fixture
@lru_cache
def deeper_data() -> dict[str, Any]:
    """Mock deeper vacancy data
    """
    with open('./tests/core/vac_deep_resp.json', 'r') as f:
        return json.loads(f.read())


class TestHhruBaseQueries:
    """Test HhruBaseQueries
    """

    @pytest.fixture(scope="function")
    async def mock_entry_response(
        self,
        session: SessionMaker,
        entry_data: dict[str, Any],
        monkeypatch,
            ) -> Callable:
        async def mock_return(*args, **kwargs) -> Callable:
            return entry_data
        monkeypatch.setattr(session, "get_query", mock_return)

    async def test_make_entry(
        self,
        base_queries: HhruBaseQueries,
        entry_data: dict[str, Any],
        mock_entry_response: Callable
            ) -> None:
        """Test make_simple_entry
        """
        result = await base_queries._make_entry()
        assert result['pages'] == entry_data['pages'], 'wrong pages'
        assert result['per_page'] == entry_data['per_page'], 'wrong per_page'

    async def test_make_simple_requests(
        self,
        base_queries: HhruBaseQueries,
        mock_entry_response,
        entry_data: dict[str, Any]
            ) -> None:
        """Test make simple request
        """
        result = await base_queries._make_simple_requests()
        assert len(result) == 2020, 'wrong result len'
        assert result[0].id == result[20].id, 'mock query not doubled'
        assert result[0].id == int(entry_data['items'][0]['id'])

    def test_get_corresct_simple_response(
        self,
        base_queries: HhruBaseQueries,
        entry_data: dict[str, Any],
            ) -> None:
        """Test get corrext simple response
        """
        data = [entry_data, HTTPException(400)]
        result = base_queries._get_corresct_simple_response(data)
        assert len(result) == 20, 'wrong result len'
        assert HTTPException not in result, 'wrong result'

    @pytest.fixture(scope="function")
    async def mock_vacancy_deeper_response(
        self,
        session: TestClient,
        deeper_data: dict[str, Any],
        monkeypatch,
            ) -> Callable:
        async def mock_return(*args, **kwargs) -> Callable:
            return deeper_data
        monkeypatch.setattr(session, "get_query", mock_return)

    async def test_make_deeper_requests(
        self,
        base_queries: HhruBaseQueries,
        mock_vacancy_deeper_response,
        deeper_data: dict[str, Any]
            ) -> None:
        """Test make deeper request
        """
        urls = [deeper_data["alternate_url"] for _ in range(10)]
        result = await base_queries._make_deeper_requests(urls)
        assert len(result) == 10, 'wrong result len'
        assert isinstance(result[0], VacancyRawData)
        assert result[0].id == int(deeper_data["id"]), 'wrong content'

    # TODO: test semaphores and errors in requests

    @pytest.fixture(scope="function")
    async def mock_simple_request(
        self,
        base_queries: HhruBaseQueries,
        simple_data: list[dict[str, Any]],
        monkeypatch,
            ) -> Callable:
        async def mock_return(*args, **kwargs) -> Callable:
            return [VacancyRawData(**res) for res in simple_data['items']]
        monkeypatch.setattr(base_queries, "_make_simple_requests", mock_return)

    @pytest.fixture(scope="function")
    async def mock_deeper_request(
        self,
        base_queries: HhruBaseQueries,
        deeper_data: dict[str, Any],
        simple_data: list[dict[str, Any]],
        monkeypatch,
            ) -> Callable:
        async def mock_return(*args, **kwargs) -> Callable:
            return [VacancyRawData(**deeper_data) for _ in range(len(simple_data))]
        monkeypatch.setattr(base_queries, "_make_deeper_requests", mock_return)

    @pytest.fixture(scope="function")
    async def mock_get_many_notexisted_v_ids(
        self,
        simple_data: list[dict[str, Any]],
        monkeypatch,
            ) -> Callable:
        async def mock_return(*args, **kwargs) -> Callable:
            return {int(d['id']) for d in simple_data["items"]}
        monkeypatch.setattr(vacancies_deep_raw , "get_many_notexisted_v_ids", mock_return)

    async def test_query(
        self,
        base_queries: HhruBaseQueries,
        db: ClientSession,
        mock_simple_request: list[VacancyRawData],
        mock_deeper_request: list[VacancyRawData],
        simple_data: list[dict[str, Any]],
        mock_get_many_notexisted_v_ids: set[int]
        ) -> None:
        """Test query
        """
        # TODO: mock save to db and taest with crud
        result = await base_queries.query(db)
        assert isinstance(result, tuple), 'wrong type'
        assert isinstance(result[0], list), 'wrong type'
        assert isinstance(result[1], list), 'wrong type'
        assert len(result[0]) == 1, 'wrong len'
        assert result[0].pop() == int(simple_data['items'][0]['id']), 'wrong id'
