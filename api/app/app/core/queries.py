import json
import asyncio
from typing import Any
from bs4 import BeautifulSoup as bs
from app.core import SessionMaker
from app.schemas import (
    VacancyRequestScheme,
    VacancyResponseScheme,
    VacanciesResponseScheme,
        )


class HhruQueries:
    """Make queries to hhru apy
    """

    def __init__(self, session: SessionMaker, url: str) -> None:
        self.session = session
        self.url = url

    @staticmethod
    def get_vacancy(vacancies: str) -> dict[str, Any]:
        return json.loads(vacancies)

    @staticmethod
    def field_to_list(x) -> list[str]:
        if x:
            if isinstance(x[0], dict):
                items = [i['name'] for i in x]
                return items
            else:
                return [x, ]
        else: return []

    @staticmethod
    def get_text(x) -> str:
        if x:
            soup = bs(x, features="html.parser")
            text = soup.get_text()
            return text
        else: return ''

    def get_vacancy_item(self, vacancy: dict[str, Any]) -> VacancyResponseScheme:
        """Get vacancy dict

        Args:
            vacancy (dict[str, Any]): _description_

        Returns:
            dict[str, Any]: _description_
        """
        result = {}
        result['vac_id'] = vacancy['id']
        for field in ['area', 'employer', ]:
            result[field] = vacancy[field]['name']
        result['alternate_url'] = vacancy['alternate_url']
        return VacancyResponseScheme(**result)

    async def vacancies_query(
        self,
        scheme: VacancyRequestScheme
            ) -> VacanciesResponseScheme:
        """Request for vacancies

        Args:
            scheme (VacanciesResponseScheme): request scheme

        Returns:
            VacancyResponseScheme: response scheme
        """
        params = json.loads(scheme.json())
        vacancies = await self.session.vacancies_query(self.url, params)
        vacancies = self.get_vacancy(vacancies)
        pages = vacancies['pages']

        result = [vacancies, ]

        if pages > 0:
            tasks = []
            for page in range(1, pages):
                params['page'] = page
                tasks.append(
                    asyncio.create_task(self.session.vacancies_query(self.url, params))
                        )

            for task in tasks:
                r = await task
                result.append(self.get_vacancy(r))

        items = []
        for item in result:
            items = items + [self.get_vacancy_item(vacancy) for vacancy in item['items']]

        return VacanciesResponseScheme(vacancies=items)

    async def go_deeper(self, scheme: VacancyResponseScheme) -> VacancyResponseScheme:
        if scheme.alternate_url:
            r = await self.session.vacancies_query(scheme.alternate_url)
            # some manipulations with scheme

        return scheme
