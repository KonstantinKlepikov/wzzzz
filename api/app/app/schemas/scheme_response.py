from pydantic import BaseModel, NonNegativeInt, HttpUrl


class VacancyResponseScheme(BaseModel):

    hhru_id: NonNegativeInt
    name: str
    area: str
    expirience: str
    description: str
    key_skills: list[str]
    employer: str
    alternative_url: HttpUrl

    class Config:

        schema_extra = {
                "example": {
                    'hhru_id': 76294246,
                    'name': 'Middle Backend Python программист',
                    'area': 'Москва',
                    'expirience': 'От 1 года до 3 лет',
                    'description':
                        'Мы создаем системы искусственного интеллекта',
                    'key_skills': [
                        'Python', 'MongoDB', 'Swagger', 'FastAPI',
                        'Django Framework', 'REST', 'Git', 'SQL'
                        ],
                    'employer': 'Lexicom',
                    'alternative_url': 'https://hh.ru/vacancy/76294246',
                        }
                    }
