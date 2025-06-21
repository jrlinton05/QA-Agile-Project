import logging
from Source.Constants.constants import PRODUCT_TABLE_NAME
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Enums.update_api_return_codes import UpdateAndDeleteReturnCodes
from Source.Helpers.database_query_helper import query_database

logger = logging.getLogger(__name__)


def update_product(product_id, product_name, product_image):
    query = f'''
    UPDATE {PRODUCT_TABLE_NAME}
    SET product_name = ?, product_image = ?
    WHERE product_id = ?
    '''
    params = (product_name, product_image, product_id)

    con = None
    try:
        _, con = query_database(query, params=params)
        if con.total_changes == 0:
            return UpdateAndDeleteReturnCodes.ITEM_DOES_NOT_EXIST
        return GenericReturnCodes.SUCCESS
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        return GenericReturnCodes.ERROR
    finally:
        if con:
            con.close()
