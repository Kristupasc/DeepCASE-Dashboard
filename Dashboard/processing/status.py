from enum import Enum


class Status(Enum):
    EMPTY = 0
    PREPROCESSING = 1
    CONTEXT_BUILDER = 2
    INTERPRETER = 3
    MANUAL_ANALYSIS = 4
    AUTO_ANALYSIS = 5
    FINISHED = 6
