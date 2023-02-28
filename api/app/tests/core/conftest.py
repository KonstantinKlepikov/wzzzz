import pytest
import json
from aiohttp import web
from aiohttp.test_utils import TestClient
from yarl import URL
from app.core import SessionMaker
from app.schemas import VacancyRequestScheme


async def hhru_vacancy(request: web.Request) -> web.Response:
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
