from typing import Optional
from pydantic import BaseModel, NonNegativeInt, HttpUrl, Field


class VacancyResponseScheme(BaseModel):
    """Response vacancy data
    """

    vac_id: NonNegativeInt
    professional_roles: list[str] = []
    area: Optional[str]
    expirience: Optional[str]
    description: Optional[str]
    key_skills: list[str] = []
    employer: Optional[str]
    alternate_url: Optional[HttpUrl] = None
    url: Optional[HttpUrl] = None

    class Config:

        schema_extra = {
                "example": {
                    'vac_id': 76294246,
                    'professional_roles': ['Middle Backend Python программист', ],
                    'area': 'Москва',
                    'expirience': 'От 1 года до 3 лет',
                    'description':
                        'Мы создаем системы искусственного интеллекта',
                    'key_skills': [
                        'Python', 'MongoDB', 'Swagger', 'FastAPI',
                        'Django Framework', 'REST', 'Git', 'SQL'
                        ],
                    'employer': 'Lexicom',
                    'alternate_url': 'https://hh.ru/vacancy/76294246',
                    'url': 'https://api.hh.ru/vacancies/8331228',
                        }
                    }

class VacanciesResponseScheme(BaseModel):
    """Vacancies
    """

    vacancies: list[VacancyResponseScheme]

    class Config:

        schema_extra = {
                "example":
                    {'vacancies': [{
                        'vac_id': 76294246,
                        'professional_roles': ['Middle Backend Python программист', ],
                        'area': 'Москва',
                        'expirience': 'От 1 года до 3 лет',
                        'description':
                            'Мы создаем системы искусственного интеллекта',
                        'key_skills': [
                            'Python', 'MongoDB', 'Swagger', 'FastAPI',
                            'Django Framework', 'REST', 'Git', 'SQL'
                            ],
                        'employer': 'Lexicom',
                        'alternate_url': 'https://hh.ru/vacancy/76294246',
                        'url': 'https://api.hh.ru/vacancies/8331228',
                        }]
                    }
                }
