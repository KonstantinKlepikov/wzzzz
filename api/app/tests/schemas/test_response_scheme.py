from app.schemas.scheme_response import VacancyResponseScheme


class TestVacancyResponsetData:
    """Test response schemas
    """

    def test_full_fill_response(self):
        """Test VacancyResponseScheme fill
        """
        data = VacancyResponseScheme.Config.schema_extra['example']

        scheme = VacancyResponseScheme(**data)

        assert scheme.hhru_id == data['hhru_id'], 'wrong hhru_id'
        assert scheme.name == data['name'], 'wrong name'
        assert scheme.area == data['area'], 'wrong area'
        assert scheme.description == data['description'], 'wrong description'
        assert scheme.key_skills == data['key_skills'], 'wrong key_skills'
        assert scheme.employer == data['employer'], 'wrong employer'
        assert scheme.alternative_url == data['alternative_url'], 'wrong url'
