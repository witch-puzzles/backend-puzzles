"""
SudokuEntriesRepository.py is a class that contains all the methods that are used to interact with the database, for the SudokuEntries table.
"""

from sqlalchemy.orm import Session
from typing import Optional, List

from app.entities.User import User
from app.entities.Sudoku import Sudoku
from app.entities.SudokuRegistry import SudokuRegistry

class SudokuRegistryRepository:
  def __init__(self, db: Session):
    self.db = db

  def create_sudoku_entry(self, user_id: str, sudoku_id: str, solving_time: float, is_applicable: bool) -> SudokuRegistry:
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

  def get_sudoku_registry_by_id(self, sudoku_registry_id: str) -> Optional[SudokuRegistry]:
    return self.db.query(SudokuRegistry).filter(SudokuRegistry.id == sudoku_registry_id).first()

  def get_sudoku_registries_by_user_id(self, user_id: str) -> List[SudokuRegistry]:
    return self.db.query(SudokuRegistry).filter(SudokuRegistry.user_id == user_id).all()

  def get_sudoku_registries_by_sudoku_id(self, sudoku_id: str) -> List[SudokuRegistry]:
    return self.db.query(SudokuRegistry).filter(SudokuRegistry.sudoku_id == sudoku_id).all()

  def delete_sudoku_registry(self, sudoku_registry: SudokuRegistry) -> None:
    self.db.delete(sudoku_registry)
    self.db.commit()

def get_sudoku_registry_repository(db: Session) -> SudokuRegistryRepository:
  return SudokuRegistryRepository(db)
