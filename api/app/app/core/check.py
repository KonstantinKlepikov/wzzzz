from typing import Optional, Any
from fastapi import HTTPException
from pymongo.client_session import ClientSession
from app.crud.crud_user import users


async def check_user(
    db: ClientSession,
    user_id: int
        ) -> Optional[dict[str, Any]]:
    """Check is user in db or raise exception

    Args:
        db: ClientSession
        user_id (int): user_id

    Returns:
        Optional[dict[str, Any]]: db query result
    """
    user = await users.get(db, {'user_id': user_id})
    if user:
        return user
    raise HTTPException(
        status_code=409,
        detail=f"User {user_id} not exist."
            )
