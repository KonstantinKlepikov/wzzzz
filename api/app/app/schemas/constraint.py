from enum import Enum


class BaseEnum(str, Enum):
    """Base class for enumeration
    """
    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def get_values(cls) -> list[str]:
        return [e.value for e in cls]


class Employment(BaseEnum):
    FULL = 'full'
    PART = 'part'
    PROJ = 'project'
    VOLUN = 'volunteer'
    PROBATION = 'probation'


class Schedule(BaseEnum):
    FULL = 'fullDay'
    SHIFT = 'shift'
    FLEX = 'flexible'
    REMOTE = 'remote'
    FLY = 'lyInFlyOut'


class Collections(BaseEnum):
    VACANCIES = 'vacancies'
