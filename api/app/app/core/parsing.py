from typing import Any
from bs4 import BeautifulSoup as bs
from pymongo.client_session import ClientSession
from app.crud.crud_vacancy import CRUDVacancies, CRUDVacanciesSimple
from app.schemas.scheme_vacancy import VacancyOut


class VacanciesParser:
    """Parse vacancies
    """

    def __init__(
            self,
            db: ClientSession,
            simple: CRUDVacanciesSimple,
            deep: CRUDVacancies,
            v_ids: list[int]
                ) -> None:
        """Parse vacancies

        Args:
            db (ClientSession): session
            simple (CRUDVacanciesSimple): simple crud
            deep (CRUDVacancies): deep crud
            v_ids (list[int]): v_ids list
        """
        self.db = db
        self.simple = simple
        self.deep = deep
        self.v_ids = v_ids

    @staticmethod
    def _field_to_list(x: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
        """Make list ov values from response field

        Args:
            x (list[dict[str, Any]] | None): field

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
            x (dict[str, Any] | None): field

        Returns:
            Any: transformed data
        """
        if x:
            if isinstance(x, dict):
                return x.get('name')
            return x
        return None

    @staticmethod
    def _html_to_text(x: str) -> str | None:
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

    async def _merged_vacancies(self) -> list[dict[str, Any]]:  # TODO: test me
        """Get merget vacancies

        Returns:
            list[dict[str, Any]: merged vacancies
        """
        return await self.simple.get_many_merged_by_v_ids(self.db, self.v_ids)

    async def parse(self) -> list[dict[str, Any]]:  # TODO: test me
        """Parse vacancyies raw data

        Returns:
            list[dict[str, Any]]: parsed vacancies
        """
        vac = await self._merged_vacancies()

        return [
                VacancyOut(
                    professional_roles=self._field_to_list(v.get('professional_roles')),
                    area=self._field_to_value(v.get('area')),
                    experience=self._field_to_value(v.get('experience')),
                    description=self._html_to_text(v.get('description')),
                    key_skills=self._field_to_list(v.get('key_skills')),
                    employer=self._field_to_value(v.get('employer')),
                    alternate_url=self._field_to_value(v.get('alternate_url')),
                        ).model_dump()
                    for v in vac
                ]
