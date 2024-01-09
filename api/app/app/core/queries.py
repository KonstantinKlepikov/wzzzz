import json
import asyncio
from asyncio import Semaphore
from itertools import chain
from redis.asyncio import Redis
from copy import copy
from pymongo.client_session import ClientSession
from typing import Any, Optional, TypeAlias, Coroutine
from fastapi import HTTPException
from bs4 import BeautifulSoup as bs
from app.core.http_session import SessionMaker
from app.schemas.constraint import Relevance
from app.schemas.scheme_vacancy import VacancyData, VacancyRequest
from app.crud.crud_vacancy import vacancies_simple, vacancies_deep
from app.config import settings


Vacancy: TypeAlias = dict[str, Any]


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

    async def _make_entry(self):
        """Get entry page for request
        """
        return await self.session.get_query(url=self.url, params=self.params)

    @staticmethod
    def _clean_simple_response(
        data: list[dict[str, Any] | HTTPException]
            ) -> list[VacancyData]:
        """Get responses without errors

        Args:
            data (list[dict[str, Any] | HTTPException]): responses

        Returns:
            list[VacancyData]: vacancies
        """
        result = []
        for nested in data:
            if not isinstance(nested, Exception):
                for res in nested['items']:
                    result.append(VacancyData(**res))
        return result

    async def _make_simple(
        self,
        sem: Semaphore | None = None,
            ) -> list[VacancyData]:
        """Make simple result of query. Here is all pages returned from
        https://api.hh.ru/vacancies

        In this function we use firsc (entry) query to get pages for
        subsequent requests. Then, we get all responses, even if it fail
        and filter failed responsses and return only correct.

        Args:
            sem (Semaphore, optional): semaphore option for prevent
                server overwelming. Defaults to None.

        Returns:
            list[VacancyData]: simple vacanices responces
        """

        tasks: list[Coroutine] = []
        entry = await self._make_entry()

        for page in range(1, entry['pages'] + 1):
            p = copy(self.params)
            p['page'] = page
            tasks.append(self.session.get_query(url=self.url, params=p, sem=sem))

        result = await asyncio.gather(*tasks, return_exceptions=True)
        return self._clean_simple_response([entry, ] + result)

    async def _make_deep(
        self,
        urls: list[str],
        sem: Optional[Semaphore] = None,
            ) -> list[VacancyData]:
        """Make requests for deep vacancy data

        Args:
            urls (list[str]): simple requests urls
            sem (Semaphore, optional): semaphore option for prevent
                server overwelming. Defaults to None.

        Returns:
            list[VacancyData]: deeper vacancy responses
        """
        tasks = [self.session.get_query(url=url, sem=sem) for url in urls]
        result = await asyncio.gather(*tasks, return_exceptions=True)
        return [
            VacancyData(**res)
            for res in result
            if not isinstance(res, Exception)
                ]

    async def query(
        self,
        db: ClientSession,
        sem: int = settings.SEM
            ) -> tuple[list[int], list[int]]:
        """Request for vacancies

        Args:
            db (ClientSession): session
            sem (int), default to settings.SEM: senaphore in seconds

        Returns:
            tuple[list[int], list[int]]: all v_ids of vacancies and not existed v_ids
        """
        semaphore = Semaphore(sem)
        simple = await self._make_simple(semaphore)

        v_ids = {d.id for d in simple}
        notexisted_v_ids = await vacancies_simple.get_many_notexisted_v_ids(db, v_ids)
        urls = [d.url for d in simple if d.id in notexisted_v_ids]

        deep = await self._make_deep(urls, semaphore)

        await vacancies_simple.create_many(db, simple)
        await vacancies_deep.create_many(db, deep)

        return list(v_ids), list(notexisted_v_ids)


async def get_vacancy(
    user_id: int,
    queries: HhruBaseQueries,
    relevance: Relevance,
    db: ClientSession,
    redis_db: Redis
        ) -> None:
    """Get vacancy by api, parse it, save to db and add to redis pubsub

    Args:
        user_id (int): user id
        queries (HhruBaseQueries): hhru query instance
        relevance (Relevance): relevance of returned content
        db (ClientSession): mongo session
        redis_db (Redis): redis connection
    """
    ids = await queries.query(db)
    if relevance == Relevance.NEW:
        m = ' '.join([str(i) for i in ids[1]])
    if relevance == Relevance.ALL:
        m = ' '.join([str(i) for i in ids[0]])
    await redis_db.publish(str(user_id), m)
