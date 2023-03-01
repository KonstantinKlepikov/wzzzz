from typing import Any
from fastapi import APIRouter, status
from fastapi.requests import Request
from app.core import SessionMaker, HhruQueries
from app.schemas import VacancyRequestScheme, VacanciesResponseScheme


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary='Request for vacancies data',
    response_description="OK. Requested data."
        )
async def vacancies(request: Request) -> VacanciesResponseScheme:
    """Request for vacancies data
    """
    params = VacancyRequestScheme(**VacancyRequestScheme.Config.schema_extra['example']) # FIXME: fixme
    queries = HhruQueries(SessionMaker, "https://api.hh.ru/vacancies", params)
    result = await queries.vacancies_query()

    return result
