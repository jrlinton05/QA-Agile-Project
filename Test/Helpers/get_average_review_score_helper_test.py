from unittest.mock import patch, MagicMock
import pytest
from Source.Helpers.get_average_review_score_helper import get_average_review_score

@patch("Source.Helpers.get_average_review_score_helper.query_database")
def test_returns_average_score(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(5,), (3,), (4,)]
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = get_average_review_score("prod1")
    mock_connection.close.assert_called_once()
    assert result == 4.0  # (5+3+4)/3 = 4.0

@patch("Source.Helpers.get_average_review_score_helper.query_database")
def test_returns_none_when_no_reviews(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = get_average_review_score("prod2")
    mock_connection.close.assert_called_once()
    assert result is None
