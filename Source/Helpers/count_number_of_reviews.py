from Source.Helpers.database_query_helper import query_database
from Source.Constants.constants import REVIEW_TABLE_NAME

def count_number_of_reviews(product_id):
    query = f"SELECT COUNT(*) FROM {REVIEW_TABLE_NAME} WHERE product_id = ?"
    cur, con = query_database(query, params=(product_id,))
    result = cur.fetchone()
    con.close()
    return result[0] if result else 0
