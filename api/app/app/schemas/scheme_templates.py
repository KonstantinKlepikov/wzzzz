from typing import Optional
from pydantic import BaseModel, Field
from datetime import date
from bson.objectid import ObjectId
from app.schemas.constraint import Employment, Schedule, Expirience


class TemplateConstraints(BaseModel):
    """Vacancy constraints scheme
    """
    area: list[int] = []
    expirience: Optional[Expirience] = None
    employment: list[Employment] = []
    schedule: list[Schedule] = []
    professional_role: list[int] = []
    date_from: date
    text: Optional[str] = None

    class Config:

        schema_extra = {
            "example": {
                'area': [113, 40, 1001],
                'expirience': 'noExperience',
                'employment': ['full', 'part', ],
                'schedule': ['remote', ],
                'professional_role': [25, 96],
                'date_from': '2022-06-01',
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


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Template(TemplateName, TemplateConstraints):
    """Template response
    """
    user: PydanticObjectId = Field(default_factory=PydanticObjectId)

    class Config:

        schema_extra = {
                "example": {
                    'name': 'my_template',
                    'area': [113, 40, 1001],
                    'expirience': 'noExperience',
                    'employment': ['full', 'part', ],
                    'schedule': ['remote', ],
                    'professional_role': [25, 96],
                    'date_from': '2022-06-01',
                    'text': 'game* OR гейм*',
                    'user': '123456781234567812345678'
                        }
                    }
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
                }
