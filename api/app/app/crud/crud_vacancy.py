import asyncio
from typing import Any, Sequence
from pymongo.client_session import ClientSession
from pymongo.results import InsertOneResult
from app.config import settings
from app.crud import CRUDBase
from app.schemas import VacancyResponseInDb, Collections


class CRUDVacancies(CRUDBase[VacancyResponseInDb]):
    """Vacancies crud
    """

    async def get_many_by_ids(
        self,
        db: ClientSession,
        ids: Sequence[int]
            ) -> list[dict[str, Any]]:
        """Get vacancies from db bay list of ids

        Args:
            db (ClientSession): session
            ids (list[int]): ids list

        Returns:
            dict[str, Any]: _description_
        """
        tasks = [
            asyncio.create_task(self.get(db, {'v_id': i}))
            for i in ids
                ]
        await asyncio.wait(tasks)
        return [task.result() for task in tasks if task.result()]

    async def create_many(
        self,
        db: ClientSession,
        obj_in: list[VacancyResponseInDb],
            ) -> list[InsertOneResult]:
        """Create many vacancy documents

        Args:
            db (ClientSession): session
            obj_in (list[VacancyResponseInDb]): list of data

        Returns:
            list[InsertOneResult]: results
        """
        tasks = [asyncio.create_task(self.create(db, i)) for i in obj_in]
        await asyncio.wait(tasks)

        return [task.result() for task in tasks]


vacancies = CRUDVacancies(
    schema=VacancyResponseInDb,
    col_name=Collections.VACANCIES.value,
    db_name=settings.DB_NAME,
        )

# TODO: add vacancies raw crud
