from unittest.mock import patch, MagicMock
from Source.APIs.ProductAPIs.delete_product_api import delete_product
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Enums.update_api_return_codes import UpdateAndDeleteReturnCodes


@patch("Source.APIs.ProductAPIs.delete_product_api.query_database")
def test_deletes_reviews_and_product_successfully(mock_query):
    mock_review_cursor = MagicMock(rowcount=2)
    mock_product_cursor = MagicMock(rowcount=1)
    mock_connection = MagicMock()

    mock_query.side_effect = [
        (mock_review_cursor, mock_connection),
        (mock_product_cursor, mock_connection)
    ]

    result = delete_product("p1")

    assert result == GenericReturnCodes.SUCCESS
    assert mock_query.call_count == 2
    mock_query.assert_any_call(
        "DELETE FROM Reviews WHERE product_id = ?", params=("p1",)
    )
    mock_query.assert_any_call(
        "DELETE FROM Products WHERE product_id = ?", params=("p1",)
    )
    mock_connection.close.assert_called_once()


@patch("Source.APIs.ProductAPIs.delete_product_api.query_database")
def test_returns_item_does_not_exist_if_product_not_found(mock_query):
    mock_review_cursor = MagicMock(rowcount=0)
    mock_product_cursor = MagicMock(rowcount=0)
    mock_connection = MagicMock()

    mock_query.side_effect = [
        (mock_review_cursor, mock_connection),
        (mock_product_cursor, mock_connection)
    ]

    result = delete_product("p2")

    assert result == UpdateAndDeleteReturnCodes.ITEM_DOES_NOT_EXIST
    mock_connection.close.assert_called_once()


@patch("Source.APIs.ProductAPIs.delete_product_api.query_database")
def test_returns_error_if_exception_raised(mock_query):
    mock_query.side_effect = Exception("DB failure")

    result = delete_product("p3")

    assert result == GenericReturnCodes.ERROR
