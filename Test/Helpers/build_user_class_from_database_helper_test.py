from unittest.mock import patch, MagicMock
from Source.Helpers.build_user_class_from_database_helper import build_user
from Source.Constants.constants import USER_TABLE_NAME
from Source.Models.user import User

@patch("Source.Helpers.build_user_class_from_database_helper.query_database")
def test_returns_none_if_user_not_found(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = build_user("nonexistent_user")

    mock_query_database.assert_called_once_with(
        f"SELECT is_admin FROM {USER_TABLE_NAME} WHERE username = ? LIMIT 1",
        params=("nonexistent_user",)
    )
    mock_connection.close.assert_called_once()
    assert result is None

@patch("Source.Helpers.build_user_class_from_database_helper.query_database")
def test_returns_user_object_if_found(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    username = "testuser"
    result = build_user(username)

    mock_query_database.assert_called_once_with(
        f"SELECT is_admin FROM {USER_TABLE_NAME} WHERE username = ? LIMIT 1",
        params=(username,)
    )
    mock_connection.close.assert_called_once()
    assert isinstance(result, User)
    assert result.username == username
    assert result.is_admin is True
