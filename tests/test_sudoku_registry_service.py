import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime, timezone
from app.services.SudokuRegistryService import SudokuRegistryService
from app.schemes.SudokuLeaderboard import SudokuLeaderboardResponse, UserRecordsResponse, SubmitSudokuResponse
from app.entities.User import User
from uuid import uuid4


@pytest.fixture
def mock_user_repository():
    """Fixture to mock the UserRepository."""
    mock_repo = MagicMock()
    return mock_repo


@pytest.fixture
def mock_sudoku_registry_repository():
    """Fixture to mock the SudokuRegistryRepository."""
    mock_repo = MagicMock()
    return mock_repo


@pytest.fixture
def mock_sudoku_service():
    """Fixture to mock the sudoku_service."""
    mock_service = MagicMock()
    return mock_service


@pytest.fixture
def sudoku_registry_service(mock_sudoku_registry_repository, mock_user_repository, mock_sudoku_service):
    """Fixture to create the SudokuRegistryService with mocked dependencies."""
    return SudokuRegistryService(
        mock_sudoku_registry_repository,
        mock_user_repository,
        mock_sudoku_service
    )

def test_get_leaderboard_today(sudoku_registry_service, mock_user_repository, mock_sudoku_registry_repository):
    # Arrange
    difficulty = 1
    firebase_user_id = 'firebase-id'

    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user_repository.get_user_by_firebase_id.return_value = mock_user

    mock_leaderboard_data = [
        MagicMock(user_id=1, solving_time=120, user=mock_user),
        MagicMock(user_id=2, solving_time=150, user=MagicMock(username='User2'))
    ]
    mock_sudoku_registry_repository.get_leaderboard.return_value = mock_leaderboard_data

    # Act
    response = sudoku_registry_service.get_leaderboard_today(difficulty, firebase_user_id)

    # Assert
    assert isinstance(response, SudokuLeaderboardResponse)
    assert len(response.leaderboard) == 2
    assert response.user_rank == 1
    assert response.user_solving_time == 120

def test_get_user_records(sudoku_registry_service, mock_user_repository, mock_sudoku_registry_repository):
    # Arrange
    firebase_user_id = 'firebase-id'
    difficulty = 1

    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user_repository.get_user_by_firebase_id.return_value = mock_user

    mock_user_records = [
        MagicMock(sudoku_id=uuid4(), solving_time=120),
        MagicMock(sudoku_id=uuid4(), solving_time=130)
    ]
    mock_sudoku_registry_repository.get_user_records.return_value = mock_user_records

    # Act
    response = sudoku_registry_service.get_user_records(firebase_user_id, difficulty)

    # Assert
    assert isinstance(response, UserRecordsResponse)
    assert len(response.records) == 2
    assert response.records[0].solving_time == 120

def test_submit_sudoku_correct_solution(sudoku_registry_service, mock_user_repository, mock_sudoku_registry_repository, mock_sudoku_service):
    # Arrange
    firebase_user_id = 'firebase-id'
    sudoku_id = uuid4()
    solving_time = 120
    is_applicable = True
    user_solution = "valid_solution"

    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.email = 'user@example.com'
    mock_user_repository.get_user_by_firebase_id.return_value = mock_user

    mock_sudoku_service.validate_sudoku.return_value = True  # Assume the solution is correct
    mock_sudoku_registry_repository.create_sudoku_registry.return_value = MagicMock()

    # Act
    response = sudoku_registry_service.submit_sudoku(firebase_user_id, sudoku_id, solving_time, is_applicable, user_solution)

    # Assert
    assert response.is_correct


def test_submit_sudoku_incorrect_solution(sudoku_registry_service, mock_user_repository, mock_sudoku_registry_repository, mock_sudoku_service):
    # Arrange
    firebase_user_id = 'firebase-id'
    sudoku_id = uuid4()
    solving_time = 120
    is_applicable = True
    user_solution = "invalid_solution"

    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.email = 'user@example.com'
    mock_user_repository.get_user_by_firebase_id.return_value = mock_user

    mock_sudoku_service.validate_sudoku.return_value = False  # Incorrect solution

    # Act
    response = sudoku_registry_service.submit_sudoku(firebase_user_id, sudoku_id, solving_time, is_applicable, user_solution)

    # Assert
    assert not response.is_correct
    assert response.message == "Solution is incorrect"
