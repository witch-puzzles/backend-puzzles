import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.repositories.SudokuRepository import SudokuRepository
from app.entities.Sudoku import Sudoku

@pytest.fixture
def mock_db():
    db = MagicMock()
    return db

@pytest.fixture
def sudoku_repository(mock_db):
    return SudokuRepository(db=mock_db)

def test_create_sudoku(sudoku_repository, mock_db):
    # Arrange
    difficulty = 3
    puzzle_data = "easy_sudoku_puzzle"

    # Mock the add, commit, and refresh methods
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    # Act
    sudoku = sudoku_repository.create_sudoku(difficulty, puzzle_data)

    # Assert
    assert sudoku.difficulty == difficulty
    assert sudoku.puzzle_data == puzzle_data
    mock_db.add.assert_called_once_with(sudoku)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sudoku)

def test_save_sudoku(sudoku_repository, mock_db):
    # Arrange
    sudoku = Sudoku(difficulty=3, puzzle_data="easy_sudoku_puzzle")

    # Mock the add, commit, and refresh methods
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    # Act
    saved_sudoku = sudoku_repository.save_sudoku(sudoku)

    # Assert
    assert saved_sudoku == sudoku
    mock_db.add.assert_called_once_with(sudoku)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sudoku)

def test_get_sudoku_by_id(sudoku_repository, mock_db):
    # Arrange
    sudoku_id = uuid4()
    sudoku = Sudoku(id=sudoku_id, difficulty=3, puzzle_data="easy_sudoku_puzzle")

    # Mock the database query result
    mock_db.query.return_value.filter.return_value.first.return_value = sudoku

    # Act
    fetched_sudoku = sudoku_repository.get_sudoku_by_id(sudoku_id)

    # Assert
    assert fetched_sudoku == sudoku
    mock_db.query.return_value.filter.return_value.first.assert_called_once()

def test_get_random_sudoku_by_difficulty(sudoku_repository, mock_db):
    # Arrange
    difficulty = 3
    sudoku = Sudoku(id=uuid4(), difficulty=difficulty, puzzle_data="easy_sudoku_puzzle")

    # Mock the database query result
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = sudoku

    # Act
    fetched_sudoku = sudoku_repository.get_random_sudoku_by_difficulty(difficulty)

    # Assert
    assert fetched_sudoku == sudoku
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.assert_called_once()

def test_delete_sudoku(sudoku_repository, mock_db):
    # Arrange
    sudoku = Sudoku(id=uuid4(), difficulty=3, puzzle_data="easy_sudoku_puzzle")

    # Mock the delete and commit methods
    mock_db.delete = MagicMock()
    mock_db.commit = MagicMock()

    # Act
    sudoku_repository.delete_sudoku(sudoku)

    # Assert
    mock_db.delete.assert_called_once_with(sudoku)
    mock_db.commit.assert_called_once()
