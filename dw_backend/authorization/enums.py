from enum import Enum

class Role(Enum):
    CEO = 'CEO'
    MANAGER = 'MANAGER'
    BETA = 'BETA'
    USER = 'USER'
    MEDIA = 'MEDIA'
    VISITOR = 'VISITOR'
    DEACTIVATED = 'AZIK'

    @classmethod
    def get_choices(cls):
        return [(i.name, i.value) for i in cls]
