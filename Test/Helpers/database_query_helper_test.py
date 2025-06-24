from unittest.mock import patch, MagicMock
import os
from Source.Constants.constants import DATABASE_FILE_NAME
import Source.Helpers.database_query_helper as db_helper

def get_expected_path():
    base_dir = os.path.dirname(os.path.abspath(db_helper.__file__))
    return os.path.join(base_dir, "../..", "Databases", DATABASE_FILE_NAME)

@patch("sqlite3.connect")
def test_query_database_no_params(mock_connect):
    mock_con = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_con
    mock_con.cursor.return_value = mock_cur

    sql = "SELECT * FROM test_table"
    result, con = db_helper.query_database(sql)

    expected_path = get_expected_path()
    mock_connect.assert_called_once_with(expected_path)
    mock_con.execute.assert_called_once_with("PRAGMA foreign_keys = ON")
    mock_con.cursor.assert_called_once()
    mock_cur.execute.assert_called_once_with(sql)
    mock_con.commit.assert_called_once()
    assert result is not None
    assert con == mock_con

@patch("sqlite3.connect")
def test_query_database_with_params(mock_connect):
    mock_con = MagicMock()
    mock_cur = MagicMock()
    mock_connect.return_value = mock_con
    mock_con.cursor.return_value = mock_cur

    sql = "SELECT * FROM test_table WHERE id = ?"
    params = (1,)
    result, con = db_helper.query_database(sql, params=params)

    expected_path = get_expected_path()
    mock_connect.assert_called_once_with(expected_path)
    mock_con.execute.assert_called_once_with("PRAGMA foreign_keys = ON")
    mock_con.cursor.assert_called_once()
    mock_cur.execute.assert_called_once_with(sql, params)
    mock_con.commit.assert_called_once()
    assert result is not None
    assert con == mock_con
