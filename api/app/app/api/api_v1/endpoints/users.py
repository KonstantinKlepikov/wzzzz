from fastapi import APIRouter, status, Depends, HTTPException
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from app.db import get_session
from app.schemas import UserInDb
from app.config import settings
from app.crud import users


router = APIRouter()


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary='Create user with given login',
    response_description="Created.",
    responses=settings.ERRORS
        )
async def create_user(
    login: int,
    db: ClientSession = Depends(get_session)
        ) -> None:
    """Create user with given login
    """
    user = UserInDb(login=login)

    try:
        await users.create(db, user)

    except DuplicateKeyError:

        raise HTTPException(
            status_code=409,
            detail=f"User {login} exist."
                )
