from fastapi import APIRouter
from app.api.api_v1.endpoints import vacancies, users


api_router = APIRouter()


api_router.include_router(
    vacancies.router, prefix="/vacancies", tags=['vacancies', ]
        )
api_router.include_router(
    users.router, prefix="/users", tags=['user', ]
        )
