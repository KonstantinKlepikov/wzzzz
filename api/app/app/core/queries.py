import json
import asyncio
from asyncio import Semaphore
from itertools import chain
from datetime import datetime
from redis.asyncio import Redis
from copy import copy
from pymongo.client_session import ClientSession
from typing import Any, Optional, TypeAlias, Coroutine
from bs4 import BeautifulSoup as bs
from app.core.http_session import SessionMaker
from app.schemas.scheme_vacanciy import VacancyRequest, VacancyResponseInDb
from app.schemas.constraint import Relevance
from app.schemas.scheme_vacancy_raw import VacancyRawData
from app.crud.crud_vacancy import vacancies, CRUDVacancies
from app.crud.crud_vacancy_raw import vacancies_simple_raw, vacancies_deep_raw


VacancyRaw: TypeAlias = dict[str, Any]


class HhruBaseQueries:
    """Query a hh.ru for vacancies raw data
    and save it to db, if not exist

    Atrs:
        session (SessionMaker): aiohttp session
        url (str): url for entry query
        params (VacancyRequest): vacancy query parameters
    """
    def __init__(
        self,
        session: SessionMaker,
        url: str,
        params: VacancyRequest
            ) -> None:
        self.session = session
        self.url = url
        self.params = json.loads(params.model_dump_json(exclude_none=True))

    # TODO: write to db raw, use raw data without schema
    @staticmethod
    def _make_schema(data: list[VacancyRaw]) -> list[VacancyRawData]:
        """Add timestamp to data before add it to db

        Args:
            data (list[VacancyRaw]): vacancies data

        Returns:
            list[VacancyRawData]: transformed data
        """
        ts = {'ts': datetime.utcnow()}
        return [VacancyRawData(id=d['id'], ts=ts, raw=d) for d in data]

    async def _make_simple_requests(
        self,
        sem: Semaphore | None = None,
            ) -> list[VacancyRaw]:  # TODO: test me
        """Make simple result of query. Here is all pages returned from
        https://api.hh.ru/vacancies

        In this function we use firsc (entry) query to get pages for
        subsequent requests. Then, we get all responses, even if it fail
        and filter failed responsses and return only correct.

        Args:
            sem (Semaphore, optional): semaphore option for prevent
                                       server overwelming. Defaults to None.

        Returns:
            list[VacancyRaw]: simple vacanices responces
        """

        tasks: list[Coroutine] = []
        entry = await self.session.get_query(url=self.url, params=self.params)
        # FIXME: if error?

        for page in range(1, entry['pages'] + 1):
            p = copy(self.params)
            p['page'] = page
            tasks.append(self.session.get_query(url=self.url, params=p, sem=sem))

        result = await asyncio.gather(*tasks, return_exceptions=True)
        return [entry, ] + [res for res in result if not isinstance(res, Exception)]

    async def _make_deeper_requests(
        self,
        urls: list[str],
        sem: Optional[Semaphore] = None,
            ) -> list[VacancyRaw]:  # TODO: test me
        """Make requests for deeper vacancy data

        Args:
            urls (list[str]): simple requests urls
            sem (Semaphore, optional): semaphore option for prevent
                            server overwelming. Defaults to None.

        Returns:
            list[VacancyRaw]: deeper vacancy responses
        """
        tasks: list[Coroutine] = []

        for url in urls:
            tasks.append(self.session.get_query(url=url, sem=sem))

        result = await asyncio.gather(*tasks, return_exceptions=True)
        return [res for res in result if not isinstance(res, Exception)]

    async def query(self, db: ClientSession) -> None:  # TODO: test me
        """Request for vacancies

        Args:
            db (ClientSession): session
        """
        semaphore = Semaphore(10)
        simple = await self._make_simple_requests(semaphore)
        ids = [d['id'] for d in simple]
        deep = await self._make_deeper_requests(ids, semaphore)

        simple_db = await vacancies_simple_raw.create_many(db, self._make_schema(simple)) # FIXME: use raw_id insted od id for db save
        deep_db = await vacancies_deep_raw.create_many(db, self._make_schema(deep)) # FIXME: use raw_id insted od id for db save

        # TODO: send simple to deeper as it available
        # TODO: transform data and save transformed...
        # or return data for transformation



# FIXME: remove me
class HhruQueriesDb:
    """"""

    def __init__(
        self,
        session: SessionMaker,
        url: str,
        params: VacancyRequest
            ) -> None:
        self.session = session
        self.url = url
        self.params = json.loads(params.json(exclude_none=True))
        self.result: tuple[list[int], VacancyRaw] = ([], {})

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
            ) -> list[list[int], VacancyRaw]:
        """Make simple result from list of transformed response data

        Args:
            db (ClientSession): session
            result (list[VacancyRaw]): transformed response data

        Returns:
            list[list[int], VacancyRaw]: transformed data
        """
        ids = [int(i['id']) for r in result for i in r['items']]
        in_db = [i['v_id'] for i in await vacancies.get_many_by_ids(db, ids)]

        not_in_db = {
            i['id']: self._simple_to_dict(i)
            for r in result
            for i in r['items']
            if int(i['id']) not in in_db
                }

        return [in_db, not_in_db]

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

    async def vacancies_query(self, db: ClientSession, entry: VacancyRaw) -> None:
        """Request for vacancies

        Args:
            db (ClientSession): session
            entry (VacancyRaw): raw entry response - this is
                                response to get number of pages

        Returns:
            dict(str, VacancyRaw): transformed response data
        """
        semaphore = Semaphore(10)
        simple = await self._make_simple_requests(entry, semaphore)
        self.result = await self._make_simple_result(db, simple)

        if self.result[1]:
            deeper = await self._make_deeper_requests(
                self.result[1], semaphore
                    )
            deeper_result = self._make_deeper_result(deeper)
            self.result[1] = self._update(
                self.result[1], deeper_result
                    )

    async def save_to_db(self, db: ClientSession) -> None:
        """Save vacancies to db

        Args:
            db (ClientSession): database session
        """
        if self.result[1]:

            await vacancies.create_many(
                db,
                [
                    VacancyResponseInDb(v_id=key, **val)
                    for key, val
                    in self.result[1].items()
                        ]
                    )

# FIXME: remove me
async def get_parse_save_vacancy(
    user_id: int,
    queries: HhruQueriesDb,
    entry: VacancyRaw,
    relevance: Relevance,
    db: ClientSession,
    redis_db: Redis
        ) -> None:
    """Get vacancy by api, parse it, save to db and add to redis pubsub

    Args:
        user_id (int): user id
        queries (HhruQueriesDb): hhru query instance
        entry (VacancyRaw): raw entry response - this is
                            response to get number of pages
        relevance (Relevance): relevance of returned content
        db (ClientSession): mongo session
        redis_db (Redis): redis connection
    """
    await queries.vacancies_query(db, entry)
    await queries.save_to_db(db)
    # TODO: test this case
    if relevance == Relevance.NEW:
        m = ' '.join([str(key) for key in queries.result[1].keys()])
    if relevance == Relevance.ALL:
        m = ' '.join([
            str(key) for key
            # NOTE: is that right for asyncio?
            in chain(queries.result[0], queries.result[1].keys())
                ])
    await redis_db.publish(str(user_id), m)
