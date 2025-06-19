import re

from Source.Constants.constants import DATABASE_FILE_NAME, USER_TABLE_NAME
from Source.APIs.database_query_api import query_database
from Source.APIs.encryption_api import encrypt_string
from Source.Enums.registration_result import RegistrationResult

def validate_user_not_in_db(username):
    query = "SELECT 1 FROM {table} WHERE username = ? LIMIT 1".format(table = USER_TABLE_NAME)
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
        return RegistrationResult.PASSWORDS_DO_NOT_MATCH
    if not validate_user_not_in_db(username):
        return RegistrationResult.USER_IN_DATABASE
    if not validate_password(password):
        return RegistrationResult.PASSWORD_INVALID

    encrypted_password = encrypt_string(password)

    query = "INSERT INTO {table} VALUES(?, ?, {admin})".format(table = USER_TABLE_NAME, admin = 1 if is_admin else 0)
    try:
        _, con = query_database(query, params = (username, encrypted_password))
        con.close()
    except Exception as e:
        return e
    else:
        return RegistrationResult.SUCCESS
