from aiofiles.tempfile import TemporaryFile
from app.core import get_vacancy_csv
from app.schemas import AllVacancies, Vacancy


class TestCsv:
    """Test write csv
    """

    async def test_csv_write(self):
        """Test csv write
        """
        v = AllVacancies(**AllVacancies.Config.json_schema_extra['example'])
        async with TemporaryFile('w+') as f:
            result = await get_vacancy_csv(v.dict()['vacancies'], f)
            async for line in result:
                if "area" in line:
                    continue
                assert Vacancy.Config.json_schema_extra['example']['area'] in line, \
                    'wrong result'

    async def test_csv_empty_write(self):
        """Test csv write with empty field
        """
        v = AllVacancies(**AllVacancies.Config.json_schema_extra['example'])
        v.vacancies[0].area = None
        async with TemporaryFile('w+') as f:
            result = await get_vacancy_csv(v.dict()['vacancies'], f)
            async for line in result:
                if "area" in line:
                    continue
                assert Vacancy.Config.json_schema_extra['example']['area'] not in line, \
                    'wrong result'
