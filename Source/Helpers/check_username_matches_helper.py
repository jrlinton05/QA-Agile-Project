from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Helpers.database_query_helper import query_database


def check_username_matches(table, review_id, username):
    query = f"SELECT username FROM {table} WHERE review_id = ? LIMIT 1"
    cur, con = query_database(query, params=(review_id,))
    owner_username = cur.fetchone()
    con.close()
    if owner_username is None:
        return GenericReturnCodes.ERROR
    owner_username = owner_username[0]
    if username != owner_username:
        return False
    return True