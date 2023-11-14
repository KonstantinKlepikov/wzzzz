import pytest
import asyncio
import json
from typing import Any, Callable
from aiohttp.test_utils import TestClient
from pymongo.client_session import ClientSession
from fastapi import HTTPException
from app.core.queries import HhruQueriesDb, HhruBaseQueries, get_parse_save_vacancy
from app.schemas.scheme_vacanciy import VacancyRequest, Vacancies
from app.schemas.constraint import Relevance
from app.db.init_redis import RedisConnection


# FIXME: remove me
# @pytest.fixture
# def hhruqueries(session: TestClient) -> HhruQueriesDb:
#     """Make queries class
#     """
#     q = HhruQueriesDb(
#         session,
#         "https://api.hh.ru/vacancies",
#         VacancyRequest(**VacancyRequest.Config.json_schema_extra['example'])
#             )
#     return q


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
def entry_data() -> dict[str, Any]:
    """Mock hhru vacancy entry page response
    """
    with open('./tests/core/vac_entry.json', 'r') as f:
        data = json.loads(f.read())
    return data


@pytest.fixture
def simple_data() -> dict[str, Any]:
    """Mock hhru vacancy response
    """
    with open('./tests/core/vac_resp.json', 'r') as f:
        data = json.loads(f.read())
    return data['items'][0]


# FIXME: remove me
# @pytest.fixture
# def deeper_data() -> dict[str, Any]:
#     """Mock deeper vacancy data
#     """
#     return {
#             'experience': {'id': 'between1And3', 'name': 'xxx'},
#             'description': '<p><strong>this is</strong> fine',
#             'professional_roles': [{
#                 'id': '25',
#                 'name': '1'
#                 }],
#             'key_skills': [
#                 {'name': '2'},
#                 {'name': '3'}
#                 ],
#             }


@pytest.fixture
def deeper_data() -> dict[str, Any]:
    """Mock deeper vacancy data
    """
    with open('./tests/core/vac_deep_resp.json', 'r') as f:
        return json.loads(f.read())


class TestHhruBaseQueries:
    """Test HhruBaseQueries
    """

    @pytest.fixture(scope="function")  # TODO: is tested in http_session, remove me
    async def mock_status(
        self,
        session: TestClient,
        request,
        monkeypatch,
            ) -> Callable:
        async def mock_return(*args, **kwargs) -> Callable:
            raise HTTPException(request.param)
        monkeypatch.setattr(session, "get_query", mock_return)

    @pytest.mark.parametrize("mock_status", [400, 404, 429], indirect=['mock_status'])
    async def test_make_simple_requests_raise_errors(  # TODO: is tested in http_session, remove me
        self,
        base_queries: HhruBaseQueries,
        mock_status: Callable,
            ) -> None:
        """Test make_simple_result raise errors when response raise error
        """
        with pytest.raises(HTTPException):
            await base_queries._make_simple_requests()
            # TODO: get an exception code and text

    @pytest.fixture(scope="function")
    async def mock_entry_response(
        self,
        session: TestClient,
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
        """Test make_simple_result
        """
        result = await base_queries._make_simple_requests()
        assert len(result) == 2020, 'wrong result len'
        assert result[0].id == result[20].id, 'mock query not doubled'

    @pytest.mark.skip('# TODO: test me')
    async def test_make_deeper_requests(
        self,
        hbase_queries: HhruBaseQueries,
        deeper_data: dict[str, Any]
            ) -> None:
        """Test make_deeper_result
        """

    @pytest.mark.skip('# TODO: test me')
    async def test_query(self, base_queries: HhruBaseQueries) -> None:
        """Test query
        """


# FIXME: remove me
# class TestHhruQueries:
#     """Test HhruqueriesDb
#     """

#     def test_field_to_list(self, hhruqueries: HhruQueriesDb) -> None:
#         """Test field_to_list
#         """
#         data = [
#             {'name': '1', 'profarea_name': 'a'},
#             {'name': '2', 'profarea_name': 'b'},
#                 ]
#         result = hhruqueries._field_to_list(data)
#         assert isinstance(result, list), 'wrong type'
#         assert len(result) == 2, 'wrong len'
#         assert result[0] == '1', 'wrong item'
#         assert result[1] == '2', 'wrong item'
#         assert hhruqueries._field_to_list(None) == [], \
#             'wrong empty result'
#         assert hhruqueries._field_to_list('some') == ['some', ], \
#             'wrong another result'

#     def test_field_to_value(self, hhruqueries: HhruQueriesDb) -> None:
#         """Test field_to_value
#         """
#         data = {'name': '1', 'profarea_name': 'a'}
#         result = hhruqueries._field_to_value(data)
#         assert result == '1', 'wrong result'
#         assert hhruqueries._field_to_value(None) is None, \
#             'wrong empty result'

#     def test_html_to_value(self, hhruqueries: HhruQueriesDb) -> None:
#         """Test html_to_value
#         """
#         data = '<p><strong>this is</strong> fine'
#         result = hhruqueries._html_to_text(data)
#         assert result == 'this is fine', 'wrong result'
#         assert hhruqueries._html_to_text(None) is None, \
#             'wrong empty result'

#     def test_simple_to_dict(
#         self,
#         hhruqueries: HhruQueriesDb,
#         simple_data: dict[str, Any]
#             ) -> None:
#         """Test simple_to_dict
#         """
#         item = hhruqueries._simple_to_dict(simple_data)
#         assert item['url'] == simple_data['url'], 'wrong url'
#         assert item['alternate_url'] == simple_data['alternate_url'], \
#             'wrong alternative_url'
#         assert item['area'] == simple_data['area']['name'], 'wrong area'
#         assert item['employer'] == simple_data['employer']['name'], 'wrong area'

#     def test_deeper_to_dict(
#         self,
#         hhruqueries: HhruQueriesDb,
#             ) -> None:
#         """Test deeper_to_dict
#         """
#         data = {
#             'experience': {'id': 'between1And3', 'name': 'xxx'},
#             'description': '<p><strong>this is</strong> fine',
#             'professional_roles': [{
#                 'id': '25',
#                 'name': '1'
#                 }],
#             'key_skills': [
#                 {'name': '2'},
#                 {'name': '3'}
#                 ],
#             }
#         item = hhruqueries._deeper_to_dict(data)
#         assert item['experience'] == 'xxx', 'wrong expirience'
#         assert item['description'] == 'this is fine', 'wrong description'
#         assert item['professional_roles'] == ['1', ], 'wrong roles'
#         assert item['key_skills'] == ['2', '3'], 'wrong skills'

#     async def test_make_simple_result(
#         self,
#         hhruqueries: HhruQueriesDb,
#         simple_data: dict[str, Any],
#         db: ClientSession
#             ) -> None:
#         """Test make_simple_result
#         """
#         data = [{'items': [simple_data, ]}, ]
#         result = await hhruqueries._make_simple_result(db, data)
#         assert isinstance(result, list), 'wrong type'
#         assert len(result) == 2, 'wrong number of objects'
#         assert isinstance(result[0], list), 'wrong in db type'
#         assert len(result[0]) == 0, 'wrong in db'
#         assert isinstance(result[1], dict), 'wrong not in db type'
#         assert len(result[1]) == 1, 'wrong not in db len'
#         assert result[1][simple_data['id']]['url'] == simple_data['url'], \
#             'wrong parsing'

#     def test_make_deeper_result(
#         self,
#         hhruqueries: HhruQueriesDb,
#         deeper_data: dict[str, Any]
#             ) -> None:
#         """Test make_deeper_result
#         """
#         deeper_data['id'] = '12345'
#         data = [deeper_data, ]
#         result = hhruqueries._make_deeper_result(data)
#         assert isinstance(result, dict), 'wrong result type'
#         assert len(result) == 1, 'wrong result len'
#         assert '12345' in result.keys(), 'wrong result keys'
#         assert result['12345']['key_skills'] == ['2', '3'], 'wrong skills'

#     @pytest.mark.skip('# TODO: test me')
#     def test_update(self, hhruqueries: HhruQueriesDb) -> None:
#         """Test _update
#         """

#     @pytest.mark.skip('# TODO: test me')
#     async def test_make_simple_requests(self, hhruqueries: HhruQueriesDb) -> None:
#         """Test _make_simple_requests
#         """

#     @pytest.mark.skip('# TODO: test me')
#     async def test_make_deeper_requests(self, hhruqueries: HhruQueriesDb) -> None:
#         """Test _make_simple_requests
#         """

#     @pytest.mark.skip('# TODO: test me')
#     async def test_vacancies_query(self, hhruqueries: HhruQueriesDb) -> None:
#         """Test vacancies_query
#         """


# @pytest.fixture(scope="function")
# def mock_query(monkeypatch) -> Callable:
#     """Mock hhru query
#     """
#     async def mock_return(*args, **kwargs) -> Callable:
#         return None

#     monkeypatch.setattr(HhruQueriesDb, "vacancies_query", mock_return)
#     monkeypatch.setattr(HhruQueriesDb, "save_to_db", mock_return)


# @pytest.fixture
# def hhruqueriesdb(session: TestClient, mock_query: Callable) -> HhruQueriesDb:
#     """Make queries class
#     """
#     q = HhruQueriesDb(
#         session,
#         "https://api.hh.ru/vacancies",
#         VacancyRequest(**VacancyRequest.Config.json_schema_extra['example'])
#         )
#     q.result[1].update(Vacancies.Config.json_schema_extra['example']['vacancies'])
#     return q


# async def test_get_parse_save_vacancy(
#     hhruqueriesdb: HhruQueriesDb,
#     db: ClientSession
#         ) -> None:
#     """Test parse vacancy pubsub
#     """
#     user_id = 12345
#     vacancy_id = list(Vacancies.Config.json_schema_extra['example']['vacancies'].keys())[0]
#     entry = Vacancies.Config.json_schema_extra['example']['vacancies']
#     relevance = Relevance.ALL

#     async with RedisConnection() as conn:
#         async with conn.pubsub() as pubsub:
#             await pubsub.subscribe(str(user_id))
#             await get_parse_save_vacancy(
#                 user_id,
#                 hhruqueriesdb,
#                 entry,
#                 relevance,
#                 db,
#                 conn,
#                     )

#             while True:
#                 message = await pubsub.get_message(ignore_subscribe_messages=True)
#                 if message:
#                     break
#                 await asyncio.sleep(0.001)
#     assert isinstance(message, dict), 'wrong type'
#     assert message['type'] == 'message', 'wrong type of message'
#     assert message['channel'].decode("utf-8") == str(user_id), 'wrong channel'
#     j_data = json.loads(message['data'].decode("utf-8"))
#     assert j_data == vacancy_id, 'wrong data'
