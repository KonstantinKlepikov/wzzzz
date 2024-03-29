from typing import Optional
from typing_extensions import Annotated
from enum import Enum
from pydantic import BaseModel, constr, validator
from pydantic.functional_validators import AfterValidator
from datetime import timedelta, datetime
from bson.objectid import ObjectId
from app.schemas.constraint import (
    Employment,
    Schedule,
    Expirience,
    Area,
    Professional,
    SearchField,
        )


def must_be_a_list(v: list) -> list[str | int]:
    if v and isinstance(v[0], Enum):
        return [a.value for a in v]
    return v


class TemplateConstraints(BaseModel):
    """Vacancy constraints scheme
    """
    area: list[Area] = Area.get_values()
    expirience: list[Expirience] = Expirience.get_values()
    employment: list[Employment] = [Employment.FULL, Employment.PART, ]
    schedule: list[Schedule] = [Schedule.REMOTE, ]
    professional_role: list[Professional] = Professional.get_values()
    date_from: datetime = datetime.utcnow() - timedelta(weeks=8)
    text: Optional[str] = None
    search_field: list[SearchField] = SearchField.get_values()

    _area = validator('area', allow_reuse=True)(must_be_a_list)
    _expirience = validator('expirience', allow_reuse=True)(must_be_a_list)
    _employment = validator('employment', allow_reuse=True)(must_be_a_list)
    _professional_role = validator(
        'professional_role', allow_reuse=True)(must_be_a_list)
    _schedule = validator('schedule', allow_reuse=True)(must_be_a_list)
    _search_field = validator('search_field', allow_reuse=True)(must_be_a_list)

    class Config:

        json_schema_extra = {
            "example": {
                'area': Area.get_names(),
                'expirience': Expirience.get_names(),
                'employment': [Employment.FULL, Employment.PART, ],
                'schedule': [Schedule.REMOTE, ],
                'professional_role': Professional.get_names(),
                'date_from': '2022-06-01T10:20:30',
                'text': 'game* OR гейм*',
                'search_field': SearchField.get_names(),
                    }
                }


class TemplateName(BaseModel):
    """Template name
    """
    name: constr(max_length=20, pattern="^[A-Za-z0-9_-]*$")  # noqa: F722

    class Config:

        json_schema_extra = {
                "example": {
                    'name': 'my_template'
                        }
                    }


class TemplatesNames(BaseModel):
    """List of templates names
    """
    names: list[TemplateName] = []

    class Config:

        json_schema_extra = {
                "example": {
                    'names': [
                        {'name': 'my_template'},
                        {'name': 'another'},
                            ]
                        }
                    }


class Template(TemplateName, TemplateConstraints):
    """Template response
    """
    class Config:

        json_schema_extra = {
                "example": {
                    'name': 'my_template',
                    'area': Area.get_names(),
                    'expirience': Expirience.get_names(),
                    'employment': [Employment.FULL, Employment.PART, ],
                    'schedule': [Schedule.REMOTE, ],
                    'professional_role': Professional.get_names(),
                    'date_from': '2022-06-01T10:20:30',
                    'text': 'game* OR гейм*',
                    'search_field': SearchField.get_names(),
                        }
                    }


def check_object_id(value: str) -> str:
    if not ObjectId.is_valid(value):
        raise ValueError('ObjectId required')
    return value


PydanticObjectId = Annotated[str, AfterValidator(check_object_id)]


class TemplateInDb(Template):
    """Template in db
    """
    user: PydanticObjectId  # TODO: test validation str/obj

    class Config:

        json_schema_extra = {
                "example": {
                    'name': 'my_template',
                    'area': Area.get_values(),
                    'expirience': Expirience.get_names(),
                    'employment': [Employment.FULL.value, Employment.PART.value, ],
                    'schedule': [Schedule.REMOTE, ],
                    'professional_role': Professional.get_values(),
                    'date_from': '2022-06-01T10:20:30',
                    'text': 'game* OR гейм*',
                    'search_field': SearchField.get_names(),
                    'user': '123456781234567812345678'
                        }
                    }
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
                }
