from unittest.mock import patch, MagicMock
import pytest
from Source.Helpers.get_review_by_id_helper import get_review_by_id
from Source.Models.review import Review

@patch("Source.Helpers.get_review_by_id_helper.query_database")
def test_get_review_by_id_returns_review(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (
        "rev123", "Great product", "Loved it", 5, "user1", "prod123"
    )
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    review = get_review_by_id("rev123")

    mock_connection.close.assert_called_once()
    assert isinstance(review, Review)
    assert review.review_id == "rev123"
    assert review.review_title == "Great product"
    assert review.review_body == "Loved it"
    assert review.review_score == 5
    assert review.username == "user1"
    assert review.product_id == "prod123"

@patch("Source.Helpers.get_review_by_id_helper.query_database")
def test_get_review_by_id_returns_none_if_not_found(mock_query_database):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_connection = MagicMock()
    mock_query_database.return_value = (mock_cursor, mock_connection)

    review = get_review_by_id("rev999")

    mock_connection.close.assert_called_once()
    assert review is None
