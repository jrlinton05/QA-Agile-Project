from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Helpers.database_query_helper import query_database
from Source.Constants.constants import PRODUCT_TABLE_NAME
from Source.Helpers.does_id_exist_helper import does_id_exist_in_table
from Source.Helpers.random_id_helper import generate_random_id


def create_product(product_name, product_image):
    unique_id_generated = False
    while not unique_id_generated:
        random_id = generate_random_id()
        unique_id_generated = not does_id_exist_in_table(random_id, PRODUCT_TABLE_NAME)

    query = f'''
    INSERT INTO {PRODUCT_TABLE_NAME} (product_id, product_name, product_image)
    VALUES (?, ?, ?)
    '''
    try:
        query_database(query, params=(random_id, product_name, product_image))
    except:
        return GenericReturnCodes.ERROR
    else:
        return random_id
