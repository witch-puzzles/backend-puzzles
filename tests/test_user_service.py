import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.UserService import UserService
from app.repositories.UserRepository import UserRepository
from app.schemes.User import UserCreateResponse, UserUpdateResponse
from app.entities.User import User


@pytest.fixture
def mock_repository():
    """Fixture to create a mocked UserRepository with async support."""
    mock_repo = MagicMock(spec=UserRepository)
    mock_repo.save_user = AsyncMock()  # Mock async save_user method
    return mock_repo


def test_get_user_by_firebase_id(mock_repository):
    # Arrange
    firebase_id = "firebase-id"
    mock_user = MagicMock(spec=User)
    mock_user.firebase_id = firebase_id
    mock_repository.get_user_by_firebase_id.return_value = mock_user

    service = UserService(mock_repository)

    # Act
    user = service.getUserByFirebaseId(firebase_id)

    # Assert
    assert user.firebase_id == firebase_id
    mock_repository.get_user_by_firebase_id.assert_called_once_with(firebase_id)


def test_get_user_by_firebase_id_not_found(mock_repository):
    # Arrange
    firebase_id = "firebase-id"
    mock_repository.get_user_by_firebase_id.return_value = None
    service = UserService(mock_repository)

    # Act & Assert
    with pytest.raises(Exception, match="User not found"):
        service.getUserByFirebaseId(firebase_id)


@pytest.mark.asyncio
async def test_create_user(mock_repository):
    # Arrange
    firebase_id = "firebase-id"
    username = "testuser"
    email = "test@example.com"
    
    mock_repository.get_user_by_firebase_id.return_value = None  # User doesn't exist
    mock_repository.create_user.return_value = None  # Mocking the user creation

    service = UserService(mock_repository)

    # Act
    response = await service.createUser(firebase_id, username, email)

    # Assert
    assert isinstance(response, UserCreateResponse)
    assert response.message == "User created successfully"
    mock_repository.create_user.assert_called_once_with(firebase_id, username, email)


@pytest.mark.asyncio
async def test_update_user(mock_repository):
    # Arrange
    firebase_id = "firebase-id"
    username = "newusername"
    
    mock_user = MagicMock(spec=User)
    mock_user.firebase_id = firebase_id
    mock_repository.get_user_by_firebase_id.return_value = mock_user
    mock_repository.is_username_taken.return_value = False  # Username is not taken

    service = UserService(mock_repository)

    # Act
    response = await service.updateUser(firebase_id, username)

    # Assert
    assert isinstance(response, UserUpdateResponse)
    assert response.message == "User updated successfully"
    assert mock_user.username == username
    mock_repository.save_user.assert_awaited_once_with(mock_user)


@pytest.mark.asyncio
async def test_update_user_username_empty(mock_repository):
    # Arrange
    firebase_id = "firebase-id"
    username = ""

    mock_user = MagicMock(spec=User)
    mock_user.firebase_id = firebase_id
    mock_repository.get_user_by_firebase_id.return_value = mock_user

    service = UserService(mock_repository)

    # Act & Assert
    with pytest.raises(Exception, match="Username cannot be empty"):
        await service.updateUser(firebase_id, username)


@pytest.mark.asyncio
async def test_update_user_username_taken(mock_repository):
    # Arrange
    firebase_id = "firebase-id"
    username = "takenusername"

    mock_user = MagicMock(spec=User)
    mock_user.firebase_id = firebase_id
    mock_repository.get_user_by_firebase_id.return_value = mock_user
    mock_repository.is_username_taken.return_value = True  # Username is taken

    service = UserService(mock_repository)

    # Act & Assert
    with pytest.raises(Exception, match="Username is already taken"):
        await service.updateUser(firebase_id, username)


def test_am_i_admin(mock_repository):
    # Arrange
    firebase_user_id = "firebase-id"
    mock_user = MagicMock(spec=User)
    mock_user.firebase_id = firebase_user_id
    mock_user.role = 1  # Admin role
    mock_repository.get_user_by_firebase_id.return_value = mock_user

    service = UserService(mock_repository)

    # Act
    is_admin = service.am_i_admin(firebase_user_id)

    # Assert
    assert is_admin is True
    mock_repository.get_user_by_firebase_id.assert_called_once_with(firebase_user_id)


def test_am_i_admin_not_admin(mock_repository):
    # Arrange
    firebase_user_id = "firebase-id"
    mock_user = MagicMock(spec=User)
    mock_user.firebase_id = firebase_user_id
    mock_user.role = 0  # Non-admin role
    mock_repository.get_user_by_firebase_id.return_value = mock_user

    service = UserService(mock_repository)

    # Act
    is_admin = service.am_i_admin(firebase_user_id)

    # Assert
    assert is_admin is False
    mock_repository.get_user_by_firebase_id.assert_called_once_with(firebase_user_id)