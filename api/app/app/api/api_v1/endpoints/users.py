from typing import Optional
from fastapi import APIRouter, status, Depends, HTTPException
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from app.db import get_session
from app.schemas.scheme_user import User
from app.config import settings
from app.crud.crud_user import users


router = APIRouter()


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary='Create user with given user id',
    response_description="Created.",
    responses=settings.ERRORS
        )
async def create_user(
    user_id: int,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Create user with given user id
    """
    try:
        await users.create(db, {"user_id": user_id})

    except DuplicateKeyError:

        raise HTTPException(
            status_code=409,
            detail=f"User {user_id} exist."
                )


@router.get(
    "/get_by_id",
    status_code=status.HTTP_200_OK,
    summary='Get user by given id given user id',
    response_description="User data.",
    responses=settings.ERRORS,
    response_model=User,
        )
async def get_user_by_id(
    user_id: int,
    db: ClientSession = Depends(get_session)
        ) -> Optional[User]:
    """Get user by given id given user id
    """
    user = await users.get(db, {'user_id': user_id})

    if user:
        return User(**user)

    raise HTTPException(
        status_code=404,
        detail=f"User {user_id} not exist."
            )
