from fastapi import APIRouter
from app.api.api_v1.endpoints import check_hhru


api_router = APIRouter()


api_router.include_router(
    check_hhru.router, prefix="/check_hhru", tags=['check_hhru', ]
        )
