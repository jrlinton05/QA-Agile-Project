from Source.Constants.constants import PRODUCT_TABLE_NAME
from Source.Enums.delete_api_return_codes import DeleteReturnCodes
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Helpers.check_username_matches_helper import check_username_matches
from Source.Helpers.database_query_helper import query_database


def delete_product(product_id, username):
    does_username_match = check_username_matches(PRODUCT_TABLE_NAME, "product_id", product_id, username)
    if does_username_match == GenericReturnCodes.ERROR:
        return DeleteReturnCodes.ITEM_DOES_NOT_EXIST
    elif not does_username_match:
        return DeleteReturnCodes.USERNAME_DOES_NOT_MATCH

    try:
        query = f"DELETE FROM {PRODUCT_TABLE_NAME} WHERE product_id = ?"
        _, con = query_database(query, params=(product_id,))
        con.close()
    except:
        return GenericReturnCodes.ERROR
    else:
        return GenericReturnCodes.SUCCESS
