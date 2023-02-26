import pytest
import json
from aiohttp import web
from aiohttp.test_utils import TestClient
from yarl import URL
from app.core.http_session import SessionMaker
from app.schemas.scheme_request import VacancyRequestScheme


async def hhru_vacancy(request: web.Request) -> str:
    """Mock hhru vacancy response
    """
    with open('./tests/core/vac_resp.json', 'r') as f:
        data = json.loads(f.read())
    return web.Response(text=json.dumps(data, ensure_ascii=False))


@pytest.fixture
def urls() -> dict[str, str]:
    """Urls for request

    Returns:
        dict[str, str]: dict with urls
    """
    urls = {
        'hhru_vacancy': str(URL.build(
            path='/vacancies',
            query=VacancyRequestScheme.Config.schema_extra['example']
                ),
            )}
    return urls


@pytest.fixture
def client(loop, aiohttp_client) -> TestClient:
    """Make a test client
    """
    app = web.Application()
    app.router.add_routes([
        web.get('/vacancies', hhru_vacancy),
            ])
    client = loop.run_until_complete(aiohttp_client(app))
    return client


@pytest.fixture
def session(client: TestClient) -> SessionMaker:
    """Make test session
    """
    SessionMaker.aiohttp_client = client
    session = SessionMaker()
    return session


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


async def test_vacancy_query(
    session: SessionMaker,
    urls: dict[str, str]
        ) -> None:
    """Test vacancy query
    """
    result = await session.vacancy_query(
        url='/vacancies',
        params=VacancyRequestScheme.Config.schema_extra['example']
            )
    assert 'Секретарь' in result, 'wrong result'
