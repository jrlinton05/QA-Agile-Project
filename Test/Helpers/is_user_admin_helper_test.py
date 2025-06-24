from unittest.mock import patch, MagicMock
from Source.Helpers.is_user_admin_helper import is_user_admin
from Source.Enums.generic_return_codes import GenericReturnCodes

@patch("Source.Helpers.is_user_admin_helper.query_database")
def test_is_user_admin_returns_true(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_con = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_con)

    result = is_user_admin("adminuser")

    mock_con.close.assert_called_once()
    assert result is True

@patch("Source.Helpers.is_user_admin_helper.query_database")
def test_is_user_admin_returns_false(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (0,)
    mock_con = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_con)

    result = is_user_admin("normaluser")

    mock_con.close.assert_called_once()
    assert result is False

@patch("Source.Helpers.is_user_admin_helper.query_database")
def test_is_user_admin_returns_error_on_no_user(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_con = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_con)

    result = is_user_admin("missinguser")

    mock_con.close.assert_called_once()
    assert result == GenericReturnCodes.ERROR
