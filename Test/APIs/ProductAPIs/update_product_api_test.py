from unittest.mock import patch, MagicMock
from Source.APIs.ProductAPIs.update_product_api import update_product
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Enums.update_api_return_codes import UpdateAndDeleteReturnCodes


@patch("Source.APIs.ProductAPIs.update_product_api.query_database")
def test_returns_success_when_update_applied(mock_query):
    mock_connection = MagicMock()
    mock_connection.total_changes = 1
    mock_query.return_value = (None, mock_connection)

    result = update_product("prod123", "Updated Name", "updated_img.jpg")

    assert result == GenericReturnCodes.SUCCESS
    mock_query.assert_called_once()
    mock_connection.close.assert_called_once()


@patch("Source.APIs.ProductAPIs.update_product_api.query_database")
def test_returns_item_does_not_exist_when_no_rows_changed(mock_query):
    mock_connection = MagicMock()
    mock_connection.total_changes = 0
    mock_query.return_value = (None, mock_connection)

    result = update_product("prod123", "New Name", "new_img.jpg")

    assert result == UpdateAndDeleteReturnCodes.ITEM_DOES_NOT_EXIST
    mock_connection.close.assert_called_once()


@patch("Source.APIs.ProductAPIs.update_product_api.query_database", side_effect=Exception("DB fail"))
@patch("Source.APIs.ProductAPIs.update_product_api.logger")
def test_returns_error_on_exception(mock_logger, mock_query):
    result = update_product("prod123", "Name", "img.jpg")

    assert result == GenericReturnCodes.ERROR
    mock_logger.error.assert_called_once()
