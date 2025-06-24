import logging
from unittest.mock import patch
from Source.APIs.ProductAPIs.create_product_api import create_product
from Source.Enums.generic_return_codes import GenericReturnCodes


def test_generate_random_id_called_until_unique():
    with patch('Source.APIs.ProductAPIs.create_product_api.generate_random_id') as mock_generate_id, \
            patch('Source.APIs.ProductAPIs.create_product_api.does_id_exist_in_table') as mock_exists, \
            patch('Source.APIs.ProductAPIs.create_product_api.query_database') as mock_query:

        mock_generate_id.side_effect = ['id1', 'id2', 'id3', 'id4', 'id5']
        mock_exists.side_effect = [True, True, True, True, False]
        mock_query.return_value = None

        result = create_product("Test Product", "image_url")

        assert mock_generate_id.call_count == 5

        mock_exists.assert_any_call('id1', 'Products', 'product_id')
        mock_exists.assert_any_call('id2', 'Products', 'product_id')
        mock_exists.assert_any_call('id3', 'Products', 'product_id')
        mock_exists.assert_any_call('id4', 'Products', 'product_id')
        mock_exists.assert_any_call('id5', 'Products', 'product_id')

        assert result == GenericReturnCodes.SUCCESS

def test_query_database_called_with_correct_params():
    with patch('Source.APIs.ProductAPIs.create_product_api.generate_random_id', return_value='unique_id') as mock_id, \
            patch('Source.APIs.ProductAPIs.create_product_api.does_id_exist_in_table', return_value=False), \
            patch('Source.APIs.ProductAPIs.create_product_api.query_database') as mock_query:

        create_product("Test Product", "test_image.jpg")
        mock_query.assert_called_once_with(
            '''
    INSERT INTO Products (product_id, product_name, product_image)
    VALUES (?, ?, ?)
    ''',
            params=('unique_id', 'Test Product', 'test_image.jpg')
        )

def test_returns_success_on_successful_insert():
    with patch('Source.APIs.ProductAPIs.create_product_api.generate_random_id', return_value='id'), \
            patch('Source.APIs.ProductAPIs.create_product_api.does_id_exist_in_table', return_value=False), \
            patch('Source.APIs.ProductAPIs.create_product_api.query_database'):

        result = create_product("Product", "img.jpg")
        assert result == GenericReturnCodes.SUCCESS

def test_logs_success_message_on_success(caplog):
    with patch('Source.APIs.ProductAPIs.create_product_api.generate_random_id', return_value='newid'), \
            patch('Source.APIs.ProductAPIs.create_product_api.does_id_exist_in_table', return_value=False), \
            patch('Source.APIs.ProductAPIs.create_product_api.query_database'):

        with caplog.at_level(logging.INFO):
            create_product("Product", "img.jpg")
            assert any("Product created successfully with ID: newid" in msg for msg in caplog.messages)

def test_returns_error_on_database_exception():
    with patch('Source.APIs.ProductAPIs.create_product_api.generate_random_id', return_value='id'), \
            patch('Source.APIs.ProductAPIs.create_product_api.does_id_exist_in_table', return_value=False), \
            patch('Source.APIs.ProductAPIs.create_product_api.query_database', side_effect=Exception("DB fail")):

        result = create_product("Product", "img.jpg")
        assert result == GenericReturnCodes.ERROR

def test_logs_error_message_on_database_exception(caplog):
    with patch('Source.APIs.ProductAPIs.create_product_api.generate_random_id', return_value='id'), \
            patch('Source.APIs.ProductAPIs.create_product_api.does_id_exist_in_table', return_value=False), \
            patch('Source.APIs.ProductAPIs.create_product_api.query_database', side_effect=Exception("DB fail")):

        with caplog.at_level(logging.ERROR):
            create_product("Product", "img.jpg")
            assert any("Error creating product" in msg for msg in caplog.messages)
