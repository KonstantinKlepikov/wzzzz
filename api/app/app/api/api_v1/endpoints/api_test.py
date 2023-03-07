from fastapi import APIRouter, status, Depends
from pymongo.client_session import ClientSession
from app.db.init_db import get_session
from app.config import settings


router = APIRouter()


@router.get(
    "/get_db_name",
    status_code=status.HTTP_200_OK,
    summary='Test data',
    response_description="OK",
        )
async def get_db_name(session: ClientSession = Depends(get_session)) -> None:
    """Test request
    """
    return {'name': session.client[settings.db_name].name}
