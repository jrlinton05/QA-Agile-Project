from unittest.mock import patch, MagicMock
import pytest
from Source.Helpers.get_product_by_id_helper import get_product_by_id
from Source.Models.product import Product

@patch("Source.Helpers.get_product_by_id_helper.query_database")
def test_get_product_by_id_returns_product(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("Test Product", "test_image.png")
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    product = get_product_by_id("prod123")

    mock_connection.close.assert_called_once()
    assert isinstance(product, Product)
    assert product.product_id == "prod123"
    assert product.name == "Test Product"
    assert product.image_url == "test_image.png"

@patch("Source.Helpers.get_product_by_id_helper.query_database")
def test_get_product_by_id_returns_none_if_not_found(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    product = get_product_by_id("prod999")

    mock_connection.close.assert_called_once()
    assert product is None
