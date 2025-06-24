from unittest.mock import patch, MagicMock
from Source.Helpers.build_list_of_products_helper import build_list_of_products
from Source.Constants.constants import PRODUCT_TABLE_NAME
from Source.Models.product import Product

@patch("Source.Helpers.build_list_of_products_helper.query_database")
def test_query_database_called_with_correct_query(mock_query_database):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    build_list_of_products()

    expected_query = f"SELECT product_id, product_name, product_image FROM {PRODUCT_TABLE_NAME}"
    mock_query_database.assert_called_once_with(expected_query)


@patch("Source.Helpers.build_list_of_products_helper.query_database")
def test_returns_list_of_product_objects(mock_query_database):
    rows = [
        ("id1", "Product 1", "image1.png"),
        ("id2", "Product 2", "image2.png")
    ]
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = rows
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = build_list_of_products()

    assert isinstance(result, list)
    assert all(isinstance(p, Product) for p in result)
    assert len(result) == 2
    assert result[0].product_id == "id1"
    assert result[0].name == "Product 1"
    assert result[0].image_url == "image1.png"


@patch("Source.Helpers.build_list_of_products_helper.query_database")
def test_closes_database_connection(mock_query_database):
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    build_list_of_products()

    mock_connection.close.assert_called_once()


@patch("Source.Helpers.build_list_of_products_helper.query_database")
def test_handles_empty_result_set(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = build_list_of_products()

    assert result == []