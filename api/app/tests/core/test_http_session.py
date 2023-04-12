from aiohttp.test_utils import TestClient
from app.core import SessionMaker
from app.schemas import VacancyRequest


async def test_aiohttp_client(
    session: SessionMaker,
    urls: dict[str, str]
        ) -> None:
    """Test get_aiohttp_client
    """
    assert isinstance(session.aiohttp_client, TestClient), 'wrong client'
    await session.close_aiohttp_client()
    assert session.aiohttp_client is None, 'not closed'
    # TODO: test sessionc creation with parameters (?)


async def test_client(
    session: SessionMaker,
    urls: dict[str, str]
        ) -> None:
    """Test testclient
    """
    resp = await session.aiohttp_client.get(urls['hhru_vacancy'])
    assert resp.status == 200
    text = await resp.text()
    assert 'Секретарь' in text, 'wrong result'


async def test_vacancies_query(
    session: SessionMaker,
    urls: dict[str, str]
        ) -> None:
    """Test vacancy query
    """
    result = await session.get_query(
        url='/vacancies',
        params=VacancyRequest.Config.schema_extra['example']
            )
    assert result['per_page'] == 1, 'wrong result'
