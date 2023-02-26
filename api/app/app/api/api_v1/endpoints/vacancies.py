from typing import Any
from fastapi import APIRouter, status
from fastapi.requests import Request
from app.core.http_session import SessionMaker


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary='Request for vacancyies data',
    response_description="OK. Requested data."
        )
async def vacancies(request: Request) -> Any:
    """Test request to hh.ru API

    Returns:
        _Any: json response
    """
    url = "https://api.hh.ru/vacancyes"
    return await SessionMaker.vacancy_query(url, params={})
