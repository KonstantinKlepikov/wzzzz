from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.requests import Request
from pymongo.client_session import ClientSession
from app.core import SessionMaker, HhruQueries
from app.db import get_session
from app.schemas import (
    VacancyRequest,
    Vacancies,
        )
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
async def vacancies(request: Request) -> Vacancies:
    """Request for vacancies data
    """
    params = VacancyRequest(
        **VacancyRequest.Config.schema_extra['example']
            )  # FIXME: fixme
    queries = HhruQueries(SessionMaker, "https://api.hh.ru/vacancies", params)
    result = await queries.vacancies_query()
    return Vacancies(vacancies=result)
