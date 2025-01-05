import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from app.services.SudokuService import SudokuService
from app.repositories.SudokuRepository import SudokuRepository
from app.libs.sudoku_grid import SudokuGrid


@pytest.fixture
def mock_repository():
    """Fixture to create a mocked SudokuRepository."""
    return MagicMock(spec=SudokuRepository)


@pytest.fixture
def mock_user_service():
    """Fixture to create a mocked UserService."""
    return MagicMock()


def test_populate_sudoku_registry_valid(mock_repository, mock_user_service, mocker):
    # Arrange
    mock_user_service.getUserByFirebaseId.return_value = {"id": "user123", "is_admin": True}
    mock_user_service.am_i_admin.return_value = True

    mock_grid = MagicMock(spec=SudokuGrid)
    mock_grid.try_solve.return_value = MagicMock(array="solved")
    mock_grid.try_solve_classify.return_value = 4  # Difficulty level matches
    mock_grid.linear_notation = "linear_puzzle"

    mocker.patch("app.services.SudokuService.SudokuGrid.generate_unique_puzzle", return_value=mock_grid)

    service = SudokuService(mock_repository, mock_user_service)

    # Act
    service.populate_sudoku_registry(difficulty=1, count=1, firebase_user_id="firebase_user")

    # Assert
    mock_user_service.getUserByFirebaseId.assert_called_once_with("firebase_user")
    mock_user_service.am_i_admin.assert_called_once_with("firebase_user")
    mock_grid.try_solve.assert_called_once()
    mock_grid.try_solve_classify.assert_called_once()
    mock_repository.create_sudoku.assert_called_once_with(1, "linear_puzzle")


def test_populate_sudoku_registry_user_not_found(mock_repository, mock_user_service):
    # Arrange
    mock_user_service.getUserByFirebaseId.return_value = None
    service = SudokuService(mock_repository, mock_user_service)

    # Act & Assert
    with pytest.raises(Exception, match="User not found"):
        service.populate_sudoku_registry(difficulty=1, count=1, firebase_user_id="firebase_user")


def test_populate_sudoku_registry_access_denied(mock_repository, mock_user_service):
    # Arrange
    mock_user_service.getUserByFirebaseId.return_value = {"id": "user123", "is_admin": False}
    mock_user_service.am_i_admin.return_value = False
    service = SudokuService(mock_repository, mock_user_service)

    # Act & Assert
    with pytest.raises(Exception, match="Access denied"):
        service.populate_sudoku_registry(difficulty=1, count=1, firebase_user_id="firebase_user")


def test_validate_sudoku_with_valid_solution(mock_repository, mocker):
    # Arrange
    mock_grid = MagicMock(spec=SudokuGrid)
    mock_grid.is_solved.return_value = True

    mocker.patch("app.services.SudokuService.SudokuGrid.from_linear_notation", return_value=mock_grid)
    service = SudokuService(mock_repository, MagicMock())

    # Act
    result = service.validate_sudoku("puzzle_id", "valid_solution")

    # Assert
    assert result is True
    mock_grid.is_solved.assert_called_once()


def test_validate_sudoku_with_invalid_solution(mock_repository, mocker):
    # Arrange
    mock_grid = MagicMock(spec=SudokuGrid)
    mock_grid.is_solved.return_value = False

    mocker.patch("app.services.SudokuService.SudokuGrid.from_linear_notation", return_value=mock_grid)
    service = SudokuService(mock_repository, MagicMock())

    # Act
    result = service.validate_sudoku("puzzle_id", "invalid_solution")

    # Assert
    assert result is False
    mock_grid.is_solved.assert_called_once()


def test_validate_sudoku_with_exception(mock_repository, mocker):
    # Arrange
    mocker.patch("app.services.SudokuService.SudokuGrid.from_linear_notation", side_effect=Exception)
    service = SudokuService(mock_repository, MagicMock())

    # Act
    result = service.validate_sudoku("puzzle_id", "invalid_solution")

    # Assert
    assert result is False


def test_get_random_sudoku_by_difficulty(mock_repository, mock_user_service):
    # Arrange
    mock_repository.get_random_sudoku_by_difficulty.return_value = {"id": "sudoku123", "difficulty": 2}
    service = SudokuService(mock_repository, mock_user_service)

    # Act
    result = service.get_random_sudoku_by_difficulty(2)

    # Assert
    mock_repository.get_random_sudoku_by_difficulty.assert_called_once_with(2)
    assert result == {"id": "sudoku123", "difficulty": 2}


def test_get_sudoku_by_id(mock_repository, mock_user_service):
    # Arrange
    sudoku_id = uuid4()
    mock_repository.get_sudoku_by_id.return_value = {"id": str(sudoku_id), "puzzle": "puzzle_data"}
    service = SudokuService(mock_repository, mock_user_service)

    # Act
    result = service.get_sudoku_by_id(sudoku_id)

    # Assert
    mock_repository.get_sudoku_by_id.assert_called_once_with(sudoku_id)
    assert result == {"id": str(sudoku_id), "puzzle": "puzzle_data"}
