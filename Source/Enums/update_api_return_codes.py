from enum import Enum, auto


class UpdateAndDeleteReturnCodes(Enum):
    ITEM_DOES_NOT_EXIST = auto()
    USERNAME_DOES_NOT_MATCH = auto()
