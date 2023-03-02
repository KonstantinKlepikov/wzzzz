from fastapi import APIRouter, status
from fastapi.requests import Request
from app.core import SessionMaker, HhruQueries
from app.schemas import VacancyRequestScheme, Vacancies
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
    params = VacancyRequestScheme(
        **VacancyRequestScheme.Config.schema_extra['example']
            )  # FIXME: fixme
    queries = HhruQueries(SessionMaker, "https://api.hh.ru/vacancies", params)
    result = await queries.vacancies_query()
    return Vacancies(vacancies=result)
