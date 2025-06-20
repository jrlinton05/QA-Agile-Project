from enum import Enum, auto

class LoginReturnCodes(Enum):
    USER_NOT_EXIST = auto()
    INCORRECT_PASSWORD = auto()