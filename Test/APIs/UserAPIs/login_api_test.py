from unittest.mock import patch, MagicMock
import pytest
from Source.APIs.UserAPIs.login_api import (
    get_user_password_from_db,
    validate_user_login,
)
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Enums.login_return_codes import LoginReturnCodes


@patch("Source.APIs.UserAPIs.login_api.query_database")
@patch("Source.APIs.UserAPIs.login_api.logger")
def test_get_user_password_from_db_user_exists(mock_logger, mock_query):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("encrypted_pass",)
    mock_query.return_value = (mock_cursor, MagicMock())

    result = get_user_password_from_db("testuser")

    assert result == "encrypted_pass"
    mock_query.assert_called_once()
    mock_cursor.fetchone.assert_called_once()


@patch("Source.APIs.UserAPIs.login_api.query_database")
@patch("Source.APIs.UserAPIs.login_api.logger")
def test_get_user_password_from_db_user_not_exist(mock_logger, mock_query):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_query.return_value = (mock_cursor, MagicMock())

    result = get_user_password_from_db("nonexistentuser")

    assert result == LoginReturnCodes.USER_NOT_EXIST
    mock_logger.warning.assert_called_once()


@patch("Source.APIs.UserAPIs.login_api.decrypt_string")
@patch("Source.APIs.UserAPIs.login_api.get_user_password_from_db")
@patch("Source.APIs.UserAPIs.login_api.logger")
def test_validate_user_login_success(mock_logger, mock_get_password, mock_decrypt):
    mock_get_password.return_value = "encrypted_pass"
    mock_decrypt.return_value = "correct_password"

    result = validate_user_login("testuser", "correct_password")

    assert result == GenericReturnCodes.SUCCESS
    mock_logger.info.assert_called_once_with("User 'testuser' logged in successfully")


@patch("Source.APIs.UserAPIs.login_api.get_user_password_from_db")
def test_validate_user_login_user_not_exist(mock_get_password):
    mock_get_password.return_value = LoginReturnCodes.USER_NOT_EXIST

    result = validate_user_login("unknownuser", "any_password")

    assert result == LoginReturnCodes.USER_NOT_EXIST


@patch("Source.APIs.UserAPIs.login_api.decrypt_string")
@patch("Source.APIs.UserAPIs.login_api.get_user_password_from_db")
@patch("Source.APIs.UserAPIs.login_api.logger")
def test_validate_user_login_incorrect_password(mock_logger, mock_get_password, mock_decrypt):
    mock_get_password.return_value = "encrypted_pass"
    mock_decrypt.return_value = "wrong_password"

    result = validate_user_login("testuser", "input_password")

    assert result == LoginReturnCodes.INCORRECT_PASSWORD
    mock_logger.info.assert_called_once_with("Incorrect password attempt for user 'testuser'")
