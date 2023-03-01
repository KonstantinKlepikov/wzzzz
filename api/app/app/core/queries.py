import json
import asyncio
from copy import copy
from typing import Any, Optional
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

    def __init__(
        self,
        session: SessionMaker,
        url: str,
        params: VacancyRequestScheme
            ) -> None:
        self.session = session
        self.url = url
        self.params = json.loads(params.json()) #TODO: fixme. Here form dict returns dt, but need srt

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

    def simple_to_scheme(self, item: dict[str, Any]) -> VacancyResponseScheme:
        """Get vacancy scheme

        Args:
            vacancy (dict[str, Any]): _description_

        Returns:
            dict[str, Any]: _description_
        """
        result = {}
        result['vac_id'] = item['id']
        for field in ['area', 'employer', ]:
            result[field] = item[field]['name']
        result['alternate_url'] = item['alternate_url']
        result['url'] = item['url']
        return VacancyResponseScheme(**result)


    def deeper_to_scheme(self) -> VacancyResponseScheme:
        """_summary_

        Returns:
            VacancyResponseScheme: _description_
        """


    async def make_simple_requests(self, entry):

        tasks = []

        for page in range(1, entry['pages'] + 1):
            p = copy(self.params)
            p['page'] = page
            tasks.append(asyncio.create_task(
                self.session.get_query(self.url, p)
                    ))

        for task in tasks:
            await task

        return [task.result() for task in tasks]


    async def make_deeper_requests(self, entry):

        tasks = []

        for page in entry:
            if page.url:
                tasks.append(asyncio.create_task(
                    self.session.get_query(page.url)
                        ))

        for task in tasks:
            await task

        return [task.result() for task in tasks]


    async def vacancies_query(self) -> VacanciesResponseScheme:
        """Request for vacancies

        Args:
            request_scheme (VacanciesResponseScheme): request scheme

        Returns:
            VacancyResponseScheme: response scheme
        """
        entry = await self.session.get_query(self.url, self.params)

        result = await self.make_simple_requests(json.loads(entry))

        result = [
            self.simple_to_scheme(i)
            for r in result
            for i in json.loads(r)['items']
                ]

        # result2 = []
        # tasks = []
        # for page in result:
        #     if page.url:
        #         tasks.append(asyncio.create_task(
        #             self.go_simple(result2, page.url)
        #                 ))

        # for task in tasks:
        #     await task

        return VacanciesResponseScheme(vacancies=result)
