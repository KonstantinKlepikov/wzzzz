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
def hhru_vacancy() -> dict[str, Any]:
    """Mock hhru vacancy response
    """
    with open('./tests/core/vac_resp.json', 'r') as f:
        data = json.loads(f.read())
    return data['items'][0]


class TestHhruQueries:
    """Test Hhruqueries
    """

    @pytest.mark.skip('# TODO: test me')
    def test_field_to_list(self, hhruqueries: HhruQueries) -> None:
        """Test field_to_list
        """

    @pytest.mark.skip('# TODO: test me')
    def test_get_text(self, hhruqueries: HhruQueries) -> None:
        """Test get_text
        """

    def test_simple_to_scheme(
        self,
        hhruqueries: HhruQueries,
        hhru_vacancy: dict[str, Any]
            ) -> None:
        """Test simple_to_scheme
        """
        item = hhruqueries.simple_to_scheme(hhru_vacancy)
        assert item.vac_id == int(hhru_vacancy['id']), 'wrong id'

    @pytest.mark.skip('# TODO: test me')
    async def vacancies_query(self, hhruqueries: HhruQueries) -> None:
        """Test vacancies_query
        """
