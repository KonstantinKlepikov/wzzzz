from typing import Optional
from pydantic import BaseModel, NonNegativeInt, HttpUrl


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


class Vacancy(BaseModel):
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


class VacancyDb(VacancyId, Vacancy):
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

    vacancies: dict[NonNegativeInt, Vacancy]

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
