from functools import lru_cache

from app.repositories.SudokuRepository import get_sudoku_repository, SudokuRepository
from app.dependencies.database import database


class SudokuService:
  def __init__(self, sudoku_repository: SudokuRepository):
    self.__sudoku_repository = sudoku_repository

  def get_random_sudoku_by_difficulty(self, difficulty: int):
    return self.__sudoku_repository.get_random_sudoku_by_difficulty(difficulty)

  def get_sudoku_by_id(self, sudoku_id: str):
    return self.__sudoku_repository.get_sudoku_by_id(sudoku_id)

  def populate_sudoku_registry(self, difficulty: int, count: int):
    for _ in range(count):
      # create sudoku and save it to the database
      pass

  def validate_sudoku(self, puzzle_id: str, solution: str) -> bool:
    return True


@lru_cache
def get_sudoku_service() -> SudokuService:
  """Returns a cached instance of SudokuService."""
  return SudokuService(get_sudoku_repository(database))
