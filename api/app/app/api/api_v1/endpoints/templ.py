from typing import Optional, Any
from fastapi import APIRouter, status, Depends, HTTPException
from pymongo.client_session import ClientSession
from bson.objectid import ObjectId
from app.db import get_session
from app.schemas import (
    TemplatesNames,
    TemplateInDb,
    Template
        )
from app.config import settings
from app.crud import templates, users


router = APIRouter()


async def check_user(
    db: ClientSession,
    login: int
        ) -> Optional[dict[str, Any]]:
    """Check is user in db or raise exception

    Args:
        db: ClientSession
        login (int): user login

    Returns:
        Optional[dict[str, Any]]: db query result
    """
    user = await users.get(db, {'login': login})
    if user:
        return user
    raise HTTPException(
        status_code=409,
        detail=f"User {login} not exist."
            )


@router.post(
    "/create_empty",
    status_code=status.HTTP_201_CREATED,
    summary='Create empty template with given name',
    response_description="Created.",
    responses=settings.ERRORS
        )
async def create_template(
    login: int,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Create empty template with given name
    """
    user = await check_user(db, login)
    await templates.create(db, obj_in=TemplateInDb(
        user=ObjectId(user['_id']),
        name=template_name
            ))


@router.get(
    "/get",
    status_code=status.HTTP_200_OK,
    summary='Get template by template name',
    response_description="Ok.",
    response_model=Template,
    responses=settings.ERRORS
        )
async def get_template(
    login: int,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> Template:
    """Get template by template_name

    Args:
        login (str): user login
        template_name (str):name of template
    """
    user = await check_user(db, login)

    result = await templates.get(db, {'name': template_name, 'user': user['_id']})

    if result:
        return Template(**result)

    else:
        raise HTTPException(
            status_code=409,
            detail="Template not found."
                )


@router.get(
    "/get_names",
    status_code=status.HTTP_200_OK,
    summary='Get list of templates names',
    response_description="Ok.",
    response_model=TemplatesNames,
    responses=settings.ERRORS
        )
async def get_templates(
    login: int,
    db: ClientSession = Depends(get_session)
        ) -> TemplatesNames:
    """Get list of templates names

    Args:
        login (str): user login
    """
    user = await check_user(db, login)
    result = await templates.get_names(db, {'user': user['_id']})
    return TemplatesNames(names=result)


@router.delete(
    "/delete",
    status_code=status.HTTP_200_OK,
    summary='Delete template by template_name',
    response_description="Ok.",
    responses=settings.ERRORS
        )
async def delete_template(
    login: int,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Delete template by template_name

    Args:
        login (str): user login
        template_name (str): name of template
    """
    user = await check_user(db, login)
    result = await templates.delete(db, {'name': template_name, 'user': user['_id']})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=409,
            detail="Template not found."
                )


@router.patch(
    "/replace",
    status_code=status.HTTP_200_OK,
    summary='Replace template constraints',
    response_description="Ok.",
    responses=settings.ERRORS
        )
async def change_template(
    login: int,
    template: Template,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Replace template constraints

    Args:
        login (str): user login
        template_name (str): name of template
        template (Template): new template constraints
    """
    user = await check_user(db, login)
    result = await templates.replace(
        db,
        {'name': template.name, 'user': user['_id']},
        template
            )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=409,
            detail="Template not found."
                )
