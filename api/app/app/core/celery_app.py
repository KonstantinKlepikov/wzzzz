from celery import Celery
from app.config import settings

celery_app = Celery("worker", broker=settings.CELERY_BROKER_URL_DEV)

celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
