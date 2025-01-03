import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime

from app.repositories.SudokuRegistryRepository import SudokuRegistryRepository
from app.entities.SudokuRegistry import SudokuRegistry
from app.entities.Sudoku import Sudoku
from app.entities.User import User
from app.schemes.SudokuLeaderboard import UserRecordsElement


@pytest.fixture
def mock_db():
    db = MagicMock()
    return db

@pytest.fixture
def sudoku_registry_repository(mock_db):
    return SudokuRegistryRepository(db=mock_db)


def test_create_sudoku_registry(sudoku_registry_repository, mock_db):
    # Arrange
    user_id = uuid4()
    sudoku_id = uuid4()
    solving_time = 120.5
    is_applicable = True

    # Mock the add, commit, and refresh methods
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    # Act
    sudoku_registry = sudoku_registry_repository.create_sudoku_registry(user_id, sudoku_id, solving_time, is_applicable)

    # Assert
    assert sudoku_registry.user_id == user_id
    assert sudoku_registry.sudoku_id == sudoku_id
    assert sudoku_registry.solving_time == solving_time
    assert sudoku_registry.is_applicable == is_applicable
    mock_db.add.assert_called_once_with(sudoku_registry)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sudoku_registry)


def test_save_sudoku_registry(sudoku_registry_repository, mock_db):
    # Arrange
    sudoku_registry = SudokuRegistry(
        id=uuid4(),
        user_id=uuid4(),
        sudoku_id=uuid4(),
        solving_time=100.5,
        is_applicable=True
    )

    # Mock the add, commit, and refresh methods
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    # Act
    saved_sudoku_registry = sudoku_registry_repository.save_sudoku_registry(sudoku_registry)

    # Assert
    assert saved_sudoku_registry == sudoku_registry
    mock_db.add.assert_called_once_with(sudoku_registry)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sudoku_registry)


def test_get_sudoku_registry_by_id(sudoku_registry_repository, mock_db):
    # Arrange
    sudoku_registry_id = uuid4()
    sudoku_registry = SudokuRegistry(
        id=sudoku_registry_id,
        user_id=uuid4(),
        sudoku_id=uuid4(),
        solving_time=100.5,
        is_applicable=True
    )

    # Mock the database query result
    mock_db.query.return_value.filter.return_value.first.return_value = sudoku_registry

    # Act
    fetched_sudoku_registry = sudoku_registry_repository.get_sudoku_registry_by_id(sudoku_registry_id)

    # Assert
    assert fetched_sudoku_registry == sudoku_registry
    mock_db.query.return_value.filter.return_value.first.assert_called_once()


def test_get_sudoku_registries_by_user_id(sudoku_registry_repository, mock_db):
    # Arrange
    user_id = uuid4()
    sudoku_registry = SudokuRegistry(
        user_id=user_id,
        sudoku_id=uuid4(),
        solving_time=100.5,
        is_applicable=True
    )

    # Mock the database query result
    mock_db.query.return_value.filter.return_value.all.return_value = [sudoku_registry]

    # Act
    registries = sudoku_registry_repository.get_sudoku_registries_by_user_id(user_id)

    # Assert
    assert registries == [sudoku_registry]
    mock_db.query.return_value.filter.return_value.all.assert_called_once()


def test_get_leaderboard(sudoku_registry_repository, mock_db):
    # Arrange
    difficulty = 3
    last_time = datetime(2023, 1, 1)
    sudoku_registry = SudokuRegistry(
        user_id=uuid4(),
        sudoku_id=uuid4(),
        solving_time=100.5,
        is_applicable=True,
        created_at=datetime.now()
    )

    # Mock the database query result
    mock_db.query.return_value.join.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = [sudoku_registry]

    # Act
    leaderboard = sudoku_registry_repository.get_leaderboard(difficulty, last_time)

    # Assert
    assert leaderboard == [sudoku_registry]  # Ensure that actual instances match, not MagicMock


def test_get_user_place_in_leaderboard(sudoku_registry_repository, mock_db):
    # Arrange
    user_id = uuid4()
    difficulty = 3
    last_time = datetime(2023, 1, 1)
    sudoku_registry = SudokuRegistry(
        user_id=user_id,
        sudoku_id=uuid4(),
        solving_time=100.5,
        is_applicable=True,
        created_at=datetime.now()
    )

    # Mock the database query result
    mock_db.query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [sudoku_registry]

    # Act
    user_place = sudoku_registry_repository.get_user_place_in_leaderboard(user_id, difficulty, last_time)

    # Assert
    assert user_place is not None  # Ensure the result is not None
    assert user_place[0] == sudoku_registry  # Assuming it returns a tuple of (sudoku_registry, place)
    assert user_place[1] == 1  # Ensure the place is correctly set (e.g., 1st place)


def test_get_user_records(sudoku_registry_repository, mock_db):
    # Arrange
    user_id = uuid4()
    difficulty = 3
    sudoku_registry = SudokuRegistry(
        user_id=user_id,
        sudoku_id=uuid4(),
        solving_time=100.5,
        is_applicable=True
    )

    # Mock the database query result
    mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [sudoku_registry]

    # Act
    user_records = sudoku_registry_repository.get_user_records(user_id, difficulty)

    # Assert
    assert len(user_records) == 1  # Ensure the returned list contains one record
    assert isinstance(user_records[0], SudokuRegistry)  # Ensure the first record is of type SudokuRegistry
    assert user_records[0].user_id == user_id  # Ensure the returned record matches the user_id
