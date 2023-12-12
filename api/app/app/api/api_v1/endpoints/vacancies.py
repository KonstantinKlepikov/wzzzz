from redis.asyncio import Redis
from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
    BackgroundTasks,
    Query,
        )
from fastapi.responses import StreamingResponse
from pymongo.client_session import ClientSession
from aiofiles.tempfile import TemporaryFile
from app.core.check import check_user
from app.core.queries import (
    HhruQueriesDb,
    HhruBaseQueries,
    get_parse_save_vacancy,
    get_vacancy,
        )
from app.core.parsing import VacanciesParser
from app.core.csv_writer import get_vacancy_csv
from app.core.http_session import SessionMaker
from app.db import get_session, get_redis_connection
from app.schemas.scheme_vacanciy import (
    VacancyRequest,
    Vacancies,
    AllVacancies,
        )
from app.schemas.constraint import Relevance
from app.crud.crud_template import templates
from app.crud.crud_vacancy import vacancies
from app.crud.crud_vacancy_raw import vacancies_deep_raw, vacancies_simple_raw
from app.config import settings


router = APIRouter()


# TODO: test me
@router.get(
    "/get",
    status_code=status.HTTP_202_ACCEPTED,
    summary='Request for vacancies data',
    response_description="Accepted to request hh.ru for vacancies",
    responses=settings.ERRORS
        )
async def ask_for_new_vacancies_with_redis(
    user_id: int,
    template_name: str,
    background_tasks: BackgroundTasks,
    db: ClientSession = Depends(get_session),
    redis_db: Redis = Depends(get_redis_connection),
    relevance: Relevance = Relevance.ALL,
        ) -> None:
    """Request for vacancies data. Call for this resource makes some operations:
    1. call hh.ru vacancy search api
    2. get 202 and wait for redis message for save vacancy data in db
    3. get a message with an vacancies ids to pub/sub channel of redis

    To get result .csv file lesson redis with user_id as channel name and
    use /get_csv resource with list of given ids
    """
    user = await check_user(db, user_id)
    template = await templates.get(
        db, {'name': template_name, 'user': str(user['_id'])}
            )

    if template:
        params = VacancyRequest(**template)
        queries = HhruBaseQueries(
            SessionMaker,
            settings.HHRU_VACANCY_URL,
            params
                )
        background_tasks.add_task(
            get_vacancy,
            user_id,
            queries,
            relevance,
            db,
            redis_db
                )

    else:
        raise HTTPException(
            status_code=404,
            detail="Template not found."
                )


# TODO: test me
# @router.get(
#     "/get_csv",
#     status_code=status.HTTP_200_OK,
#     summary='Request for vacancies csv.',
#     response_description="OK. Requested data",
#     responses=settings.ERRORS,
#         )
# async def get_vacancies_csv(
#     redis_ids: list[int] = Query(),
#     db: ClientSession = Depends(get_session),
#         ) -> None:
#     """Request for .csv file of new vacancies
#     """

#     vac = await vacancies.get_many_by_ids(db, redis_ids)
#     vac = AllVacancies(vacancies=vac).model_dump()['vacancies']
#     if vac:
#         async def iterfile():
#             async with TemporaryFile('w+') as f:
#                 result = await get_vacancy_csv(vac, f)
#                 async for line in result:
#                     yield line

#         return StreamingResponse(
#             iterfile(),
#             media_type='text/csv',
#             headers={
#                 "Content-Disposition": "attachment;filename=vacancies.csv"
#                     }
#                 )
#     else:
#         raise HTTPException(
#             status_code=404,
#             detail="Vacancies not found."
#                 )


@router.get(
    "/get_csv",
    status_code=status.HTTP_200_OK,
    summary='Request for vacancies csv.',
    response_description="OK. Requested data",
    responses=settings.ERRORS,
        )
async def get_vacancies_csv(
    redis_ids: list[int] = Query(),
    db: ClientSession = Depends(get_session),
        ) -> None:
    """Request for .csv file of new vacancies
    """

    vac = VacanciesParser(
        db,
        vacancies_simple_raw,
        vacancies_deep_raw,
        redis_ids
            )
    if vac := await vac.parse():

        async def iterfile():
            async with TemporaryFile('w+') as f:
                result = await get_vacancy_csv(vac, f)
                async for line in result:
                    yield line

        return StreamingResponse(
            iterfile(),
            media_type='text/csv',
            headers={
                "Content-Disposition": "attachment;filename=vacancies.csv"
                    }
                )
    else:
        raise HTTPException(
            status_code=404,
            detail="Vacancies not found."
                )
