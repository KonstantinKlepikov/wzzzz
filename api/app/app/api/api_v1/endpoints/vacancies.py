from fastapi import APIRouter, status, Depends, HTTPException
from pymongo.client_session import ClientSession
from app.core import SessionMaker, HhruQueries, check_user
from app.db import get_session
from app.schemas import (
    VacancyRequest,
    Vacancies,
        )
from app.crud import templates
from app.config import settings


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary='Request for vacancies data',
    response_description="OK. Requested data.",
    response_model=Vacancies,
    responses=settings.ERRORS
        )
async def vacancies(
    login: int,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> Vacancies:
    """Request for vacancies data
    """
    user = await check_user(db, login)
    template = await templates.get(db, {'name': template_name, 'user': str(user['_id'])})
    if template:
        params = VacancyRequest(**template)
        queries = HhruQueries(SessionMaker, "https://api.hh.ru/vacancies", params)
        vacancies = await queries.vacancies_query(db)

        print(vacancies)

        return Vacancies(vacancies=vacancies['not_in_db'])
    else:
        raise HTTPException(
            status_code=409,
            detail="Template not found."
                )
