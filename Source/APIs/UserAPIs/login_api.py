from Source.Constants.constants import USER_TABLE_NAME
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Helpers.database_query_helper import query_database
from Source.Helpers.encryption_helper import decrypt_string
from Source.Enums.login_return_codes import LoginReturnCodes


def get_user_password_from_db(username):
    query = f"SELECT password FROM {USER_TABLE_NAME} WHERE username = ? LIMIT 1"
    result, con = query_database(query, params=(username,))
    result = result.fetchone()
    con.close()
    if result is None:
        return LoginReturnCodes.USER_NOT_EXIST
    else:
        return result[0]


def validate_user_login(username, password):
    encrypted_correct_password = get_user_password_from_db(username)
    if encrypted_correct_password == LoginReturnCodes.USER_NOT_EXIST:
        return LoginReturnCodes.USER_NOT_EXIST

    decrypted_correct_password = decrypt_string(encrypted_correct_password)
    if decrypted_correct_password != password:
        return LoginReturnCodes.INCORRECT_PASSWORD
    else:
        return GenericReturnCodes.SUCCESS
