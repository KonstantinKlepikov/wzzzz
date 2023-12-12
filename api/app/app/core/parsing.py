import asyncio
from typing import Any
from bs4 import BeautifulSoup as bs
from pymongo.client_session import ClientSession
from app.crud.crud_vacancy_raw import CRUDVacanciesRaw
from app.schemas.scheme_vacancy_raw import VacancyOut


class VacanciesParser:
    """Parse vacancies
    """

    def __init__(
            self,
            db: ClientSession,
            simple: CRUDVacanciesRaw,
            deep: CRUDVacanciesRaw,
            ids: list[int]
                ) -> None:
        """Parse vacancies

        Args:
            db (ClientSession): session
            simple (CRUDVacanciesRaw): simple crud
            deep (CRUDVacanciesRaw): deep crud
            ids (list[int]): v_ids list
        """
        self.db = db
        self.simple = simple
        self.deep = deep
        self.ids = ids

    @staticmethod
    def _field_to_list(x: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
        """Make list ov values from response field

        Args:
            x (VacancyRaw): vacancy

        Returns:
            list[Any]: transformed data
        """
        if x:
            if isinstance(x[0], dict):
                items = [i['name'] for i in x]
                return items
            else:
                return [x, ]
        return []

    @staticmethod
    def _field_to_value(x: dict[str, Any] | None) -> Any:
        """Get value from response field

        Args:
            x (VacancyRaw): vacancy raw

        Returns:
            Any: transformed data
        """
        if x:
            if isinstance(x, dict):
                return x.get('name')
            return x
        return None

    @staticmethod
    def _html_to_text(x: dict[str, Any] | None) -> str | None:
        """Transform html to text

        Args:
            x (str): html text

        Returns:
            str: text without tags
        """
        if x:
            soup = bs(x, features="html.parser")
            text = soup.get_text()
            return text
        return None

    async def _merged_vacancy(  # TODO: test me
        self, id: int) -> tuple[dict[str, Any], dict[str, Any]]:
        """Get simple and deep part of data

        Args:
            id (int): v_id

        Returns:
            tuple[dict[str, Any], dict[str, Any]]: simple and deep data
        """
        return await self.simple.get_by_v_ids(self.db, id), \
                await self.deep.get_by_v_ids(self.db, id)


    async def _get_merged_vacancies(self) -> list[dict[str, Any]]:  # TODO: test me
        """Get merget vacancies

        Returns:
         list[dict[str, Any]: merged vacancies
        """
        tasks = [self._merged_vacancy(id) for id in self.ids]
        result = await asyncio.gather(*tasks)
        print(result)
        return [dict(res[0], *res[1]) for res in result]

    async def parse(self) -> list[dict[str, Any]]:  # TODO: test me
        """Parse vacancyies raw data

        Returns:
            list[dict[str, Any]]: parsed vacancies
        """
        vac = await self._get_merged_vacancies()

        return [
                VacancyOut(
                    professional_roles=self._field_to_list(v['professional_roles']),
                    area=self._field_to_value(v['area']),
                    experience=self._field_to_value(v['expirience']),
                    description=self._html_to_text([v['description']]),
                    key_skills=self._field_to_list(v['key_skills']),
                    employer=self._field_to_value(v['employer']),
                    alternate_url=self._field_to_value(v['alternate_url']),
                        ).model_dump()
                    for v in vac
                ]
