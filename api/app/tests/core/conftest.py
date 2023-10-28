import pytest
import json
from aiohttp import web
from aiohttp.test_utils import TestClient
from yarl import URL
from app.core.http_session import SessionMaker
from app.schemas.scheme_vacanciy import VacancyRequest


async def hhru_vacancy(request: web.Request) -> web.Response:
    """Mock hhru vacancy response
    """
    with open('./tests/core/vac_resp.json', 'r') as f:
        data = json.loads(f.read())
    return web.Response(text=json.dumps(
        data, ensure_ascii=False), content_type='application/json'
            )


async def err400(request: web.Request) -> web.Response:
    """Mock hhru vacancy response errors
    """
    return web.Response(status=400, content_type='application/json')


async def err404(request: web.Request) -> web.Response:
    """Mock hhru vacancy response errors
    """
    return web.Response(status=404, content_type='application/json')


async def err429(request: web.Request) -> web.Response:
    """Mock hhru vacancy response errors
    """
    return web.Response(status=429, content_type='application/json')


@pytest.fixture
def urls() -> dict[str, str]:
    """Urls for request

    Returns:
        dict[str, str]: dict with urls
    """
    q = VacancyRequest.Config.json_schema_extra['example']
    urls = {
        'hhru_vacancy': str(URL.build(path='/vacancies', query=q)),
        'err400': str(URL.build(path='/err400', query=q)),
        'err404': str(URL.build(path='/err404', query=q)),
        'err429': str(URL.build(path='/err429', query=q)),
            }
    return urls


@pytest.fixture
def client(loop, aiohttp_client) -> TestClient:
    """Make a test client
    """
    app = web.Application()
    app.router.add_routes([
        web.get('/vacancies', hhru_vacancy),
        web.get('/err400', err400),
        web.get('/err404', err404),
        web.get('/err429', err429),
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
