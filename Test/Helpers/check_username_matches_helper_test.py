from unittest.mock import patch, MagicMock
from Source.Helpers.check_username_matches_helper import check_username_matches
from Source.Enums.generic_return_codes import GenericReturnCodes


@patch("Source.Helpers.check_username_matches_helper.query_database")
def test_returns_error_when_no_username_found(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = check_username_matches("some_table", "review123", "user1")

    assert result == GenericReturnCodes.ERROR
    mock_connection.close.assert_called_once()


@patch("Source.Helpers.check_username_matches_helper.query_database")
def test_returns_false_when_username_does_not_match(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("other_user",)
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = check_username_matches("some_table", "review123", "user1")

    assert result is False
    mock_connection.close.assert_called_once()


@patch("Source.Helpers.check_username_matches_helper.query_database")
def test_returns_true_when_username_matches(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("user1",)
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = check_username_matches("some_table", "review123", "user1")

    assert result is True
    mock_connection.close.assert_called_once()
