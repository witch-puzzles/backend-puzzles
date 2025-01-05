import pytest
from unittest.mock import MagicMock
from app.services.SudokuService import SudokuService
from app.repositories.SudokuRepository import SudokuRepository
from app.libs.sudoku_grid import SudokuGrid


@pytest.fixture
def mock_repository():
    """Fixture to create a mocked SudokuRepository using pytest-mock."""
    return MagicMock(spec=SudokuRepository)


def test_get_random_sudoku_by_difficulty(mock_repository, mocker):
    # Arrange
    mock_repository.get_random_sudoku_by_difficulty.return_value = {
        "id": "123", "difficulty": 2, "puzzle": "example"
    }
    service = SudokuService(mock_repository)
    
    # Act
    result = service.get_random_sudoku_by_difficulty(2)
    
    # Assert
    mock_repository.get_random_sudoku_by_difficulty.assert_called_once_with(2)
    assert result == {"id": "123", "difficulty": 2, "puzzle": "example"}


def test_get_sudoku_by_id(mock_repository):
    # Arrange
    mock_repository.get_sudoku_by_id.return_value = {
        "id": "123", "puzzle": "example"
    }
    service = SudokuService(mock_repository)
    
    # Act
    result = service.get_sudoku_by_id("123")
    
    # Assert
    mock_repository.get_sudoku_by_id.assert_called_once_with("123")
    assert result == {"id": "123", "puzzle": "example"}


def test_validate_sudoku_valid_solution(mock_repository, mocker):
    # Arrange
    # Mock the SudokuGrid class
    mock_grid = MagicMock(spec=SudokuGrid)
    mock_grid.is_solved.return_value = True  # Simulate that the puzzle is solved
    
    # Mock the from_linear_notation method to return the mocked grid
    mocker.patch('app.services.SudokuService.SudokuGrid.from_linear_notation', return_value=mock_grid)
    
    service = SudokuService(mock_repository)
    
    # Act
    result = service.validate_sudoku("123", "valid_solution")
    
    # Assert
    assert result is True
    mock_grid.is_solved.assert_called_once()


def test_validate_sudoku_invalid_solution(mock_repository, mocker):
    # Arrange
    # Mock the SudokuGrid class
    mock_grid = MagicMock(spec=SudokuGrid)
    mock_grid.is_solved.return_value = False  # Simulate that the puzzle is not solved
    
    # Mock the from_linear_notation method to return the mocked grid
    mocker.patch('app.services.SudokuService.SudokuGrid.from_linear_notation', return_value=mock_grid)
    
    service = SudokuService(mock_repository)
    
    # Act
    result = service.validate_sudoku("123", "invalid_solution")
    
    # Assert
    assert result is False
    mock_grid.is_solved.assert_called_once()


def test_validate_sudoku_with_exception(mock_repository, mocker):
    # Arrange
    # Mock the from_linear_notation method to raise an exception
    mocker.patch('app.services.SudokuService.SudokuGrid.from_linear_notation', side_effect=Exception)
    
    service = SudokuService(mock_repository)
    
    # Act
    result = service.validate_sudoku("123", "invalid_solution")
    
    # Assert
    assert result is False