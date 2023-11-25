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
