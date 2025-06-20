from enum import Enum, auto

class RegistrationReturnCodes(Enum):
    PASSWORDS_DO_NOT_MATCH = auto()
    USER_IN_DATABASE = auto()
    PASSWORD_INVALID = auto()