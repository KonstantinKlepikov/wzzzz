from fastapi import APIRouter, status, Depends, HTTPException
from pymongo.client_session import ClientSession
from app.core import SessionMaker, HhruQueries, check_user
from app.db import get_session
from app.schemas import (
    VacancyRequest,
    Vacancies,
        )
from app.crud import templates, vacancies, VacancyResponseInDb
from app.config import settings


router = APIRouter()


@router.get(
    "/new",
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
