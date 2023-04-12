import json
import asyncio
from asyncio import Semaphore
from redis.asyncio import Redis
from copy import copy
from pymongo.client_session import ClientSession
from typing import Any, Optional, TypeAlias
from bs4 import BeautifulSoup as bs
from app.core import SessionMaker
from app.schemas import VacancyRequest, VacancyResponseInDb, Vacancies
from app.crud import vacancies


VacancyRaw: TypeAlias = dict[str, Any]


class HhruQueries:
    """Make queries to hhru api
    """

    def __init__(
        self,
        session: SessionMaker,
        url: str,
        params: VacancyRequest
            ) -> None:
        self.session = session
        self.url = url
        self.params = json.loads(params.json(exclude_none=True))
        # TODO: fixme. Here form dict returns dt, but need str

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

    async def _make_simple_result(
        self,
        db: ClientSession,
        result: list[VacancyRaw],
            ) -> dict[str, dict[int, VacancyRaw]]:
        """Make simple result from list of transformed response data

        Args:
            db (ClientSession): session
            result (list[VacancyRaw]): transformed response data

        Returns:
            dict[str, dict[int, VacancyRaw]]: transformed data
        """
        ids = [int(i['id']) for r in result for i in r['items']]

        result_in_db = await vacancies.get_many_by_ids(db, ids)

        in_db = {
            i['v_id']: self._simple_to_dict(i)
            for i in result_in_db
                }

        not_in_db = {
            i['id']: self._simple_to_dict(i)
            for r in result
            for i in r['items']
            if int(i['id']) not in in_db.keys()
                }

        return {'in_db': in_db, 'not_in_db': not_in_db}

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

    async def vacancies_query(self, db: ClientSession,) -> dict[str, VacancyRaw]:
        """Request for vacancies

        Args:
            db (ClientSession): session

        Returns:
            dict(str, VacancyRaw): transformed response data
        """
        semaphore = Semaphore(10)
        entry = await self.session.get_query(
            url=self.url,
            params=self.params,
            sem=semaphore
                )
        simple = await self._make_simple_requests(entry, semaphore)
        simple_result = await self._make_simple_result(db, simple)

        if simple_result['not_in_db']:
            deeper = await self._make_deeper_requests(
                simple_result['not_in_db'], semaphore
                    )
            deeper_result = self._make_deeper_result(deeper)

            return {
                'in_db': simple_result['in_db'],
                'not_in_db': self._update(simple_result['not_in_db'], deeper_result)
                    }
        else:

            return {
                'in_db': simple_result['in_db'],
                'not_in_db': {}
                    }


class HhruQueriesDb(HhruQueries):

    def __init__(self, session: SessionMaker, url: str, params: VacancyRequest) -> None:
        super().__init__(session, url, params)
        self.result: dict[str, VacancyRaw] = {'in_db': {}, 'not_in_db': {}}

    async def vacancies_query(self, db: ClientSession,) -> None:
        """Request for vacancies

        Args:
            db (ClientSession): session

        Returns:
            dict(str, VacancyRaw): transformed response data
        """
        semaphore = Semaphore(10)
        entry = await self.session.get_query(
            url=self.url,
            params=self.params,
            sem=semaphore
                )
        simple = await self._make_simple_requests(entry, semaphore)
        simple_result = await self._make_simple_result(db, simple)

        self.result['in_db'] = simple_result['in_db']
        if simple_result['not_in_db']:
            deeper = await self._make_deeper_requests(
                simple_result['not_in_db'], semaphore
                    )
            deeper_result = self._make_deeper_result(deeper)
            self.result['not_in_db'] = self._update(
                simple_result['not_in_db'], deeper_result
                    )

    async def save_to_db(self, db: ClientSession) -> None:
        """Save vacancies to db

        Args:
            db (ClientSession): database session
        """
        if self.result['not_in_db']:

            await vacancies.create_many(
                db,
                [
                    VacancyResponseInDb(v_id=key, **val)
                    for key, val
                    in self.result['not_in_db'].items()
                        ]
                    )


async def parse_vacancy(
    user_id: int,
    queries: HhruQueriesDb,
    db: ClientSession,
    redis_db: Redis
        ) -> None:
    """Get vacancy by api, parse it, save to db and add to redis pubsub

    Args:
        queries (HhruQueriesDb): hhru query instance
        db (ClientSession): mongo session
        redis_db (Redis): redis connection
    """
    await queries.vacancies_query(db)
    await queries.save_to_db(db)
    m = Vacancies(vacancies=queries.result['not_in_db']).json()
    await redis_db.publish(str(user_id), m)

    # async with redis_db.pubsub() as pubsub:
    #     await pubsub.subscribe('vacancies')
    #     while True:
    #         message = await pubsub.get_message(ignore_subscribe_messages=True)
    #         if message:
    #             print(message)
    #             break
    #         await asyncio.sleep(0.001)

    #         await redis_db.publish('vacancies', m)
