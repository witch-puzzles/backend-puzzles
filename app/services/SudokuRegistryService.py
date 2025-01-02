from functools import lru_cache
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from app.repositories.SudokuRegistryRepository import get_sudoku_registry_repository, SudokuRegistryRepository
from app.repositories.UserRepository import get_user_repository, UserRepository

from app.dependencies.database import database
from app.schemes.SudokuLeaderboard import SudokuLeaderboardResponse, SudokuLeaderboardElement


class SudokuRegistryService:
  def __init__(self, sudoku_registry_repository: SudokuRegistryRepository, user_repository: UserRepository):
    self.__sudoku_registry_repository = sudoku_registry_repository
    self.__user_repository = user_repository

  def get_leaderboard_today(self, difficulty: int, firebase_user_id: str) -> SudokuLeaderboardResponse:
    beginning_of_today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return self.get_leaderboard(difficulty, firebase_user_id, beginning_of_today)

  def get_leaderboard_week(self, difficulty: int, firebase_user_id: str) -> SudokuLeaderboardResponse:
    beginning_of_week = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    beginning_of_week = beginning_of_week.replace(day=beginning_of_week.day - beginning_of_week.weekday())
    return self.get_leaderboard(difficulty, firebase_user_id, beginning_of_week)

  def get_leaderboard_month(self, difficulty: int, firebase_user_id: str) -> SudokuLeaderboardResponse:
    beginning_of_month = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    beginning_of_month = beginning_of_month.replace(day=1)
    return self.get_leaderboard(difficulty, firebase_user_id, beginning_of_month)

  def get_leaderboard_all_time(self, difficulty: int, firebase_user_id: str) -> SudokuLeaderboardResponse:
    return self.get_leaderboard(difficulty, firebase_user_id)

  def get_leaderboard(self, difficulty: int, firebase_user_id: str, beginning_time: Optional[datetime] = None) -> SudokuLeaderboardResponse:
    user = self.__user_repository.get_user_by_firebase_id(firebase_user_id)
    if not user:
      raise Exception("User not found")
    user_id = user.id

    if not beginning_time:
      leaderboard_data = self.__sudoku_registry_repository.get_all_time_leaderboard(difficulty)
    else:
      leaderboard_data = self.__sudoku_registry_repository.get_leaderboard(difficulty, beginning_time)
  
    leaderboard = []
    user_rank = -1
    user_solving_time = -1
    for entry in leaderboard_data:
      if entry.user_id == user_id:
        user_solving_time = entry.solving_time
      leaderboard.append(SudokuLeaderboardElement(
        user_name=entry.user.username,
        rank=user_rank,
        solving_time=entry.solving_time
      ))
      user_rank += 1

    if user_solving_time < 0:
      user_leaderboard_elemet = self.__sudoku_registry_repository.get_user_place_in_leaderboard(user_id, difficulty, beginning_time)
      if user_leaderboard_elemet:
        user_solving_time = user_leaderboard_elemet[0].solving_time
        user_rank = user_leaderboard_elemet[1]

    return SudokuLeaderboardResponse(
      leaderboard=leaderboard,
      user_rank=user_rank,
      user_solving_time=user_solving_time
    )

  def submit_sudoku(self, user_id: UUID, sudoku_id: UUID, solving_time: float, is_applicable: bool) -> None:
    self.__sudoku_registry_repository.create_sudoku_entry(user_id, sudoku_id, solving_time, is_applicable)


@lru_cache
def get_sudoku_registry_service(database: database) -> SudokuRegistryService:
  """Returns a cached instance of SudokuRegistryService."""
  return SudokuRegistryService(
    get_sudoku_registry_repository(database),
    get_user_repository(database),
  )
