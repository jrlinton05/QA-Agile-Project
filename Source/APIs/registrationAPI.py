from Source.Constants.Constants import USER_DATABASE_NAME, USER_TABLE_NAME
from Source.APIs.databaseQueryAPI import query_database
from Source.APIs.encryptionAPI import encrypt_string

def validate_user_not_in_db(username):
    query = "SELECT 1 FROM {table} WHERE username = ? LIMIT 1".format(table = USER_TABLE_NAME)
    result = query_database(USER_DATABASE_NAME, query, params = (username,))
    return result.fetchone() is None

def repeated_password_matches_password(password, repeated_password):
    return password == repeated_password

def register_new_user(username, password, repeated_password, is_admin):
    if not repeated_password_matches_password(password, repeated_password):
        return "passwordsDoNotMatch"
    if not validate_user_not_in_db(username):
        return "userInDatabase"

    encrypted_password = encrypt_string(password)

    query = "INSERT INTO {table} VALUES(?, ?, {admin})".format(table = USER_TABLE_NAME, admin = 1 if is_admin else 0)
    try:
        query_database(USER_DATABASE_NAME, query, params = (username, encrypted_password))
    except:
        return "unknownError"
    else:
        return "success"
