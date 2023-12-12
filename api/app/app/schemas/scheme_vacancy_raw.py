from datetime import datetime
from pydantic import BaseModel, NonNegativeInt, Field, ConfigDict


class VacancyId(BaseModel):
    """Vacancy id

    When id is serialized - the name of attribute is change to
    v_id - because id is reserved for mongoDb primary key
    """
    id: NonNegativeInt = Field(..., serialization_alias='v_id')

    class Config:

        json_schema_extra = {
            "example": {
                'id': 87542153,
                    }
                }


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


class VacancyRawData(VacancyId, VacancyTs):
    """Vacancy raw

    Extra fields is used to allow raw vacancy data.
    Yhis requred because we dont know actual api respons.
    """

    class Config:

        extra='allow'
        json_schema_extra = {
            "example": {
                'id': 87542153,
                'ts': '2022-06-01T10:20:30',
                    }
                }


class VacancyOut(BaseModel):
    """Csv vacancy data
    """
    professional_roles: list[str] = []
    area: str | None = None
    experience: str | None = None
    description: str | None = None
    key_skills: list[str] = []
    employer: str | None = None
    alternate_url: str | None = None  # FIXME: switch to httpurl, but we have problem with model dump

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
