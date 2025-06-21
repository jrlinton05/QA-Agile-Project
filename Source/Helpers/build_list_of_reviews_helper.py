from Source.Helpers.database_query_helper import query_database
from Source.Constants.constants import REVIEW_TABLE_NAME
from Source.Models.review import Review


def build_list_of_reviews(product_id):
    query = f"SELECT review_title, review_body, review_score, username FROM {REVIEW_TABLE_NAME} WHERE product_id = ?"
    cur, con = query_database(query, params=(product_id,))
    rows = cur.fetchall()
    con.close()

    reviews = []
    for row in rows:
        review_title, review_body, review_score, username = row
        review = Review(review_title, review_body, review_score, username)
        reviews.append(review)

    return reviews
