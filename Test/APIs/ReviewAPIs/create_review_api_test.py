from unittest.mock import patch
from Source.APIs.ReviewAPIs.create_review_api import create_review
from Source.Constants.constants import REVIEW_TABLE_NAME
from Source.Enums.generic_return_codes import GenericReturnCodes


@patch("Source.APIs.ReviewAPIs.create_review_api.query_database")
@patch("Source.APIs.ReviewAPIs.create_review_api.does_id_exist_in_table")
@patch("Source.APIs.ReviewAPIs.create_review_api.generate_random_id")
def test_generate_random_id_until_unique(mock_generate_id, mock_exists, _):
    mock_generate_id.side_effect = ['id1', 'id2', 'id3']
    mock_exists.side_effect = [True, True, False]

    result = create_review("Title", "Body", 5, "prod1", "user1")

    assert mock_generate_id.call_count == 3
    assert mock_exists.call_count == 3
    assert result == GenericReturnCodes.SUCCESS


@patch("Source.APIs.ReviewAPIs.create_review_api.query_database")
@patch("Source.APIs.ReviewAPIs.create_review_api.does_id_exist_in_table", return_value=False)
@patch("Source.APIs.ReviewAPIs.create_review_api.generate_random_id", return_value="abc123")
def test_query_database_called_with_correct_params(_, __, mock_query):
    create_review("Title", "Body", 5, "prod1", "user1")

    expected_sql = f"""
        INSERT INTO {REVIEW_TABLE_NAME} (
            review_id, product_id, username, review_title, review_body, review_score
        ) VALUES (?, ?, ?, ?, ?, ?)
    """
    mock_query.assert_called_once_with(
        expected_sql,
        params=("abc123", "prod1", "user1", "Title", "Body", 5),
    )


@patch("Source.APIs.ReviewAPIs.create_review_api.query_database", return_value=None)
@patch("Source.APIs.ReviewAPIs.create_review_api.does_id_exist_in_table", return_value=False)
@patch("Source.APIs.ReviewAPIs.create_review_api.generate_random_id", return_value="abc123")
def test_returns_success_on_successful_insert(_, __, ___):
    result = create_review("T", "B", 4, "prod1", "user1")
    assert result == GenericReturnCodes.SUCCESS


@patch("Source.APIs.ReviewAPIs.create_review_api.logger")
@patch("Source.APIs.ReviewAPIs.create_review_api.query_database", side_effect=Exception("DB error"))
@patch("Source.APIs.ReviewAPIs.create_review_api.does_id_exist_in_table", return_value=False)
@patch("Source.APIs.ReviewAPIs.create_review_api.generate_random_id", return_value="abc123")
def test_returns_error_and_logs_on_query_failure(_, __, ___, mock_logger):
    result = create_review("T", "B", 2, "prod1", "user1")

    assert result == GenericReturnCodes.ERROR
    mock_logger.error.assert_called_once()
