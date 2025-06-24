from unittest.mock import patch, MagicMock
from Source.APIs.ReviewAPIs.delete_review_api import delete_review
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Enums.update_api_return_codes import UpdateAndDeleteReturnCodes


@patch("Source.APIs.ReviewAPIs.delete_review_api.query_database")
@patch("Source.APIs.ReviewAPIs.delete_review_api.check_username_matches", return_value=True)
def test_successful_delete_by_owner(mock_check_match, mock_query):
    mock_con = MagicMock()
    mock_query.return_value = (None, mock_con)

    result = delete_review("review123", "user1", is_admin=False)

    assert result == GenericReturnCodes.SUCCESS
    mock_check_match.assert_called_once_with("Reviews", "review123", "user1")
    mock_query.assert_called_once()
    mock_con.close.assert_called_once()


@patch("Source.APIs.ReviewAPIs.delete_review_api.query_database")
def test_successful_delete_by_admin(mock_query):
    mock_con = MagicMock()
    mock_query.return_value = (None, mock_con)

    result = delete_review("review123", "admin_user", is_admin=True)

    assert result == GenericReturnCodes.SUCCESS
    mock_query.assert_called_once()
    mock_con.close.assert_called_once()


@patch("Source.APIs.ReviewAPIs.delete_review_api.logger")
@patch("Source.APIs.ReviewAPIs.delete_review_api.check_username_matches", return_value=GenericReturnCodes.ERROR)
def test_returns_item_does_not_exist_when_username_check_errors(mock_check_match, mock_logger):
    result = delete_review("review123", "user1", is_admin=False)

    assert result == UpdateAndDeleteReturnCodes.ITEM_DOES_NOT_EXIST
    mock_logger.warning.assert_called_once()


@patch("Source.APIs.ReviewAPIs.delete_review_api.logger")
@patch("Source.APIs.ReviewAPIs.delete_review_api.check_username_matches", return_value=False)
def test_returns_username_does_not_match(mock_check_match, mock_logger):
    result = delete_review("review123", "wrong_user", is_admin=False)

    assert result == UpdateAndDeleteReturnCodes.USERNAME_DOES_NOT_MATCH
    mock_logger.warning.assert_called_once()


@patch("Source.APIs.ReviewAPIs.delete_review_api.logger")
@patch("Source.APIs.ReviewAPIs.delete_review_api.query_database", side_effect=Exception("DB error"))
@patch("Source.APIs.ReviewAPIs.delete_review_api.check_username_matches", return_value=True)
def test_returns_error_on_query_exception(mock_check_match, mock_query, mock_logger):
    result = delete_review("review123", "user1", is_admin=False)

    assert result == GenericReturnCodes.ERROR
    mock_logger.error.assert_called_once()
