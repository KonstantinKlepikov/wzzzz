from typing import Any
from celery import chain
from app.core.celery_app import celery_app
from app.core import HhruQueries, SessionMaker
from app.schemas.scheme_vacanciy import VacancyRequest


@celery_app.task
def get_pages(api_url: str, params: dict[str, Any]):
    """Here we get firts page by query
    """
    params = VacancyRequest(**params)
    queries = HhruQueries(SessionMaker, api_url, params)

    return 'abcde'


@celery_app.task
def check_in_db(some):
    """Here we check - is a vacancy in db
    """
    return ''.join([let for let in some if let in 'abcd'])


@celery_app.task
def get_full_vacancy(some):
    """Here we get full vacancy
    """
    return some + 'z'


@celery_app.task
def save_to_db(some):
    """Save data to db
    """
    return some.capitalize()


def get_vacancy(api_url: str, params: dict[str, Any]):
    """Get vacancies task

    get_pages -> check in db -> get full -> save

    Args:

    """
    c = chain(
        get_pages.s(api_url, params)
        | check_in_db.s()
        | get_full_vacancy.s()
        | save_to_db.s()
            )
    return c().get()
