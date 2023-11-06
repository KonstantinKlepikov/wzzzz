import asyncio
from typing import Any, Sequence
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from pymongo.results import InsertOneResult
from app.config import settings
from app.crud.crud_base import CRUDBase
from app.schemas.scheme_vacancy_raw import VacancyRawData
from app.schemas.constraint import Collections


class CRUDVacanciesRaw(CRUDBase[VacancyRawData]):
    """Vacancies crud
    """

    async def get_many_by_ids(  # TODO: test me
        self,
        db: ClientSession,
        ids: Sequence[int]
            ) -> list[dict[str, Any]]:
        """Get vacancies from db bay list of ids

        Args:
            db (ClientSession): session
            ids (list[int]): ids list

        Returns:
            list[dict[str, Any]]: vacancies
        """
        tasks = [
            asyncio.create_task(self.get(db, {'id': i}))
            for i in ids
                ]
        await asyncio.wait(tasks)
        return [task.result() for task in tasks if task.result()]

    async def create_many(  # TODO: test me
        self,
        db: ClientSession,
        obj_in: Sequence[VacancyRawData],
            ) -> list[InsertOneResult]:
        """Create many vacancy documents

        Args:
            db (ClientSession): session
            obj_in (Sequence[VacancyRawData]): sequence of data

        Returns:
            list[InsertOneResult]: results
        """
        tasks = [self.create(db, i) for i in obj_in]  # FIXME: use raw_id insted od id for db save. Add create_raw method
        result = await asyncio.gather(*tasks, return_exceptions=True)
        return [res for res in result if not isinstance(res, DuplicateKeyError)]


vacancies_simple_raw = CRUDVacanciesRaw(
    schema=VacancyRawData,
    col_name=Collections.VACANCIES_SIMPLE_RAW.value,
    db_name=settings.DB_NAME,
        )

vacancies_deep_raw = CRUDVacanciesRaw(
    schema=VacancyRawData,
    col_name=Collections.VACANCIES_DEEP_RAW.value,
    db_name=settings.DB_NAME,
        )
