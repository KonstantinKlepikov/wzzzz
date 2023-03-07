from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.requests import Request
from pymongo.client_session import ClientSession
from app.core import SessionMaker, HhruQueries
from app.db.init_db import get_session
from app.schemas import (
    VacancyRequestScheme,
    VacanciesResponseScheme,
    TemplateNamesScheme,
    TemplateResponseScheme,
        )
from app.config import settings
from app.crud import template


router = APIRouter()


@router.post(
    "/template",
    status_code=status.HTTP_201_CREATED,
    summary='Create template with given name',
    response_description="Created.",
    responses=settings.ERRORS
        )
async def create_template(name: str, db: ClientSession = Depends(get_session)) -> None:
    """Create template with given name
    """


@router.get(
    "/template",
    status_code=status.HTTP_200_OK,
    summary='Get template by name name',
    response_description="Ok.",
    response_model=TemplateResponseScheme,
    responses=settings.ERRORS
        )
async def get_template(
    name: str,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Get template constraints by name
    """
    result = await template.get(db, {'name': name})
    if result:
        return TemplateResponseScheme(**result)
    else:
        raise HTTPException(
            status_code=400,
            detail="Template not find."
                )


@router.get(
    "/templates",
    status_code=status.HTTP_200_OK,
    summary='Get list of templates names',
    response_description="Ok.",
    response_model=TemplateNamesScheme,
    responses=settings.ERRORS
        )
async def get_templates(db: ClientSession = Depends(get_session)) -> None:
    """Get list of templates names
    """
    result = await template.get_names(db)
    return TemplateNamesScheme(names=result)



@router.delete(
    "/template",
    status_code=status.HTTP_200_OK,
    summary='Get template by name name',
    response_description="Ok.",
    responses=settings.ERRORS
        )
async def delete_template(name: str, db: ClientSession = Depends(get_session)) -> None:
    """Delete template by name
    """


@router.patch(
    "/template",
    status_code=status.HTTP_200_OK,
    summary='Change templates constraints',
    response_description="Ok.",
    responses=settings.ERRORS
        )
async def change_template(name: str, db: ClientSession = Depends(get_session)) -> None:
    """Change templates constraints
    """


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary='Request for vacancies data',
    response_description="OK. Requested data.",
    response_model=VacanciesResponseScheme,
    responses=settings.ERRORS
        )
async def vacancies(request: Request) -> VacanciesResponseScheme:
    """Request for vacancies data
    """
    params = VacancyRequestScheme(
        **VacancyRequestScheme.Config.schema_extra['example']
            )  # FIXME: fixme
    queries = HhruQueries(SessionMaker, "https://api.hh.ru/vacancies", params)
    result = await queries.vacancies_query()
    return VacanciesResponseScheme(vacancies=result)
