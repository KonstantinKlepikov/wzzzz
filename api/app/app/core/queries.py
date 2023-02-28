import json
import asyncio
from asyncio import Event, Task
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
        request_scheme: VacancyRequestScheme
            ) -> VacanciesResponseScheme:
        """Request for vacancies

        Args:
            request_scheme (VacanciesResponseScheme): request scheme

        Returns:
            VacancyResponseScheme: response scheme
        """
        params = json.loads(request_scheme.json())
        vacancies = await self.session.get_query(self.url, params)
        vacancies = json.loads(vacancies)

        # if vacancies['pages'] > 0:
        #     tasks = []
        #     for page in range(1, vacancies['pages']):
        #         params['page'] = page
                # tasks.append(
                #     asyncio.create_task(self.session.get_query(self.url, params))
                #         )

        # for task in tasks:
        #         r = await task
        #         result.append(json.loads(r))

        # items = []
        # for item in result:
        #     items = items + [self.get_vacancy_item(vacancy) for vacancy in item['items']]

        works = {}
        results = {}

        for num, page in enumerate(range(vacancies['pages'])):

            params['page'] = page
            e = Event()
            # t1 = asyncio.create_task(
            #     self.session.get_query(self.url, params)
            #         )
            t1 = asyncio.create_task(
                self.go_simple(num, results, params)
                    )
            t2 = asyncio.create_task(
                self.go_deeper(num, results, e)
                    )
            works[num] = (e, t1, t2)

            # work['event' + str(num)] = Event()
            # work['task' + str(num)] = asyncio.create_task(
            #     self.session.get_query(self.url, params)
            #         )
            # work['task_deep' + str(num)] = asyncio.create_task(
            #     self.go_deeper(work['result' + str(num)], work['event' + str(num)])
            #         )

        for work in works.values():
            await work[1]
            work[0].set()
            await work[2]

        # for num, work in enumerate(works):
        #     result.append(json.loads(work['result' + str(num)]))

        responses = []

        for result in results.values():
            responses.append(json.loads(result))

        # items = []
        # for item in result:
        #     items = items + [self.get_vacancy_item(vacancy) for vacancy in item['items']]

        return VacanciesResponseScheme(vacancies=responses)

    async def go_simple(
        self,
        num: int,
        results: dict[str, VacancyResponseScheme],
        params: dict[str, Any],
            ) -> None:

        r = await self.session.get_query(self.url, params)
        import pprint
        pprint.pprint(json.loads(r))

        results[num] = self.get_vacancy_item(json.loads(r))

    async def go_deeper(
        self,
        num: int,
        results: dict[str, VacancyResponseScheme],
        event: Event
            ) -> None:

        await event.wait()

        if results[num].url:
            r = await self.session.get_query(results[num].url)
            # some manipulations with scheme
