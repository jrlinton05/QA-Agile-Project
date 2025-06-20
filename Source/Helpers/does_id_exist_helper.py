from Source.Helpers.database_query_helper import query_database

def does_id_exist_in_table(product_id, table_name):
    query = f"SELECT 1 FROM {table_name} WHERE product_id = ? LIMIT 1"
    result, con = query_database(query, params=product_id)
    is_in_db = result.fetchone() is not None
    con.close()
    return is_in_db
