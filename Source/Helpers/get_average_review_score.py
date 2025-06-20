from Source.Helpers.database_query_helper import query_database
from Source.Constants.constants import REVIEW_TABLE_NAME

def get_average_review_score(product_id):
    query = f"SELECT review_score FROM {REVIEW_TABLE_NAME} WHERE product_id = ?"
    cur, con = query_database(query, params=(product_id,))
    result = cur.fetchall()
    con.close()

    if not result:
        return None

    total = sum(score[0] for score in result)
    return total / len(result)
