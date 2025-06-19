from enum import Enum, auto

class LoginResult(Enum):
    USER_NOT_EXIST = auto()
    INCORRECT_PASSWORD = auto()
    SUCCESS = auto()