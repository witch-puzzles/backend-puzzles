"""
SudokuEntriesRepository.py is a class that contains all the methods that are used to interact with the database, for the SudokuEntries table.
"""

from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime

from app.entities.User import User
from app.entities.Sudoku import Sudoku
from app.entities.SudokuRegistry import SudokuRegistry
from app.dependencies.database import database

from app.schemes.SudokuLeaderboard import UserRecordsElement


class SudokuRegistryRepository:
  def __init__(self, db: database):
    self.db = db

  def create_sudoku_registry(self, user_id: UUID, sudoku_id: UUID, solving_time: float, is_applicable: bool) -> SudokuRegistry:
    sudoku_registry = SudokuRegistry(user_id=user_id, sudoku_id=sudoku_id, solving_time=solving_time, is_applicable=is_applicable)
    self.db.add(sudoku_registry)
    self.db.commit()
    self.db.refresh(sudoku_registry)
    return sudoku_registry

  def save_sudoku_registry(self, sudoku_registry: SudokuRegistry) -> SudokuRegistry:
    self.db.add(sudoku_registry)
    self.db.commit()
    self.db.refresh(sudoku_registry)
    return sudoku_registry

  def get_sudoku_registry_by_id(self, sudoku_registry_id: UUID) -> Optional[SudokuRegistry]:
    return self.db.query(SudokuRegistry).filter(SudokuRegistry.id == sudoku_registry_id).first()

  def get_sudoku_registries_by_user_id(self, user_id: UUID) -> List[SudokuRegistry]:
    return self.db.query(SudokuRegistry).filter(SudokuRegistry.user_id == user_id).all()

  def get_sudoku_registries_by_sudoku_id(self, sudoku_id: UUID) -> List[SudokuRegistry]:
    return self.db.query(SudokuRegistry).filter(SudokuRegistry.sudoku_id == sudoku_id).all()

  def delete_sudoku_registry(self, sudoku_registry: SudokuRegistry) -> None:
    self.db.delete(sudoku_registry)
    self.db.commit()

  def get_leaderboard(self, difficulty: int, last_time: datetime, limit: int = 20) -> List[SudokuRegistry]:
    return self.db.query(SudokuRegistry).join(Sudoku).filter(Sudoku.difficulty == difficulty).filter(SudokuRegistry.created_at > last_time).filter(SudokuRegistry.is_applicable == True).order_by(SudokuRegistry.solving_time).limit(limit).all()

  def get_all_time_leaderboard(self, difficulty: int, limit: int = 20) -> List[SudokuRegistry]:
    return self.db.query(SudokuRegistry).join(Sudoku).filter(Sudoku.difficulty == difficulty).filter(SudokuRegistry.is_applicable == True).order_by(SudokuRegistry.solving_time).limit(limit).all()

  def get_user_place_in_leaderboard(self, user_id: UUID, difficulty: int, last_time: datetime) -> Optional[Tuple[SudokuRegistry, int]]:
    leaderboard = self.db.query(SudokuRegistry).join(Sudoku).filter(Sudoku.difficulty == difficulty).filter(SudokuRegistry.created_at > last_time).filter(SudokuRegistry.is_applicable == True).order_by(SudokuRegistry.solving_time).all()
    user_place = 1
    for entry in leaderboard:
      if entry.user_id == user_id:
        return entry, user_place
      user_place += 1
    return None

  def get_user_place_in_all_time_leaderboard(self, user_id: UUID, difficulty: int) -> Optional[Tuple[SudokuRegistry, int]]:
    leaderboard = self.db.query(SudokuRegistry).join(Sudoku).filter(Sudoku.difficulty == difficulty).filter(SudokuRegistry.is_applicable == True).order_by(SudokuRegistry.solving_time).all()
    user_place = 1
    for entry in leaderboard:
      if entry.user_id == user_id:
        return entry, user_place
      user_place += 1
    return None

  def get_broken_record_user_if_any(self, difficulty: int, user_id: UUID, solving_time: float, limit: int = 20) -> Optional[User]:
    """
    Checks if the given solving time is breaking any records in the leaderboard.
    If so, returns the user who's record is broken.
    Checks only the last `limit` entries.
    Checks if the user is not breaking his own record.
    """
    leaderboard = self.db.query(SudokuRegistry).join(Sudoku).filter(Sudoku.difficulty == difficulty).filter(SudokuRegistry.is_applicable == True).order_by(SudokuRegistry.solving_time).limit(limit).all()
    for entry in leaderboard:
      if entry.solving_time > solving_time and entry.user_id != user_id:
        return entry.user
    return None

  def get_user_records(self, user_id: UUID, difficulty: int, limit: int = 20) -> List[UserRecordsElement]:
    user_records = self.db.query(SudokuRegistry).join(Sudoku).filter(Sudoku.difficulty == difficulty).filter(SudokuRegistry.user_id == user_id).filter(SudokuRegistry.is_applicable == True).order_by(SudokuRegistry.solving_time).limit(limit).all()
    records = []
    for entry in user_records:
      records.append(UserRecordsElement(
        puzzle_id=entry.sudoku_id,
        solving_time=entry.solving_time
      ))
    return records


def get_sudoku_registry_repository(db: database) -> SudokuRegistryRepository:
  return SudokuRegistryRepository(db)
