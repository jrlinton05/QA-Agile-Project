from Source.APIs.database_query_api import query_database
from Source.Constants.constants import USER_TABLE_NAME, PRODUCT_TABLE_NAME, REVIEW_TABLE_NAME


def create_user_db_if_not_exists():
    query = '''
    CREATE TABLE IF NOT EXISTS {table_name} (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        is_admin INTEGER NOT NULL
    )
    '''.format(table_name=USER_TABLE_NAME)
    _, con = query_database(query)
    con.close()

def create_product_db_if_not_exists():
    query = '''
    CREATE TABLE IF NOT EXISTS {table_name} (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        product_image TEXT NOT NULL
    )
    '''.format(table_name=PRODUCT_TABLE_NAME)
    _, con = query_database(query)
    con.close()

def create_review_db_if_not_exists():
    query = '''
    CREATE TABLE IF NOT EXISTS {table_name} (
        review_id TEXT PRIMARY KEY,
        product_id TEXT NOT NULL,
        username TEXT NOT NULL,
        review_title TEXT NOT NULL,
        review_body TEXT NOT NULL,
        review_score INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES {product_table_name}(product_id),
        FOREIGN KEY (username) REFERENCES {user_table_name}(username)
    )
    '''.format(table_name=REVIEW_TABLE_NAME, product_table_name=PRODUCT_TABLE_NAME, user_table_name=USER_TABLE_NAME)
    _, con = query_database(query)
    con.close()

if __name__ == "__main__":
    create_user_db_if_not_exists()
    create_product_db_if_not_exists()
    create_review_db_if_not_exists()