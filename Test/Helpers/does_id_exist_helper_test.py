from unittest.mock import patch, MagicMock
import pytest
from Source.Helpers.does_id_exist_helper import does_id_exist_in_table
from Source.Constants.constants import PRODUCT_TABLE_NAME, REVIEW_TABLE_NAME

@patch("Source.Helpers.does_id_exist_helper.query_database")
def test_does_id_exist_in_table_returns_true(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = does_id_exist_in_table("some_id", PRODUCT_TABLE_NAME, "product_id")

    assert result is True
    mock_connection.close.assert_called_once()
    mock_query_database.assert_called_once_with(
        f"SELECT 1 FROM {PRODUCT_TABLE_NAME} WHERE product_id = ? LIMIT 1",
        params=("some_id",)
    )

@patch("Source.Helpers.does_id_exist_helper.query_database")
def test_does_id_exist_in_table_returns_false(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = does_id_exist_in_table("some_id", REVIEW_TABLE_NAME, "review_id")

    assert result is False
    mock_connection.close.assert_called_once()
    mock_query_database.assert_called_once_with(
        f"SELECT 1 FROM {REVIEW_TABLE_NAME} WHERE review_id = ? LIMIT 1",
        params=("some_id",)
    )
