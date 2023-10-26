from typing import Any
from datetime import datetime
from pydantic import BaseModel, NonNegativeInt, HttpUrl, conint


class VacancyId(BaseModel):
    """Vacancy id
    """
    id: NonNegativeInt

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
    """
    raw: dict[str, Any]

    class Config:

        json_schema_extra = {
            "example": {
                'id': 87542153,
                'ts': '2022-06-01T10:20:30',
                'raw': {},
                    }
                }
