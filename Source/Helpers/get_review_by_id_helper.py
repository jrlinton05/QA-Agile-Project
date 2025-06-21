from Source.Constants.constants import REVIEW_TABLE_NAME
from Source.Helpers.database_query_helper import query_database
from Source.Models.review import Review

def get_review_by_id(review_id):
    query = f"""
        SELECT review_id, review_title, review_body, review_score, username, product_id
        FROM {REVIEW_TABLE_NAME}
        WHERE review_id = ?
        LIMIT 1
    """
    params = (review_id,)
    cur, con = query_database(query, params=params)

    row = cur.fetchone()
    con.close()

    if row is None:
        return None

    review = Review(
        review_id=row[0],
        review_title=row[1],
        review_body=row[2],
        review_score=row[3],
        username=row[4],
        product_id=row[5]
    )
    return review
