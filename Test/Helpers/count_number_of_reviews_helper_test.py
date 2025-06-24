from unittest.mock import patch, MagicMock
from Source.Helpers.count_number_of_reviews_helper import count_number_of_reviews

@patch("Source.Helpers.count_number_of_reviews_helper.query_database")
def test_returns_correct_count_when_result_exists(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (5,)
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = count_number_of_reviews("prod123")

    assert result == 5
    mock_connection.close.assert_called_once()

@patch("Source.Helpers.count_number_of_reviews_helper.query_database")
def test_returns_zero_when_no_result(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = count_number_of_reviews("prod123")

    assert result == 0
    mock_connection.close.assert_called_once()
