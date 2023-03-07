import pytest
import json
from typing import Any
from aiohttp import web
from aiohttp.test_utils import TestClient
from app.core import HhruQueries
from app.schemas import VacancyRequestScheme


@pytest.fixture
def hhruqueries(session: TestClient) -> HhruQueries:
    """Make queries class
    """
    q = HhruQueries(
        session,
        "https://api.hh.ru/vacancies",
        VacancyRequestScheme(**VacancyRequestScheme.Config.schema_extra['example'])
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

    def test_make_simple_result(
        self,
        hhruqueries: HhruQueries,
        simple_data: dict[str, Any]
            ) -> None:
        """Test make_simple_result
        """
        data = [{'items': [simple_data, ]}, ]
        result = hhruqueries._make_simple_result(data)
        assert isinstance(result, dict), 'wrong result type'
        assert len(result) == 1, 'wrong len result'
        assert simple_data['id'] in result.keys(), 'wrong key'
        assert result[simple_data['id']]['url'] == simple_data['url'], \
            'wrong transform'

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