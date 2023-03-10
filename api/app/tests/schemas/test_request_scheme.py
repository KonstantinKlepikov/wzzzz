from app.schemas import VacancyRequest, Employment, Schedule
from datetime import date


class TestVacancyRequestData:
    """Test request schemas
    """

    def test_full_fill_request(self):
        """Test VacancyRequest fill
        """
        data = VacancyRequest.Config.schema_extra['example']
        scheme = VacancyRequest(**data)

        assert scheme.area == data['area'], 'wrong area'
        assert scheme.text == data['text'], 'wrong text'
        assert scheme.search_field == data['search_field'], 'wrong search'
        assert scheme.employment[0] == Employment.FULL, 'wrong employment'
        assert scheme.schedule[0] == Schedule.REMOTE, 'wrong schedule'
        assert scheme.professional_role == data['professional_role'], 'wrong role'
        assert scheme.date_from == date(2022, 6, 1), 'wrong date'
        assert scheme.page == data['page'], 'wrong per page'
        assert scheme.per_page == data['per_page'], 'wrong per page'
        assert scheme.expirience == data['expirience'], 'wrong expirience'

        result = scheme.json()

        assert data['date_from'] in result, 'wrong date result'
