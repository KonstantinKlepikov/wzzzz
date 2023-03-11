from typing import Optional
from pydantic import BaseModel
from datetime import timedelta, datetime
from bson.objectid import ObjectId
from bson.errors import InvalidId
from app.schemas.constraint import Employment, Schedule, Expirience


class TemplateConstraints(BaseModel):
    """Vacancy constraints scheme
    """
    area: list[int] = []
    expirience: Optional[Expirience] = None
    employment: list[Employment] = []
    schedule: list[Schedule] = []
    professional_role: list[int] = []
    date_from: datetime = datetime.utcnow() - timedelta(weeks=12)
    text: Optional[str] = None

    class Config:

        schema_extra = {
            "example": {
                'area': [113, 40, 1001],
                'expirience': 'noExperience',
                'employment': ['full', 'part', ],
                'schedule': ['remote', ],
                'professional_role': [25, 96],
                'date_from': '2022-06-01T10:20:30',
                'text': 'game* OR гейм*',
                    }
                }


class TemplateName(BaseModel):
    """Template name
    """
    name: str

    class Config:

        schema_extra = {
                "example": {
                    'name': 'my_template'
                        }
                    }


class TemplatesNames(BaseModel):
    """List of templates names
    """
    names: list[TemplateName] = []

    class Config:

        schema_extra = {
                "example": {
                    'names': {
                        'name': 'my_template'
                            }
                        }
                    }


class Template(TemplateName, TemplateConstraints):
    """Template response
    """
    class Config:

        schema_extra = {
                "example": {
                    'name': 'my_template',
                    'area': [113, 40, 1001],
                    'expirience': 'noExperience',
                    'employment': ['full', 'part', ],
                    'schedule': ['remote', ],
                    'professional_role': [25, 96],
                    'date_from': '2022-06-01T10:20:30',
                    'text': 'game* OR гейм*',
                        }
                    }


class PydanticObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            try:
                ObjectId(v)
            except InvalidId:
                raise TypeError('ObjectId required')
        return str(v)


class TemplateInDb(Template):
    """Template in db
    """
    user: PydanticObjectId  # TODO: test validation str/obj

    class Config:

        schema_extra = {
                "example": {
                    'name': 'my_template',
                    'area': [113, 40, 1001],
                    'expirience': 'noExperience',
                    'employment': ['full', 'part', ],
                    'schedule': ['remote', ],
                    'professional_role': [25, 96],
                    'date_from': '2022-06-01T10:20:30',
                    'text': 'game* OR гейм*',
                    'user': '123456781234567812345678'
                        }
                    }
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
                }
