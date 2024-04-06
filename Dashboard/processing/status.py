from enum import Enum


class Status(Enum):
    EMPTY = 0
    WAITING_INPUT_DATA = 1
    IN_PROGRESS = 2
    FINISHED = 3
