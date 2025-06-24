from unittest.mock import patch, MagicMock
import pytest
from Source.APIs.UserAPIs.registration_api import (
    validate_user_not_in_db,
    repeated_password_matches_password,
    validate_password,
    register_new_user,
)
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Enums.registration_return_codes import RegistrationReturnCodes


@patch("Source.APIs.UserAPIs.registration_api.query_database")
def test_validate_user_not_in_db_user_not_exists(mock_query):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_query.return_value = (mock_cursor, MagicMock())

    assert validate_user_not_in_db("newuser") is True
    mock_query.assert_called_once()


@patch("Source.APIs.UserAPIs.registration_api.query_database")
def test_validate_user_not_in_db_user_exists(mock_query):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_query.return_value = (mock_cursor, MagicMock())

    assert validate_user_not_in_db("existinguser") is False


def test_repeated_password_matches_password_true():
    assert repeated_password_matches_password("Password123", "Password123") is True


def test_repeated_password_matches_password_false():
    assert repeated_password_matches_password("Password123", "Password124") is False


def test_validate_password_valid():
    valid_password = "ValidPass123"
    assert validate_password(valid_password) is True


def test_validate_password_invalid():
    invalid_passwords = ["short1A", "nouppercase123", "NOLOWERCASE123", "NoDigitsHere", "1234567890"]
    for pwd in invalid_passwords:
        assert validate_password(pwd) is False


@patch("Source.APIs.UserAPIs.registration_api.encrypt_string", return_value="encrypted_pw")
@patch("Source.APIs.UserAPIs.registration_api.validate_user_not_in_db", return_value=True)
def test_register_new_user_passwords_do_not_match(mock_validate_user, mock_encrypt):
    result = register_new_user("user", "Password123", "Password124", False)
    assert result == RegistrationReturnCodes.PASSWORDS_DO_NOT_MATCH


@patch("Source.APIs.UserAPIs.registration_api.validate_user_not_in_db", return_value=False)
def test_register_new_user_user_already_exists(mock_validate_user):
    result = register_new_user("user", "Password123", "Password123", False)
    assert result == RegistrationReturnCodes.USER_IN_DATABASE


@patch("Source.APIs.UserAPIs.registration_api.validate_user_not_in_db", return_value=True)
def test_register_new_user_password_invalid(mock_validate_user):
    result = register_new_user("user", "invalid", "invalid", False)
    assert result == RegistrationReturnCodes.PASSWORD_INVALID


@patch("Source.APIs.UserAPIs.registration_api.query_database")
@patch("Source.APIs.UserAPIs.registration_api.encrypt_string", return_value="encrypted_pw")
@patch("Source.APIs.UserAPIs.registration_api.validate_user_not_in_db", return_value=True)
def test_register_new_user_success(mock_validate_user, mock_encrypt, mock_query):
    mock_query.return_value = (MagicMock(), MagicMock())
    result = register_new_user("user", "ValidPass123", "ValidPass123", True)
    assert result == GenericReturnCodes.SUCCESS


@patch("Source.APIs.UserAPIs.registration_api.query_database", side_effect=Exception("DB Error"))
@patch("Source.APIs.UserAPIs.registration_api.encrypt_string", return_value="encrypted_pw")
@patch("Source.APIs.UserAPIs.registration_api.validate_user_not_in_db", return_value=True)
@patch("Source.APIs.UserAPIs.registration_api.logger")
def test_register_new_user_db_error(mock_logger, mock_validate_user, mock_encrypt, mock_query):
    result = register_new_user("user", "ValidPass123", "ValidPass123", False)
    assert result == GenericReturnCodes.ERROR
    mock_logger.error.assert_called_once()
