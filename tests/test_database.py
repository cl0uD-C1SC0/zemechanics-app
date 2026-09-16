from unittest.mock import patch, MagicMock
from app.database import get_db

@patch("app.database.SessionLocal")
def test_get_db_yield_and_close(mock_session_local):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    generator = get_db()

    db = next(generator) 

    assert db == mock_db
    mock_session_local.assert_called_once()

    try:
        next(generator)
    except StopIteration:
        pass

    mock_db.close.assert_called_once()

@patch("app.database.SessionLocal")
def test_get_db_close_on_exception(mock_session_local):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    generator = get_db()
    db = next(generator)

    assert db == mock_db

    generator.close()

    mock_db.close.assert_called_once()

