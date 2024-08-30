from enum import Enum

class Sub(Enum):
    MONTH = 30
    THREE_MONTHS = 90
    YEAR = 364 
    NONE = 0

    @classmethod
    def get_choices(cls):
        return [(i.name, i.value) for i in cls]
