from datetime import datetime
from pydantic import BaseModel, NonNegativeInt, Field, conint
from datetime import datetime
from app.schemas.scheme_templates import TemplateConstraints
from app.schemas.constraint import (
    Area,
    Expirience,
    Employment,
    Professional,
    Schedule,
    SearchField,
        )


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


class VacancyData(VacancyId, VacancyTs):
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


class VacancyOut(BaseModel):
    """Csv vacancy data
    """
    professional_roles: list[str] = []
    area: str | None = None
    experience: str | None = None
    description: str | None = None
    key_skills: list[str] = []
    employer: str | None = None
    alternate_url: str | None = None

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
