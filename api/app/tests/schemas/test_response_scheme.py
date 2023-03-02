from app.schemas import Vacancy

class TestVacancyResponsetData:
    """Test response schemas
    """

    def test_full_fill_response(self):
        """Test VacancyResponseScheme fill
        """
        data = Vacancy.Config.schema_extra['example']
        scheme = Vacancy(**data)

        assert scheme.professional_roles == data['professional_roles'], \
            'wrong professional_roles'
        assert scheme.area == data['area'], 'wrong area'
        assert scheme.description == data['description'], 'wrong description'
        assert scheme.key_skills == data['key_skills'], 'wrong key_skills'
        assert scheme.employer == data['employer'], 'wrong employer'
        assert scheme.alternate_url == data['alternate_url'], 'wrong url'
        assert scheme.experience == data['experience'], 'wrong experience'
