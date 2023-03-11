from fastapi import APIRouter
from app.api.api_v1.endpoints import vacancies, users, templ


api_router = APIRouter()

api_router.include_router(
    users.router, prefix="/users", tags=['users', ]
        )
api_router.include_router(
    templ.router, prefix="/templates", tags=['templates', ]
        )
api_router.include_router(
    vacancies.router, prefix="/vacancies", tags=['vacancies', ]
        )
