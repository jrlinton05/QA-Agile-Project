import logging
from Source.Constants.constants import REVIEW_TABLE_NAME
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Helpers.database_query_helper import query_database
from Source.Helpers.does_id_exist_helper import does_id_exist_in_table
from Source.Helpers.random_id_helper import generate_random_id

logger = logging.getLogger(__name__)

def create_review(review_title, review_body, review_score, product_id, username):
    unique_id_generated = False
    while not unique_id_generated:
        random_id = generate_random_id()
        unique_id_generated = not does_id_exist_in_table(random_id, REVIEW_TABLE_NAME, "review_id")

    query = f'''
        INSERT INTO {REVIEW_TABLE_NAME} (
            review_id, product_id, username, review_title, review_body, review_score
        ) VALUES (?, ?, ?, ?, ?, ?)
    '''

    try:
        query_database(
            query,
            params=(
                random_id,
                product_id,
                username,
                review_title,
                review_body,
                review_score,
            ),
        )
        logger.info(f"Review created successfully with ID: {random_id}")
    except Exception as e:
        logger.error(f"Error creating review: {e}")
        return GenericReturnCodes.ERROR
    else:
        return GenericReturnCodes.SUCCESS
