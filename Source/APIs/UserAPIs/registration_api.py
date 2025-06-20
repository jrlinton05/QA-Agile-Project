import re

from Source.Constants.constants import USER_TABLE_NAME
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Helpers.database_query_helper import query_database
from Source.Helpers.encryption_helper import encrypt_string
from Source.Enums.registration_return_codes import RegistrationReturnCodes

def validate_user_not_in_db(username):
    query = f"SELECT 1 FROM {USER_TABLE_NAME} WHERE username = ? LIMIT 1"
    result, con = query_database(query, params = (username,))
    is_valid = result.fetchone() is None
    con.close()
    return is_valid

def repeated_password_matches_password(password, repeated_password):
    return password == repeated_password

def validate_password(password):
    pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{10,}$"
    return re.fullmatch(pattern, password) is not None

def register_new_user(username, password, repeated_password, is_admin):
    if not repeated_password_matches_password(password, repeated_password):
        return RegistrationReturnCodes.PASSWORDS_DO_NOT_MATCH
    if not validate_user_not_in_db(username):
        return RegistrationReturnCodes.USER_IN_DATABASE
    if not validate_password(password):
        return RegistrationReturnCodes.PASSWORD_INVALID

    encrypted_password = encrypt_string(password)

    int_is_admin = 1 if is_admin else 0
    query = f"INSERT INTO {USER_TABLE_NAME} VALUES(?, ?, {int_is_admin})"
    try:
        _, con = query_database(query, params = (username, encrypted_password))
        con.close()
    except Exception as e:
        return e
    else:
        return GenericReturnCodes.SUCCESS
