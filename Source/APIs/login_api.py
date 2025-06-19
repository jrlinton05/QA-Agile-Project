from Source.Constants.constants import USER_DATABASE_NAME, USER_TABLE_NAME
from Source.APIs.database_query_api import query_database
from Source.APIs.encryption_api import encrypt_string, decrypt_string
from Source.Enums.login_result import LoginResult

def get_user_password_from_db(username):
    query = "SELECT password FROM {table} WHERE username = ? LIMIT 1".format(table = USER_TABLE_NAME)
    result = query_database(USER_DATABASE_NAME, query, params = (username,)).fetchone()
    if result is None:
        return LoginResult.USER_NOT_EXIST
    else:
        return result[0]

def login_user(username, password):
    encrypted_correct_password = get_user_password_from_db(username)
    if encrypted_correct_password == LoginResult.USER_NOT_EXIST:
        return LoginResult.USER_NOT_EXIST

    decrypted_correct_password = decrypt_string(encrypted_correct_password)
    if decrypted_correct_password != password:
        print("Correct: {c} | Submitted: {s}".format(c=decrypted_correct_password, s=password))
        return LoginResult.INCORRECT_PASSWORD
    else:
        return LoginResult.SUCCESS
