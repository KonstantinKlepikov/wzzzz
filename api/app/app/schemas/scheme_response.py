from typing import Optional
from pydantic import BaseModel, NonNegativeInt, HttpUrl
from app.schemas import VacancyConstraintsScheme


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


class VacancyResponseScheme(BaseModel):
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


class VacancyResponseSchemeDb(VacancyId, VacancyResponseScheme):
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


class VacanciesResponseScheme(BaseModel):
    """Vacancies
    """

    vacancies: dict[NonNegativeInt, VacancyResponseScheme]

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


class TemplateNameScheme(BaseModel):
    """Template name
    """
    name: str

    class Config:

        schema_extra = {
                "example": {
                    'name': 'my_template'
                        }
                    }


class TemplateNamesScheme(BaseModel):
    """List of templates names
    """
    names: list[TemplateNameScheme] = []

    class Config:

        schema_extra = {
                "example": {
                    'names': {
                        'name': 'my_template'
                            }
                        }
                    }


class TemplateResponseScheme(TemplateNameScheme):
    """Template response
    """
    constraints: VacancyConstraintsScheme

    class Config:

        schema_extra = {
                "example": {
                    'name': 'my_template',
                    'constarints': VacancyConstraintsScheme.Config.schema_extra['example']
                        }
                    }
