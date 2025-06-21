import logging
from Source.Constants.constants import REVIEW_TABLE_NAME
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Enums.update_api_return_codes import UpdateAndDeleteReturnCodes
from Source.Helpers.check_username_matches_helper import check_username_matches
from Source.Helpers.database_query_helper import query_database

logger = logging.getLogger(__name__)

def update_review(username, review_id, review_title, review_body, review_score, is_admin):
    if not is_admin:
        does_username_match = check_username_matches(REVIEW_TABLE_NAME, review_id, username)
        if does_username_match == GenericReturnCodes.ERROR:
            logger.warning(f"Review ID {review_id} does not exist when checking username match for update.")
            return UpdateAndDeleteReturnCodes.ITEM_DOES_NOT_EXIST
        elif not does_username_match:
            logger.warning(f"Username '{username}' does not match owner of review ID {review_id} for update.")
            return UpdateAndDeleteReturnCodes.USERNAME_DOES_NOT_MATCH

    query = f'''
    UPDATE {REVIEW_TABLE_NAME}
    SET review_title = ?, review_body = ?, review_score = ?
    WHERE review_id = ?
    '''
    params = (review_title, review_body, review_score, review_id)

    try:
        query_database(query, params=params)
        logger.info(f"Review ID {review_id} updated successfully by user '{username}'.")
    except Exception as e:
        logger.error(f"Error updating review ID {review_id}: {e}")
        return GenericReturnCodes.ERROR
    else:
        return GenericReturnCodes.SUCCESS
