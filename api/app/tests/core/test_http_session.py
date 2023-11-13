import pytest
from aiohttp.test_utils import TestClient
from fastapi import HTTPException
from app.core.http_session import SessionMaker
from app.schemas.scheme_vacanciy import VacancyRequest


class TestAiohttpClient:
    """Test aiohttp session cleint
    """


    async def test_aiohttp_client(
        self,
        session: SessionMaker,
        urls: dict[str, str]
            ) -> None:
        """Test get_aiohttp_client
        """
        assert isinstance(session.aiohttp_client, TestClient), 'wrong client'
        await session.close_aiohttp_client()
        assert session.aiohttp_client is None, 'not closed'
        # TODO: test session creation with parameters (?)

    async def test_client(
        self,
        session: SessionMaker,
        urls: dict[str, str]
            ) -> None:
        """Test testclient
        """
        resp = await session.aiohttp_client.get(urls['hhru_vacancy'])
        assert resp.status == 200
        text = await resp.text()
        assert 'Секретарь' in text, 'wrong result'

    @pytest.mark.parametrize(
        "route,status",
        [("err400", "400"), ("err404", "404"), ("err429", "429")]
            )
    async def test_client_errors(
        self,
        route: str,
        status: int,
        session: SessionMaker,
        urls: dict[str, str]
            ) -> None:
        """Test testclient raise response errors
        """
        with pytest.raises(HTTPException):
            await session._get(session.aiohttp_client, urls[route])
            # TODO: get an exception code and text

    async def test_vacancies_query(
        self,
        session: SessionMaker,
        urls: dict[str, str]
            ) -> None:
        """Test vacancy query
        """
        result = await session.get_query(
            url='/vacancies',
            params=VacancyRequest.Config.json_schema_extra['example']
                )
        assert result['per_page'] == 1, 'wrong result'
        # TODO: test with semaphores
