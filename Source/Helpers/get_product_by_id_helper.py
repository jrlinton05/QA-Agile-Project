from Source.Constants.constants import PRODUCT_TABLE_NAME
from Source.Helpers.database_query_helper import query_database
from Source.Models.product import Product

def get_product_by_id(product_id):
    query = f"""
        SELECT product_name, product_image
        FROM {PRODUCT_TABLE_NAME}
        WHERE product_id = ?
        LIMIT 1
    """
    params = (product_id,)
    cur, con = query_database(query, params=params)

    row = cur.fetchone()
    con.close()

    if row is None:
        return None

    product = Product(
        product_id=product_id,
        name=row[0],
        image_url=row[1],
    )
    return product
