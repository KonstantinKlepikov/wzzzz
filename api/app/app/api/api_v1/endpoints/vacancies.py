from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.requests import Request
from pymongo.client_session import ClientSession
from app.core import SessionMaker, HhruQueries
from app.db import get_session
from app.schemas import (
    VacancyRequest,
    Vacancies,
    TemplatesNames,
    Template,
        )
from app.config import settings
from app.crud import templates, users


router = APIRouter()


@router.post(
    "/template",
    status_code=status.HTTP_201_CREATED,
    summary='Create template with given template_name',
    response_description="Created.",
    responses=settings.ERRORS
        )
async def create_template(
    login: str,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Create template with given template_name
    """


@router.get(
    "/template",
    status_code=status.HTTP_200_OK,
    summary='Get template by template_name',
    response_description="Ok.",
    response_model=Template,
    responses=settings.ERRORS
        )
async def get_template(
    login: str,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Get template constraints by template_name

    Args:
        login (str): user login
        template_name (str):name of template
    """
    user = await users.get(db, {'login': login})

    if user:

        result = await templates.get(db, {'name': template_name, 'user': user['_id']})

        if result:
            return Template(**result)

        else:
            raise HTTPException(
                status_code=400,
                detail="Template not finded."
                    )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"User {login} not exist."
                )


@router.get(
    "/templates",
    status_code=status.HTTP_200_OK,
    summary='Get list of templates names',
    response_description="Ok.",
    response_model=TemplatesNames,
    responses=settings.ERRORS
        )
async def get_templates(
    login: str,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Get list of templates names
    """
    # TODO: rewrite me
    result = await templates.get_names(db)
    return TemplatesNames(names=result)


@router.delete(
    "/template",
    status_code=status.HTTP_200_OK,
    summary='Get template by template_name',
    response_description="Ok.",
    responses=settings.ERRORS
        )
async def delete_template(
    login: str,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Delete template by template_name
    """


@router.patch(
    "/template",
    status_code=status.HTTP_200_OK,
    summary='Change templates constraints',
    response_description="Ok.",
    responses=settings.ERRORS
        )
async def change_template(
    login: str,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Change templates constraints
    """


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
