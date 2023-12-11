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

    async def create_raw(
        self,
        db: ClientSession,
        obj_in: VacancyRawData
            ) -> InsertOneResult:
        """Create raw vacancy document

        Args:
            db (ClientSession): session
            obj_in (VacancyRawData): scheme to creare

        Returns:
            InsertOneResult: result of creation
        """
        return await db.client[self.db_name][self.col_name] \
            .insert_one(obj_in.model_dump(by_alias=True))

    async def get_by_v_ids(  # TODO: test me
        self,
        db: ClientSession,
        id: int
            ) -> dict[str, Any]:  # FIXME: here is a scheme
        """Get vacancies from db bay list of ids

        Args:
            db (ClientSession): session
            id (int): v_ids

        Returns:
            dict[str, Any]: vacancies
        """
        data = db.client[self.db_name][self.col_name].find_one({'v_id': id})
        return data

    async def get_many_by_v_ids(
        self,
        db: ClientSession,
        ids: Sequence[int]
            ) -> list[dict[str, Any]]:  # FIXME: here is a scheme
        """Get vacancies from db bay list of ids

        Args:
            db (ClientSession): session
            ids (list[int]): v_ids list

        Returns:
            list[dict[str, Any]]: vacancies
        """
        data = db.client[self.db_name][self.col_name].find(
            {'v_id': {'$in': list(ids)}}
                )
        return await data.to_list(length=len(ids))

    async def get_many_notexisted_v_ids(
        self,
        db: ClientSession,
        v_ids: set[int],
            ) -> set[int]:
        """Get not existed raw vacancies ids by list of ids

        Args:
            db (ClientSession): session
            ids (set[int]): ids

        Returns:
            set[int]: noteisted vacancies ids
        """
        exist = set()
        async for data in db.client[self.db_name][self.col_name].find(
            {'v_id': {'$in': list(v_ids)}}, { "v_id": 1 }
                ):
            exist.add(data['v_id'])
        return v_ids.symmetric_difference(exist)

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
        tasks = [self.create_raw(db, i) for i in obj_in]
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
