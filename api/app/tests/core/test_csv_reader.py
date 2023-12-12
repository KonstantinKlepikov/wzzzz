from aiofiles.tempfile import TemporaryFile
from app.core.csv_writer import get_vacancy_csv
# from app.schemas.scheme_vacanciy import AllVacancies, Vacancy
from app.schemas.scheme_vacancy_raw import VacancyOut


class TestCsv:
    """Test write csv
    """

    async def test_csv_write(self):
        """Test csv write
        """
        v = [dict(**VacancyOut.Config.json_schema_extra['example']), ]
        async with TemporaryFile('w+') as f:
            result = await get_vacancy_csv(v, f)
            async for line in result:
                if "area" in line:
                    continue
                assert VacancyOut.Config.json_schema_extra['example']['area'] in line, \
                    'wrong result'

    async def test_csv_empty_write(self):
        """Test csv write with empty field
        """
        v = [dict(**VacancyOut.Config.json_schema_extra['example']), ]
        v[0]['area'] = None
        async with TemporaryFile('w+') as f:
            result = await get_vacancy_csv(v, f)
            async for line in result:
                if "area" in line:
                    continue
                assert VacancyOut.Config.json_schema_extra['example']['area'] not in line, \
                    'wrong result'
