import pytest
import json
from typing import Any
from functools import lru_cache
from aiohttp import web
from aiohttp.test_utils import TestClient
from yarl import URL
from app.core.http_session import SessionMaker
from app.schemas.scheme_vacancy_raw import VacancyRequest


@lru_cache
def hhru_vacancy() -> dict[str, Any]:
    """Mock hhru vacancy json data
    """
    with open('./tests/core/vac_resp.json', 'r') as f:
        return json.loads(f.read())


def hhru_response(request: web.Request) -> web.Response:
    """Mock hhru vacancy response
    """
    return web.Response(text=json.dumps(
        hhru_vacancy(), ensure_ascii=False), content_type='application/json'
            )


def err400(request: web.Request) -> web.Response:
    """Mock hhru vacancy response errors
    """
    return web.Response(status=400, content_type='application/json')


def err404(request: web.Request) -> web.Response:
    """Mock hhru vacancy response errors
    """
    return web.Response(status=404, content_type='application/json')


def err429(request: web.Request) -> web.Response:
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
def aiohttp_custom_client(loop, aiohttp_client) -> TestClient:
    """Make a test aioshttp client
    """
    app = web.Application()
    app.router.add_routes([
        web.get('/vacancies', hhru_response),
        web.get('/err400', err400),
        web.get('/err404', err404),
        web.get('/err429', err429),
            ])
    client = loop.run_until_complete(aiohttp_client(app))
    return client


@pytest.fixture
def session(aiohttp_custom_client: TestClient) -> SessionMaker:  # FIXME: used real session maker for test - need to return state
    """Make test session
    """
    SessionMaker.aiohttp_client = aiohttp_custom_client
    session = SessionMaker()
    return session
