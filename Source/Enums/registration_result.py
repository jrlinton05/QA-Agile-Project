from enum import Enum, auto

class RegistrationResult(Enum):
    PASSWORDS_DO_NOT_MATCH = auto()
    USER_IN_DATABASE = auto()
    SUCCESS = auto()
    PASSWORD_INVALID = auto()