from typing import Optional
from datetime import datetime
from pydantic import BaseModel, NonNegativeInt, HttpUrl, conint
from app.schemas.scheme_templates import TemplateConstraints


class VacancyId(BaseModel):
    """Vacancy id
    """
    v_id: NonNegativeInt

    class Config:

        schema_extra = {
                "example": {
                    'v_id': 123456,
                        }
                    }


class VacancyRequest(TemplateConstraints):
    """Request querie to hh.ru vacancy API
    """
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
                    'date_from': '2022-06-01T10:20:30',
                    'page': 0,
                    'per_page': 100,
                        }
                    }
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d'),
                }


class VacancyResponse(BaseModel):
    """Response vacancy data
    """
    professional_roles: list[str] = []
    area: Optional[str] = None
    experience: Optional[str] = None
    description: Optional[str] = None
    key_skills: list[str] = []
    employer: Optional[str] = None
    alternate_url: Optional[HttpUrl] = None

    class Config:

        schema_extra = {
                "example": {
                    'professional_roles': ['Middle Backend Python программист', ],
                    'area': 'Москва',
                    'experience': 'От 1 года до 3 лет',
                    'description':
                        'Мы создаем системы искусственного интеллекта',
                    'key_skills': [
                        'Python', 'MongoDB', 'Swagger', 'FastAPI',
                        'Django Framework', 'REST', 'Git', 'SQL'
                        ],
                    'employer': 'Lexicom',
                    'alternate_url': 'https://hh.ru/vacancy/76294246',
                        }
                    }


class VacancyResponseInDb(VacancyId, VacancyResponse):
    """Vacancy in db
    """

    class Config:

        schema_extra = {
            "example": {
                'v_id': 123456,
                'professional_roles': ['Middle Backend Python программист', ],
                'area': 'Москва',
                'experience': 'От 1 года до 3 лет',
                'description':
                    'Мы создаем системы искусственного интеллекта',
                'key_skills': [
                    'Python', 'MongoDB', 'Swagger', 'FastAPI',
                    'Django Framework', 'REST', 'Git', 'SQL'
                    ],
                'employer': 'Lexicom',
                'alternate_url': 'https://hh.ru/vacancy/76294246',
                    }
                }


class Vacancies(BaseModel):
    """Vacancies
    """

    vacancies: dict[NonNegativeInt, VacancyResponse]

    class Config:

        schema_extra = {
                "example": {
                    'vacancies': {
                        76294246: {
                            'professional_roles': [
                                'Middle Backend Python программист',
                                    ],
                            'area': 'Москва',
                            'experience': 'От 1 года до 3 лет',
                            'description':
                            'Мы создаем системы искусственного интеллекта',
                            'key_skills': [
                                'Python', 'MongoDB', 'Swagger', 'FastAPI',
                                'Django Framework', 'REST', 'Git', 'SQL'
                                ],
                            'employer': 'Lexicom',
                            'alternate_url': 'https://hh.ru/vacancy/76294246',
                                },
                            }
                        }
                    }
