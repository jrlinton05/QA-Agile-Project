from Source.Constants.constants import PRODUCT_TABLE_NAME, REVIEW_TABLE_NAME
from Source.Enums.delete_api_return_codes import DeleteReturnCodes
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Helpers.check_username_matches_helper import check_username_matches
from Source.Helpers.database_query_helper import query_database


def delete_review(review_id, username):
    does_username_match = check_username_matches(REVIEW_TABLE_NAME, "review_id", review_id, username)
    if does_username_match == GenericReturnCodes.ERROR:
        return DeleteReturnCodes.ITEM_DOES_NOT_EXIST
    elif not does_username_match:
        return DeleteReturnCodes.USERNAME_DOES_NOT_MATCH

    try:
        query = f"DELETE FROM {REVIEW_TABLE_NAME} WHERE review_id = ?"
        _, con = query_database(query, params=(review_id,))
        con.close()
    except:
        return GenericReturnCodes.ERROR
    else:
        return GenericReturnCodes.SUCCESS
