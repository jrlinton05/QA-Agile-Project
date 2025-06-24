from unittest.mock import patch, MagicMock
from Source.Constants.constants import USER_TABLE_NAME, PRODUCT_TABLE_NAME, REVIEW_TABLE_NAME
from Source.Helpers.create_databases_helper import (
    create_user_db_if_not_exists,
    create_product_db_if_not_exists,
    create_review_db_if_not_exists,
)

@patch("Source.Helpers.create_databases_helper.query_database")
def test_create_user_db_executes_correct_query(mock_query_database):
    mock_connection = MagicMock()
    mock_query_database.return_value = (None, mock_connection)

    create_user_db_if_not_exists()

    expected_sql = f'''
    CREATE TABLE IF NOT EXISTS {USER_TABLE_NAME} (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        is_admin INTEGER NOT NULL
    )
    '''
    mock_query_database.assert_called_once_with(expected_sql)
    mock_connection.close.assert_called_once()

@patch("Source.Helpers.create_databases_helper.query_database")
def test_create_product_db_executes_correct_query(mock_query_database):
    mock_connection = MagicMock()
    mock_query_database.return_value = (None, mock_connection)

    create_product_db_if_not_exists()

    expected_sql = f'''
    CREATE TABLE IF NOT EXISTS {PRODUCT_TABLE_NAME} (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        product_image TEXT NOT NULL
    )
    '''
    mock_query_database.assert_called_once_with(expected_sql)
    mock_connection.close.assert_called_once()

@patch("Source.Helpers.create_databases_helper.query_database")
def test_create_review_db_executes_correct_query(mock_query_database):
    mock_connection = MagicMock()
    mock_query_database.return_value = (None, mock_connection)

    create_review_db_if_not_exists()

    expected_sql = f'''
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
    mock_query_database.assert_called_once_with(expected_sql)
    mock_connection.close.assert_called_once()
