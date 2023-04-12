import asyncio
from redis.asyncio import Redis
from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pymongo.client_session import ClientSession
from app.core import SessionMaker, HhruQueries, HhruQueriesDb, check_user, parse_vacancy
from app.tasks.worker import get_vacancy
from app.db import get_session, get_redis_connection
from app.schemas import (
    VacancyRequest,
    Vacancies,
        )
from app.crud import templates, vacancies, VacancyResponseInDb
from app.config import settings


router = APIRouter()


@router.get(
    "/get_new_vacancies_with async_query",
    status_code=status.HTTP_200_OK,
    summary='Request for vacancies data',
    response_description="OK. Requested data.",
    response_model=Vacancies,
    responses=settings.ERRORS
        )
async def ask_for_new_vacancies(
    user_id: int,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> Vacancies:
    """Request for vacancies data
    """
    user = await check_user(db, user_id)
    template = await templates.get(
        db, {'name': template_name, 'user': str(user['_id'])}
            )

    if template:
        params = VacancyRequest(**template)
        queries = HhruQueries(SessionMaker, "https://api.hh.ru/vacancies", params)
        all_v = await queries.vacancies_query(db)

        if all_v['not_in_db']:

            await vacancies.create_many(
                db,
                [
                    VacancyResponseInDb(v_id=key, **val)
                    for key, val
                    in all_v['not_in_db'].items()
                        ]
                    )
            return Vacancies(vacancies=all_v['not_in_db'])

        else:

            raise HTTPException(
                status_code=404,
                detail="New vacancy not found."
                    )

    else:

        raise HTTPException(
            status_code=404,
            detail="Template not found."
                )


@router.get(
    "/get_new_vacancies_with_redis",
    status_code=status.HTTP_202_ACCEPTED,
    summary='Request for vacancies data',
    response_description="Accepted to request hh.ru for vacancies",
    responses=settings.ERRORS
        )
async def ask_for_new_vacancies(
    user_id: int,
    template_name: str,
    background_tasks: BackgroundTasks,
    db: ClientSession = Depends(get_session),
    redis_db: Redis = Depends(get_redis_connection)
        ) -> Vacancies:
    """Request for vacancies data
    """
    user = await check_user(db, user_id)
    template = await templates.get(
        db, {'name': template_name, 'user': str(user['_id'])}
            )

    if template:
        params = VacancyRequest(**template)
        queries = HhruQueriesDb(SessionMaker, "https://api.hh.ru/vacancies", params)
        background_tasks.add_task(parse_vacancy, queries, db, redis_db)

    else:
        raise HTTPException(
            status_code=404,
            detail="Template not found."
                )


@router.get(
    "/Get_new_vacancies_with_celery",
    status_code=status.HTTP_201_CREATED,
    summary='Request for vacancies data',
    response_description="OK. Requested data.",
    responses=settings.ERRORS
        )
async def ask_hhru_api_and_stroe_to_db_result(
    user_id: int,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> Vacancies:
    """Request for vacancies data and store it to db
    """
    user = await check_user(db, user_id)
    template = await templates.get(
        db, {'name': template_name, 'user': str(user['_id'])}
            )

    if template:
        params = VacancyRequest(**template).dict()
        task = get_vacancy("https://api.hh.ru/vacancies", params)
        return JSONResponse(status_code=201, content={"status": 200, "message": f"You post {task}"})

    else:
        raise HTTPException(
            status_code=404,
            detail="Template not found."
                )
