import pytest
import asyncio
import json
from typing import Any, Callable
from aiohttp.test_utils import TestClient
from pymongo.client_session import ClientSession
from app.core import HhruQueries, HhruQueriesDb, parse_vacancy
from app.schemas import VacancyRequest, Vacancies
from app.db.init_redis import RedisConnection


@pytest.fixture
def hhruqueries(session: TestClient) -> HhruQueries:
    """Make queries class
    """
    q = HhruQueries(
        session,
        "https://api.hh.ru/vacancies",
        VacancyRequest(**VacancyRequest.Config.schema_extra['example'])
        )
    return q


@pytest.fixture
def simple_data() -> dict[str, Any]:
    """Mock hhru vacancy response
    """
    with open('./tests/core/vac_resp.json', 'r') as f:
        data = json.loads(f.read())
    return data['items'][0]


@pytest.fixture
def deeper_data() -> dict[str, Any]:
    """Mock deeper vacancy data
    """
    return {
            'experience': {'id': 'between1And3', 'name': 'xxx'},
            'description': '<p><strong>this is</strong> fine',
            'professional_roles': [{
                'id': '25',
                'name': '1'
                }],
            'key_skills': [
                {'name': '2'},
                {'name': '3'}
                ],
            }


class TestHhruQueries:
    """Test Hhruqueries
    """

    def test_field_to_list(self, hhruqueries: HhruQueries) -> None:
        """Test field_to_list
        """
        data = [
            {'name': '1', 'profarea_name': 'a'},
            {'name': '2', 'profarea_name': 'b'},
                ]
        result = hhruqueries._field_to_list(data)
        assert isinstance(result, list), 'wrong type'
        assert len(result) == 2, 'wrong len'
        assert result[0] == '1', 'wrong item'
        assert result[1] == '2', 'wrong item'
        assert hhruqueries._field_to_list(None) == [], \
            'wrong empty result'
        assert hhruqueries._field_to_list('some') == ['some', ], \
            'wrong another result'

    def test_field_to_value(self, hhruqueries: HhruQueries) -> None:
        """Test field_to_value
        """
        data = {'name': '1', 'profarea_name': 'a'}
        result = hhruqueries._field_to_value(data)
        assert result == '1', 'wrong result'
        assert hhruqueries._field_to_value(None) is None, \
            'wrong empty result'

    def test_html_to_value(self, hhruqueries: HhruQueries) -> None:
        """Test html_to_value
        """
        data = '<p><strong>this is</strong> fine'
        result = hhruqueries._html_to_text(data)
        assert result == 'this is fine', 'wrong result'
        assert hhruqueries._html_to_text(None) is None, \
            'wrong empty result'

    def test_simple_to_dict(
        self,
        hhruqueries: HhruQueries,
        simple_data: dict[str, Any]
            ) -> None:
        """Test simple_to_dict
        """
        item = hhruqueries._simple_to_dict(simple_data)
        assert item['url'] == simple_data['url'], 'wrong url'
        assert item['alternate_url'] == simple_data['alternate_url'], \
            'wrong alternative_url'
        assert item['area'] == simple_data['area']['name'], 'wrong area'
        assert item['employer'] == simple_data['employer']['name'], 'wrong area'

    def test_deeper_to_dict(
        self,
        hhruqueries: HhruQueries,
            ) -> None:
        """Test deeper_to_dict
        """
        data = {
            'experience': {'id': 'between1And3', 'name': 'xxx'},
            'description': '<p><strong>this is</strong> fine',
            'professional_roles': [{
                'id': '25',
                'name': '1'
                }],
            'key_skills': [
                {'name': '2'},
                {'name': '3'}
                ],
            }
        item = hhruqueries._deeper_to_dict(data)
        assert item['experience'] == 'xxx', 'wrong expirience'
        assert item['description'] == 'this is fine', 'wrong description'
        assert item['professional_roles'] == ['1', ], 'wrong roles'
        assert item['key_skills'] == ['2', '3'], 'wrong skills'

    async def test_make_simple_result(
        self,
        hhruqueries: HhruQueries,
        simple_data: dict[str, Any],
        db: ClientSession
            ) -> None:
        """Test make_simple_result
        """
        data = [{'items': [simple_data, ]}, ]
        result = await hhruqueries._make_simple_result(db, data)
        assert isinstance(result, dict), 'wrong type'
        assert len(result) == 2, 'wrong number of objects'
        assert len(result['in_db']) == 0, 'wrong in db'
        assert len(result['not_in_db']) == 1, 'wrong not in db'
        assert result['not_in_db'][simple_data['id']]['url'] == simple_data['url'], \
            'wrong parsing'

    def test_make_deeper_result(
        self,
        hhruqueries: HhruQueries,
        deeper_data: dict[str, Any]
            ) -> None:
        """Test make_deeper_result
        """
        deeper_data['id'] = '12345'
        data = [deeper_data, ]
        result = hhruqueries._make_deeper_result(data)
        assert isinstance(result, dict), 'wrong result type'
        assert len(result) == 1, 'wrong result len'
        assert '12345' in result.keys(), 'wrong result keys'
        assert result['12345']['key_skills'] == ['2', '3'], 'wrong skills'

    @pytest.mark.skip('# TODO: test me')
    def test_update(self, hhruqueries: HhruQueries) -> None:
        """Test _update
        """

    @pytest.mark.skip('# TODO: test me')
    async def test_make_simple_requests(self, hhruqueries: HhruQueries) -> None:
        """Test _make_simple_requests
        """

    @pytest.mark.skip('# TODO: test me')
    async def test_make_deeper_requests(self, hhruqueries: HhruQueries) -> None:
        """Test _make_simple_requests
        """

    @pytest.mark.skip('# TODO: test me')
    async def test_vacancies_query(self, hhruqueries: HhruQueries) -> None:
        """Test vacancies_query
        """


class TestHhruQueriesDb:
    """Test HhruqueriesDb
    # TODO: test me'
    """


@pytest.fixture(scope="function")
def mock_query(monkeypatch) -> Callable:
    """Mock hhru query
    """
    async def mock_return(*args, **kwargs) -> Callable:
        return None

    monkeypatch.setattr(HhruQueriesDb, "vacancies_query", mock_return)
    monkeypatch.setattr(HhruQueriesDb, "save_to_db", mock_return)


@pytest.fixture
def hhruqueriesdb(session: TestClient, mock_query: Callable) -> HhruQueriesDb:
    """Make queries class
    """
    q = HhruQueriesDb(
        session,
        "https://api.hh.ru/vacancies",
        VacancyRequest(**VacancyRequest.Config.schema_extra['example'])
        )
    q.result['not_in_db'] = Vacancies.Config.schema_extra['example']['vacancies']
    return q


async def test_parse_vacancy(hhruqueriesdb: HhruQueriesDb, db: ClientSession) -> None:
    """Test parse vacancy pubsub
    """
    user_id = list(Vacancies.Config.schema_extra['example']['vacancies'].keys())[0]

    async with RedisConnection() as conn:
        async with conn.pubsub() as pubsub:
            await pubsub.subscribe(str(user_id))
            await parse_vacancy(user_id, hhruqueriesdb, db, conn)

            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    break
                await asyncio.sleep(0.001)
    assert isinstance(message, dict), 'wrong type'
    assert message['type'] == 'message', 'wrong type of message'
    assert message['channel'].decode("utf-8") == str(user_id), 'wrong channel'
    j_data = json.loads(message['data'].decode("utf-8"))
    assert str(user_id) in j_data['vacancies'].keys(), 'wrong data'
