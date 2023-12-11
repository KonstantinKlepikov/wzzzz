from typing import Optional
from datetime import datetime
from pydantic import BaseModel, NonNegativeInt, HttpUrl, conint
from app.schemas.scheme_templates import TemplateConstraints
from app.schemas.constraint import (
    Area,
    Expirience,
    Employment,
    Professional,
    Schedule,
    SearchField,
        )


# FIXME: remove me
class VacancyId(BaseModel):
    """Vacancy id
    """
    v_id: NonNegativeInt

    class Config:

        json_schema_extra = {
                "example": {
                    'v_id': 123456,
                        }
                    }

# FIXME: remove me
class VacancyTs(BaseModel):
    """Timestamp
    """
    ts: datetime = datetime.utcnow()

    class Config:

        json_schema_extra = {
                "example": {
                    'ts': '2022-06-01T10:20:30',
                        }
                    }

# FIXME: remove me
class VacancyRequest(TemplateConstraints):
    """Request querie to hh.ru vacancy API
    """
    page: conint(ge=0, le=100) = 0
    per_page: conint(gt=0, le=100) = 100

    class Config:

        json_schema_extra = {
                "example": {
                    'area': Area.get_values(),
                    'text': 'game* OR гейм*',
                    'search_field': SearchField.get_names(),
                    'expirience': Expirience.get_names(),
                    'employment': [Employment.FULL, Employment.PART, ],
                    'schedule': [Schedule.REMOTE, ],
                    'professional_role': Professional.get_values(),
                    'date_from': '2022-06-01T10:20:30',
                    'page': 0,
                    'per_page': 100,
                        }
                    }
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d'),
                }

# FIXME: remove me
class VacancyResponse(BaseModel):
    """Response vacancy data
    """
    professional_roles: list[str] = []
    area: Optional[str] = None
    experience: Optional[str] = None
    description: Optional[str] = None
    key_skills: list[str] = []
    employer: Optional[str] = None
    alternate_url: Optional[str] = None  # FIXME: switch to httpurl, but we have problem with model dump

    class Config:

        json_schema_extra = {
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


# FIXME: remove me
class Vacancy(VacancyId, VacancyResponse):
    """Vacancy with id
    """

    class Config:

        json_schema_extra = {
            "example": {
                'v_id': 123456, # FIXME: string
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

# FIXME: remove me
class VacancyResponseInDb(Vacancy, VacancyTs):
    """Vacancy in db
    """

    class Config:

        json_schema_extra = {
            "example": {
                'v_id': 123456, # FIXME: string
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
                'ts': '2022-06-01T10:20:30',
                    }
                }


# FIXME: remove me
class Vacancies(BaseModel):
    """Vacancies as dict
    """

    vacancies: dict[NonNegativeInt, VacancyResponse]

    class Config:

        json_schema_extra = {
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


# FIXME: remove me
class AllVacancies(BaseModel):
    """Vacancies as list
    """

    vacancies: list[Vacancy]

    class Config:

        json_schema_extra = {
                "example": {
                    'vacancies': [
                        {
                            'v_id': 123456,
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
                            ]
                        }
                    }
