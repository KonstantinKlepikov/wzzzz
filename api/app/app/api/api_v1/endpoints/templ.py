from fastapi import APIRouter, status, Depends, HTTPException
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from app.db import get_session
from app.schemas import (
    TemplatesNames,
    TemplateInDb,
    Template
        )
from app.config import settings
from app.crud import templates
from app.core import check_user


router = APIRouter()


@router.post(
    "/create_empty",
    status_code=status.HTTP_201_CREATED,
    summary='Create empty template with given name',
    response_description="Created.",
    responses=settings.ERRORS
        )
async def create_template(
    user_id: int,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Create empty template with given name
    """
    user = await check_user(db, user_id)
    try:
        await templates.create(db, obj_in=TemplateInDb(
            user=ObjectId(user['_id']),
            name=template_name
                ))
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail=f"Template with name {template_name} is exist."
                )


@router.get(
    "/get",
    status_code=status.HTTP_200_OK,
    summary='Get template by template name',
    response_description="Ok.",
    response_model=Template,
    responses=settings.ERRORS
        )
async def get_template(
    user_id: int,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> Template:
    """Get template by template_name

    Args:
        user_id (str): user_id
        template_name (str):name of template
    """
    user = await check_user(db, user_id)
    result = await templates.get(db, {'name': template_name, 'user': str(user['_id'])})

    if result:
        return Template(**result)

    else:
        raise HTTPException(
            status_code=404,
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
    user_id: int,
    db: ClientSession = Depends(get_session)
        ) -> TemplatesNames:
    """Get list of templates names

    Args:
        user_id (str): user_id
    """
    user = await check_user(db, user_id)
    result = await templates.get_names(db, {'user': str(user['_id'])})
    return TemplatesNames(names=result)


@router.delete(
    "/delete",
    status_code=status.HTTP_200_OK,
    summary='Delete template by template_name',
    response_description="Ok.",
    responses=settings.ERRORS
        )
async def delete_template(
    user_id: int,
    template_name: str,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Delete template by template_name

    Args:
        user_id (str): user_id
        template_name (str): name of template
    """
    user = await check_user(db, user_id)
    result = await templates.delete(
        db, {'name': template_name, 'user': str(user['_id'])}
            )
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
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
    user_id: int,
    template: Template,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Replace template constraints

    Args:
        user_id (str): user_id
        template_name (str): name of template
        template (Template): new template constraints
    """
    user = await check_user(db, user_id)
    t = TemplateInDb(user=str(user['_id']), **template.dict())
    result = await templates.replace(
        db,
        {'name': template.name, 'user': str(user['_id'])},
        t
            )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Template not found."
                )
