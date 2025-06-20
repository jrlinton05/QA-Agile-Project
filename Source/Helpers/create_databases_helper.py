from Source.Helpers.database_query_helper import query_database
from Source.Constants.constants import USER_TABLE_NAME, PRODUCT_TABLE_NAME, REVIEW_TABLE_NAME


def create_user_db_if_not_exists():
    query = f'''
    CREATE TABLE IF NOT EXISTS {USER_TABLE_NAME} (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        is_admin INTEGER NOT NULL
    )
    '''
    _, con = query_database(query)
    con.close()

def create_product_db_if_not_exists():
    query = f'''
    CREATE TABLE IF NOT EXISTS {PRODUCT_TABLE_NAME} (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        product_image TEXT NOT NULL
    )
    '''
    _, con = query_database(query)
    con.close()

def create_review_db_if_not_exists():
    query = f'''
    CREATE TABLE IF NOT EXISTS {REVIEW_TABLE_NAME} (
        review_id TEXT PRIMARY KEY,
        product_id TEXT NOT NULL,
        username TEXT NOT NULL,
        review_title TEXT NOT NULL,
        review_body TEXT NOT NULL,
        review_score INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES {PRODUCT_TABLE_NAME}(product_id),
        FOREIGN KEY (username) REFERENCES {USER_TABLE_NAME}(username)
    )
    '''
    _, con = query_database(query)
    con.close()

if __name__ == "__main__":
    create_user_db_if_not_exists()
    create_product_db_if_not_exists()
    create_review_db_if_not_exists()