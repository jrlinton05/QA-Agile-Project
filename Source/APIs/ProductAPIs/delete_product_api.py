import logging
from Source.Constants.constants import PRODUCT_TABLE_NAME, REVIEW_TABLE_NAME
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Enums.update_api_return_codes import UpdateAndDeleteReturnCodes
from Source.Helpers.database_query_helper import query_database

logger = logging.getLogger(__name__)


def delete_product(product_id):
    try:
        cur_reviews, con = query_database(
            f"DELETE FROM {REVIEW_TABLE_NAME} WHERE product_id = ?", params=(product_id,)
        )
        logger.info(f"Deleted {cur_reviews.rowcount} reviews for product_id {product_id}")

        cur_product, _ = query_database(
            f"DELETE FROM {PRODUCT_TABLE_NAME} WHERE product_id = ?", params=(product_id,)
        )

        if cur_product.rowcount == 0:
            logger.info(f"Delete failed: product_id {product_id} does not exist")
            con.close()
            return UpdateAndDeleteReturnCodes.ITEM_DOES_NOT_EXIST

        logger.info(f"Deleted product_id {product_id} successfully")
        con.close()
        return GenericReturnCodes.SUCCESS

    except Exception as e:
        logger.error(f"Error deleting product_id {product_id}: {e}")
        try:
            con.close()
        except Exception:
            pass
        return GenericReturnCodes.ERROR