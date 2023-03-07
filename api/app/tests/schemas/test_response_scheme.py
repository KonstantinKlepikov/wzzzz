from app.schemas import VacancyResponseScheme

class TestVacancyResponsetData:
    """Test response schemas
    """

    def test_full_fill_response(self):
        """Test VacancyResponseScheme fill
        """
        data = VacancyResponseScheme.Config.schema_extra['example']
        scheme = VacancyResponseScheme(**data)

        assert scheme.professional_roles == data['professional_roles'], \
            'wrong professional_roles'
        assert scheme.area == data['area'], 'wrong area'
        assert scheme.description == data['description'], 'wrong description'
        assert scheme.key_skills == data['key_skills'], 'wrong key_skills'
        assert scheme.employer == data['employer'], 'wrong employer'
        assert scheme.alternate_url == data['alternate_url'], 'wrong url'
        assert scheme.experience == data['experience'], 'wrong experience'
