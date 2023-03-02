from enum import Enum


class Employment(str, Enum):
    FULL = 'full'
    PART = 'part'
    PROJ = 'project'
    VOLUN = 'volunteer'
    PROBATION = 'probation'


class Schedule(str, Enum):
    FULL = 'fullDay'
    SHIFT = 'shift'
    FLEX = 'flexible'
    REMOTE = 'remote'
    FLY = 'lyInFlyOut'
