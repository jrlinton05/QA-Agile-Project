from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Helpers.database_query_helper import query_database


def check_username_matches(table, id_type, item_id, username):
    query = f"SELECT username FROM {table} WHERE {id_type} = ? LIMIT 1"
    cur, con = query_database(query, params=(item_id,))
    owner_username = cur.fetchone()
    con.close()
    if owner_username is None:
        return GenericReturnCodes.ERROR
    owner_username = owner_username[0]
    if username != owner_username:
        return False
    return True