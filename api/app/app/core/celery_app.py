from celery import Celery
from app.config import settings


celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL_DEV,
    backend='rpc://',
    include=['app.tasks',]
        )
