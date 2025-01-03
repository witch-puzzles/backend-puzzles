from functools import lru_cache
from uuid import UUID

from app.repositories.SudokuRepository import get_sudoku_repository, SudokuRepository
from app.dependencies.user_service import user_service
from app.dependencies.database import database
from app.libs.sudoku_grid import SudokuGrid
from app.services.UserService import UserService, get_user_service


class SudokuService:
    def __init__(self, sudoku_repository: SudokuRepository, user_service: user_service):
        self.__sudoku_repository = sudoku_repository
        self.__user_service = user_service

    def get_random_sudoku_by_difficulty(self, difficulty: int):
        return self.__sudoku_repository.get_random_sudoku_by_difficulty(difficulty)

    def get_sudoku_by_id(self, sudoku_id: UUID):
        return self.__sudoku_repository.get_sudoku_by_id(sudoku_id)

    def populate_sudoku_registry(
        self, difficulty: int, count: int, firebase_user_id: str
    ):
        print(type(self.__user_service))
        user = self.__user_service.getUserByFirebaseId(firebase_user_id)
        if user is None:
            raise Exception("User not found")
        if self.__user_service.am_i_admin(firebase_user_id) is False:
            raise Exception("Access denied")

        while count > 0:
            # create sudoku and save it to the database
            grid = SudokuGrid.generate_unique_puzzle()
            solution = grid.try_solve()

            if solution is None:
                print(".try_solve returned None, ignoring...")
                print(
                    "This might indicate some problems with the sudoku board generation or solving algorithms"
                )
                print(grid)
                print(f"Linear notation: '{grid.linear_notation}'")
                continue

            required_assumptions = grid.try_solve_classify(solution.array)

            if required_assumptions < 0:
                print("Got difficulty score < 0, ignoring...")
                print(
                    "This might indicate some problems with the sudoku board classification algorithms"
                )
                print(grid)
                print(f"Linear notation: '{grid.linear_notation}'")
                continue

            if (
                difficulty == 0
                and not 0 <= required_assumptions < 3
                or difficulty == 1
                and not 3 <= required_assumptions < 6
                or difficulty == 2
                and not 6 <= required_assumptions
            ):
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
    return SudokuService(get_sudoku_repository(database), get_user_service())
