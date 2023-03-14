from typing import Optional, Any
from fastapi import HTTPException
from pymongo.client_session import ClientSession
from app.crud import users


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
