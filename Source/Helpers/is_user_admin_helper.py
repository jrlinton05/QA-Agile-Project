from Source.Constants.constants import USER_TABLE_NAME
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Helpers.database_query_helper import query_database


def is_user_admin(username):
    query = f"SELECT is_admin FROM {USER_TABLE_NAME} WHERE username=?"
    cur, con = query_database(query, params=(username,))
    result = cur.fetchone()
    con.close()
    if result is None:
        return GenericReturnCodes.ERROR
    else:
        return bool(result[0])
