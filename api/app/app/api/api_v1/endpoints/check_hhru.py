from typing import Any
from fastapi import APIRouter, status
from fastapi.requests import Request
from app.core.http_session import SessionMaker


router = APIRouter()


@router.post(
    "/check_simple_post",
    status_code=status.HTTP_200_OK,
    summary='Check simple post',
    response_description="OK. Request is responsed."
        )
async def check_simple_post(request: Request) -> Any:
    """Test request to hh.ru API

    Returns:
        _Any: json response
    """
    url = "https://api.hh.ru/professional_roles"
    return await SessionMaker.simple_query(url)
