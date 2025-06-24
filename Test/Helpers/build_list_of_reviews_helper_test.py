from unittest.mock import patch, MagicMock
from Source.Helpers.build_list_of_reviews_helper import build_list_of_reviews
from Source.Models.review import Review
from Source.Constants.constants import REVIEW_TABLE_NAME

@patch("Source.Helpers.build_list_of_reviews_helper.query_database")
def test_query_database_called_with_correct_query_and_params(mock_query_database):
    product_id = "prod123"
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    build_list_of_reviews(product_id)

    expected_query = f"SELECT review_id, review_title, review_body, review_score, username FROM {REVIEW_TABLE_NAME} WHERE product_id = ?"
    mock_query_database.assert_called_once_with(expected_query, params=(product_id,))


@patch("Source.Helpers.build_list_of_reviews_helper.query_database")
def test_returns_list_of_review_objects(mock_query_database):
    rows = [
        ("r1", "Title 1", "Body 1", 5, "user1"),
        ("r2", "Title 2", "Body 2", 4, "user2")
    ]
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = rows
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = build_list_of_reviews("prod123")

    assert isinstance(result, list)
    assert all(isinstance(r, Review) for r in result)
    assert len(result) == 2
    assert result[0].review_id == "r1"
    assert result[0].review_title == "Title 1"
    assert result[0].review_body == "Body 1"
    assert result[0].review_score == 5
    assert result[0].username == "user1"
    assert result[0].product_id == "prod123"


@patch("Source.Helpers.build_list_of_reviews_helper.query_database")
def test_returns_empty_list_when_no_reviews(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    result = build_list_of_reviews("prod123")

    assert result == []


@patch("Source.Helpers.build_list_of_reviews_helper.query_database")
def test_closes_database_connection(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    build_list_of_reviews("prod123")

    mock_connection.close.assert_called_once()