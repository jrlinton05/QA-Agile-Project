import logging
from Source.Constants.constants import USER_TABLE_NAME
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Helpers.database_query_helper import query_database
from Source.Helpers.encryption_helper import decrypt_string
from Source.Enums.login_return_codes import LoginReturnCodes

logger = logging.getLogger(__name__)

def get_user_password_from_db(username):
    query = f"SELECT password FROM {USER_TABLE_NAME} WHERE username = ? LIMIT 1"
    result, con = query_database(query, params=(username,))
    row = result.fetchone()
    con.close()

    if row is None:
        logger.warning(f"User '{username}' not found in database")
        return LoginReturnCodes.USER_NOT_EXIST

    return row[0]


def validate_user_login(username, password):
    encrypted_correct_password = get_user_password_from_db(username)
    if encrypted_correct_password == LoginReturnCodes.USER_NOT_EXIST:
        return LoginReturnCodes.USER_NOT_EXIST

    decrypted_correct_password = decrypt_string(encrypted_correct_password)
    if decrypted_correct_password != password:
        logger.info(f"Incorrect password attempt for user '{username}'")
        return LoginReturnCodes.INCORRECT_PASSWORD

    logger.info(f"User '{username}' logged in successfully")
    return GenericReturnCodes.SUCCESS
