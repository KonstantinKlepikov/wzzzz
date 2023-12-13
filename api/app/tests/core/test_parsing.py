import pytest
from app.core.parsing import VacanciesParser
from app.crud.crud_vacancy_raw import CRUDVacanciesRaw
from tests.conftest import VACANCY


@pytest.fixture
def parser(
    db,
    crud_vacancy_simple_raw: CRUDVacanciesRaw,
    crud_vacancy_deep_raw: CRUDVacanciesRaw,
        ) -> VacanciesParser:
    """Make test session
    """
    return VacanciesParser(
        db,
        crud_vacancy_simple_raw,
        crud_vacancy_deep_raw,
        [VACANCY[0]['v_id'], VACANCY[1]['v_id']]
            )


class TestParsing:
    """Test vacancy parsing
    """

    def test_field_to_list(self, parser: VacanciesParser) -> None:
        """Test field_to_list
        """
        data = [
            {'name': '1', 'profarea_name': 'a'},
            {'name': '2', 'profarea_name': 'b'},
                ]
        result = parser._field_to_list(data)
        assert isinstance(result, list), 'wrong type'
        assert len(result) == 2, 'wrong len'
        assert result[0] == '1', 'wrong item'
        assert result[1] == '2', 'wrong item'
        assert parser._field_to_list(None) == [], \
            'wrong empty result'
        assert parser._field_to_list('some') == ['some', ], \
            'wrong another result'

    def test_field_to_value(self, parser: VacanciesParser) -> None:
        """Test field_to_value
        """
        data = {'name': '1', 'profarea_name': 'a'}
        result = parser._field_to_value(data)
        assert result == '1', 'wrong result'
        assert parser._field_to_value(None) is None, \
            'wrong empty result'

    def test_html_to_value(self, parser: VacanciesParser) -> None:
        """Test html_to_value
        """
        data = '<p><strong>this is</strong> fine'
        result = parser._html_to_text(data)
        assert result == 'this is fine', 'wrong result'
        assert parser._html_to_text(None) is None, \
            'wrong empty result'
