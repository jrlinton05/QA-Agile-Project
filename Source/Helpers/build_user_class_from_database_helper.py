from Source.Constants.constants import USER_TABLE_NAME
from Source.Helpers.database_query_helper import query_database
from Source.Models.user import User


def build_user(username):
    query = f"SELECT is_admin FROM {USER_TABLE_NAME} WHERE username = ? LIMIT 1"
    cur, con = query_database(query, params=(username,))
    result = cur.fetchone()
    con.close()
    if result is None:
        return None
    else:
        return User(username, bool(result[0]))