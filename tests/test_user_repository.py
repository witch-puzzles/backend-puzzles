import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.repositories.UserRepository import UserRepository
from app.entities.User import User

@pytest.fixture
def mock_db():
    db = MagicMock()
    return db

@pytest.fixture
def user_repository(mock_db):
    return UserRepository(db=mock_db)

def test_create_user(user_repository, mock_db):
    # Arrange
    firebase_id = "test_firebase_id"
    username = "test_username"
    email = "test@example.com"

    # Mock the add, commit, and refresh methods
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    # Act
    user = user_repository.create_user(firebase_id, username, email)

    # Assert
    assert user.firebase_id == firebase_id
    assert user.username == username
    assert user.email == email
    mock_db.add.assert_called_once_with(user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(user)

def test_save_user(user_repository, mock_db):
    # Arrange
    user = User(firebase_id="firebase_id", username="username", email="email@example.com")
    
    # Mock the add, commit, and refresh methods
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    # Act
    saved_user = user_repository.save_user(user)

    # Assert
    assert saved_user == user
    mock_db.add.assert_called_once_with(user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(user)

def test_get_user_by_id(user_repository, mock_db):
    # Arrange
    user_id = uuid4()
    user = User(id=user_id, firebase_id="firebase_id", username="username", email="email@example.com")
    
    # Mock the database query result
    mock_db.query.return_value.filter.return_value.first.return_value = user

    # Act
    fetched_user = user_repository.get_user_by_id(user_id)

    # Assert
    assert fetched_user == user
    mock_db.query.return_value.filter.return_value.first.assert_called_once()

def test_get_user_by_firebase_id(user_repository, mock_db):
    # Arrange
    firebase_id = "firebase_id"
    user = User(id=uuid4(), firebase_id=firebase_id, username="username", email="email@example.com")
    
    # Mock the database query result
    mock_db.query.return_value.filter.return_value.first.return_value = user

    # Act
    fetched_user = user_repository.get_user_by_firebase_id(firebase_id)

    # Assert
    assert fetched_user == user
    mock_db.query.return_value.filter.return_value.first.assert_called_once()

def test_delete_user(user_repository, mock_db):
    # Arrange
    user = User(id=uuid4(), firebase_id="firebase_id", username="username", email="email@example.com")
    
    # Mock the delete and commit methods
    mock_db.delete = MagicMock()
    mock_db.commit = MagicMock()

    # Act
    user_repository.delete_user(user)

    # Assert
    mock_db.delete.assert_called_once_with(user)
    mock_db.commit.assert_called_once()

def test_is_username_taken(user_repository, mock_db):
    # Arrange
    username = "existing_user"
    
    # Mock the query to return an existing user
    mock_db.query.return_value.filter.return_value.first.return_value = User(id=uuid4(), firebase_id="firebase_id", username=username, email="email@example.com")
    
    # Act
    result = user_repository.is_username_taken(username)

    # Assert
    assert result is True
    mock_db.query.return_value.filter.return_value.first.assert_called_once()
    
    # Test with a non-existing username
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = user_repository.is_username_taken("non_existing_user")
    assert result is False
