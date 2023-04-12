from typing import Any
from celery import chain
from app.core.celery_app import celery_app
from app.core import HhruQueries, SessionMaker
from app.schemas.scheme_vacanciy import VacancyRequest


@celery_app.task
def get_pages(api_url: str, params: dict[str, any]):
    """Here we get firts page by query
    """
    params = VacancyRequest(**params)
    queries = HhruQueries(SessionMaker, api_url, params)


@celery_app.task
def check_in_db(some):
    """Here we check - is a vacancy in db
    """


@celery_app.task
def get_full_vacancy(some):
    """Here we get full vacancy
    """


@celery_app.task
def save_to_db(some):
    """Save data to db
    """


def get_vacancy(api_url: str, params: dict[str, Any]):
    """Get vacancies task

    get_pages -> get_full_vacancies -> fetch_vacancies_data -> store_to_db

    Args:

    """
    print('here')
    c = chain(get_pages.s(api_url, params) | check_in_db.s() | get_full_vacancy.s() | save_to_db.s())
    print(c)
    return c().get()
