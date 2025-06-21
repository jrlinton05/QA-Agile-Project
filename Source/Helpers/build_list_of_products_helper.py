from Source.Helpers.database_query_helper import query_database
from Source.Constants.constants import PRODUCT_TABLE_NAME
from Source.Models.product import Product

def build_list_of_products():
    query = f"SELECT product_id, product_name, product_image FROM {PRODUCT_TABLE_NAME}"
    cur, con = query_database(query)
    rows = cur.fetchall()
    con.close()

    products = []
    for row in rows:
        product_id, product_name, product_image = row
        product = Product(product_id, product_name, product_image)
        products.append(product)

    return products
