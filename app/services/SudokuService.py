from functools import lru_cache

from app.repositories.SudokuRepository import get_sudoku_repository, SudokuRepository
from app.dependencies.database import database
from app.libs.sudoku_grid import SudokuGrid

class SudokuService:
  def __init__(self, sudoku_repository: SudokuRepository):
    self.__sudoku_repository = sudoku_repository

  def get_random_sudoku_by_difficulty(self, difficulty: int):
    return self.__sudoku_repository.get_random_sudoku_by_difficulty(difficulty)

  def get_sudoku_by_id(self, sudoku_id: str):
    return self.__sudoku_repository.get_sudoku_by_id(sudoku_id)

  def populate_sudoku_registry(self, difficulty: int, count: int):
    while count > 0:
      # create sudoku and save it to the database
      grid = SudokuGrid.generate_unique_puzzle()
      solution = grid.try_solve()

      if solution is None:
        print(".try_solve returned None, ignoring...")
        print("This might indicate some problems with the sudoku board generation or solving algorithms")
        print(grid)
        print(f"Linear notation: '{grid.linear_notation}'")
        continue

      required_assumptions = grid.try_solve_classify(solution.array)

      if required_assumptions < 0:
        print("Got difficulty score < 0, ignoring...")
        print("This might indicate some problems with the sudoku board classification algorithms")
        print(grid)
        print(f"Linear notation: '{grid.linear_notation}'")
        continue

      if difficulty == 0 and not 0 <= required_assumptions < 3 or \
         difficulty == 1 and not 3 <= required_assumptions < 6 or \
         difficulty == 2 and not 6 <= required_assumptions:
        continue

      self.__sudoku_repository.create_sudoku(difficulty, grid.linear_notation)

      count -= 1

  def validate_sudoku(self, puzzle_id: str, solution: str) -> bool:
    try:
      grid = SudokuGrid.from_linear_notation(solution)
      return grid.is_solved()

    except Exception:
      return False


@lru_cache
def get_sudoku_service() -> SudokuService:
  """Returns a cached instance of SudokuService."""
  return SudokuService(get_sudoku_repository(database))
