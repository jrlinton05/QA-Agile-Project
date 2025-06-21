from enum import Enum, auto


class DeleteReturnCodes(Enum):
    ITEM_DOES_NOT_EXIST = auto()
    USERNAME_DOES_NOT_MATCH = auto()
