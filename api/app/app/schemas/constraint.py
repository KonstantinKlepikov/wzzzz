from enum import Enum


class BaseEnum(Enum):
    """Base class for enumeration
    """
    @classmethod
    def has_value(cls, value: str | int) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def get_values(cls) -> list[str| int]:
        return [e.value for e in cls]

    @classmethod
    def get_names(cls) -> list[Enum]:
        return [e for e in cls]


class BaseStrEnum(str, BaseEnum):
    """Base class for enumeration
    """

class Area(BaseEnum):
    """https://github.com/hhru/api/blob/master/docs/areas.md
    """
    RUSSIA = 113
    KAZAKHSTAN = 40
    GEORGIA = 28
    OTHER = 1001


class Expirience(BaseStrEnum):
    NO = 'noExperience'
    B1TO3 = 'between1And3'
    B3TO6 = 'between3And6'
    MORE6 = 'moreThan6'


class Employment(BaseStrEnum):
    FULL = 'full'
    PART = 'part'
    PROJ = 'project'
    VOLUN = 'volunteer'
    PROBATION = 'probation'


class Schedule(BaseStrEnum):
    FULL = 'fullDay'
    SHIFT = 'shift'
    FLEX = 'flexible'
    REMOTE = 'remote'
    FLY = 'lyInFlyOut'


class Professional(BaseEnum):
    """https://api.hh.ru/openapi/redoc#tag/Obshie-spravochniki/operation/get-professional-roles-dictionary
    """
    PROGRAMMER = 96
    DEVOPS = 160
    DATASCIENTIST = 165
    TESTER = 124


class SearchField(BaseStrEnum):
    DESCRIPTION = 'description'
    NAME = 'name'


class Collections(BaseStrEnum):
    VACANCIES = 'vacancies'
    TEMPLATES = 'templates'
    USERS = 'users'
