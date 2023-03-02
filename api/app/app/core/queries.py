import json
import asyncio
from asyncio import Semaphore
from copy import copy
from typing import Any, Optional, TypeAlias
from bs4 import BeautifulSoup as bs
from app.core import SessionMaker
from app.schemas import VacancyRequestScheme


VacancyRaw: TypeAlias = dict[str, Any]


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
        self.params = json.loads(params.json())
        # TODO: fixme. Here form dict returns dt, but need srt

    @staticmethod
    def _field_to_list(x: Optional[list[VacancyRaw] | VacancyRaw]) -> list[Any]:
        """Make list ov values from response field

        Args:
            x (VacancyRaw): vacancy raw

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
    def _field_to_value(x: Optional[VacancyRaw]) -> Optional[Any]:
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
    def _html_to_text(x: Optional[str]) -> Optional[str]:
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

    def _simple_to_dict(self, item: VacancyRaw) -> VacancyRaw:
        """Get simple vacancy dict

        Args:
            item (VacancyRaw): vacancy raw

        Returns:
            VacancyRaw: transformed vacancy raw
        """
        result = {}
        for field in ['area', 'employer', ]:
            result[field] = self._field_to_value(item.get(field))
        result['alternate_url'] = item.get('alternate_url')
        result['url'] = item.get('url')
        return result

    def _deeper_to_dict(self, item: VacancyRaw) -> VacancyRaw:
        """Get deeper vacancy dict

        Args:
            item (VacancyRaw): vacancy raw

        Returns:
            VacancyRaw: transformed vacancy raw
        """
        result = {}
        result['experience'] = self._field_to_value(item.get('experience'))
        for field in ['professional_roles', 'key_skills', ]:
            result[field] = self._field_to_list(item.get(field))
        result['description'] = self._html_to_text(item.get('description'))
        return result

    async def _make_simple_requests(
        self,
        result: VacancyRaw,
        sem: Optional[Semaphore] = None,
            ) -> list[VacancyRaw]:

        tasks = []

        for page in range(1, result['pages'] + 1):
            p = copy(self.params)
            p['page'] = page
            tasks.append(asyncio.create_task(
                self.session.get_query(url=self.url, params=p, sem=sem)
                    ))

        await asyncio.wait(tasks)
        return [result, ] + [task.result() for task in tasks]

    async def _make_deeper_requests(
        self,
        result: dict[int, VacancyRaw],
        sem: Optional[Semaphore] = None,
            ) -> list[VacancyRaw]:

        tasks = []

        for page in result.values():
            if page.get('url'):
                tasks.append(asyncio.create_task(
                    self.session.get_query(url=page['url'], sem=sem)
                        ))

        await asyncio.wait(tasks)
        return [task.result() for task in tasks]

    def _make_simple_result(
        self,
        result: list[VacancyRaw]
            ) -> dict[int, VacancyRaw]:
        """Make simple result from list of transformed response data

        Args:
            result (list[VacancyRaw]): transformed response data

        Returns:
            dict[int, VacancyRaw]: transformed data
        """
        return {
            i['id']: self._simple_to_dict(i)
            for r in result
            for i in r['items']
                }

    def _make_deeper_result(
        self,
        result: list[VacancyRaw]
            ) -> dict[int, VacancyRaw]:
        """Make deeper result from list of transformed response data

        Args:
            result (list[VacancyRaw]): transformed response data

        Returns:
            dict[int, VacancyRaw]: transformed data
        """
        return {r['id']: self._deeper_to_dict(r) for r in result}

    @staticmethod
    def _update(
        simple: dict[int, VacancyRaw],
        deeper: dict[int, VacancyRaw]
            ) -> dict[int, VacancyRaw]:
        for key in simple.keys():
            if deeper.get(key):
                simple[key].update(deeper[key])
        return simple

    async def vacancies_query(self) -> VacancyRaw:
        """Request for vacancies

        Returns:
            VacancyRaw:: transformed response data
        """
        semaphore = Semaphore(10)
        entry = await self.session.get_query(
            url=self.url,
            params=self.params,
            sem=semaphore
                )
        simple = await self._make_simple_requests(entry, semaphore)
        simple = self._make_simple_result(simple)
        deeper = await self._make_deeper_requests(simple, semaphore)
        deeper = self._make_deeper_result(deeper)

        return self._update(simple, deeper)
