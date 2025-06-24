from Source.Helpers.database_query_helper import query_database

def does_id_exist_in_table(id_value, table_name, column_name):
    query = f"SELECT 1 FROM {table_name} WHERE {column_name} = ? LIMIT 1"
    result, con = query_database(query, params=(id_value,))
    is_in_db = result.fetchone() is not None
    con.close()
    return is_in_db
