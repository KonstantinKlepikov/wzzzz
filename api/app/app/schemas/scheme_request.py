from typing import Optional
from pydantic import BaseModel, conint
from datetime import date
from app.schemas.constraint import Employment, Schedule, Expirience


class VacancyConstraintsScheme(BaseModel):
    """Vacancy constraints scheme
    """
    area: list[int] = []
    expirience: Optional[Expirience] = None
    employment: list[Employment] = []
    schedule: list[Schedule] = []
    professional_role: list[int] = []
    date_from: date
    text: Optional[str] = None

    class Config:

        schema_extra = {
            "example": {
                'area': [113, 40, 1001],
                'expirience': 'noExperience',
                'employment': ['full', 'part', ],
                'schedule': ['remote', ],
                'professional_role': [25, 96],
                'date_from': '2022-06-01',
                'text': 'game* OR гейм*',
                    }
                }


class VacancyRequestScheme(VacancyConstraintsScheme):
    """Request to hh.ru vacancy API
    """
    # text: str
    search_field: list[str]
    page: conint(ge=0, le=100) = 0
    per_page: conint(gt=0, le=100) = 100

    class Config:

        schema_extra = {
                "example": {
                    'area': [113, 40, 1001],
                    'text': 'game* OR гейм*',
                    'search_field': ['description', ],
                    'expirience': 'noExperience',
                    'employment': ['full', 'part', ],
                    'schedule': ['remote', ],
                    'professional_role': [25, 96],
                    'date_from': '2022-06-01',
                    'page': 0,
                    'per_page': 100,
                        }
                    }
