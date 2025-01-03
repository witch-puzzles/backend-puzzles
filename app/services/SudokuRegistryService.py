from functools import lru_cache
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID
import os

from app.repositories.SudokuRegistryRepository import get_sudoku_registry_repository, SudokuRegistryRepository
from app.repositories.UserRepository import get_user_repository, UserRepository

from app.dependencies.database import database
from app.dependencies.sudoku_service import sudoku_service
from app.schemes.SudokuLeaderboard import SudokuLeaderboardResponse, SudokuLeaderboardElement, SubmitSudokuResponse
from app.utils.EmailUtil import EmailUtil
from app.core.settings import settings


class SudokuRegistryService:
  def __init__(self, sudoku_registry_repository: SudokuRegistryRepository, user_repository: UserRepository, sudoku_service: sudoku_service):
    self.__sudoku_registry_repository = sudoku_registry_repository
    self.__user_repository = user_repository
    self.__sudoku_service = sudoku_service

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

  def submit_sudoku(self, firebase_user_id: str, sudoku_id: UUID, solving_time: float, is_applicable: bool, user_solution: str) -> SubmitSudokuResponse:
    user = self.__user_repository.get_user_by_firebase_id(firebase_user_id)
    if not user:
      raise Exception("User not found")
    user_id = user.id
    is_solution_correct = self.__sudoku_service.validate_sudoku(sudoku_id, user_solution)
    if not is_solution_correct:
      return SubmitSudokuResponse(
        is_correct=False,
        message="Solution is incorrect"
      )

    # if is_applicable & registry places in a better place, send email to user which was placed lower
    if is_applicable:
      sudoku = self.__sudoku_service.get_sudoku_by_id(sudoku_id)
      broken_record_user = self.__sudoku_registry_repository.get_broken_record_user_if_any(sudoku.difficulty, user_id, solving_time)

      if broken_record_user:
        email_to_send = broken_record_user.email
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        template_path = os.path.join(parent_dir, "assets/new_record/new_record.html")

        html_content = EmailUtil.read_from_html(template_path)
        EmailUtil.send_email(email_to_send, settings.MAIL_SENDER, "New Record in Leaderboard!", html_content)


    new_registry = self.__sudoku_registry_repository.create_sudoku_registry(user_id, sudoku_id, solving_time, is_applicable)

    return SubmitSudokuResponse(
      is_correct=True,
      message="Solution is correct"
    )


@lru_cache
def get_sudoku_registry_service(database: database, sudoku_service: sudoku_service) -> SudokuRegistryService:
  """Returns a cached instance of SudokuRegistryService."""
  return SudokuRegistryService(
    get_sudoku_registry_repository(database),
    get_user_repository(database),
    sudoku_service,
  )
