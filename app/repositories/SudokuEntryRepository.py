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

  def create_sudoku_entry(self, user_id: str, sudoku_id: str, entry: str) -> SudokuRegistry:
    sudoku_entry = SudokuRegistry(user_id=user_id, sudoku_id=sudoku_id, entry=entry)
    self.db.add(sudoku_entry)
    self.db.commit()
    self.db.refresh(sudoku_entry)
    return sudoku_entry

  def save_sudoku_entry(self, sudoku_entry: SudokuRegistry) -> SudokuRegistry:
    self.db.add(sudoku_entry)
    self.db.commit()
    self.db.refresh(sudoku_entry)
    return sudoku_entry

  def get_sudoku_entry_by_id(self, sudoku_entry_id: str) -> Optional[SudokuRegistry]:
    return self.db.query(SudokuRegistry).filter(SudokuRegistry.id == sudoku_entry_id).first()

  def get_sudoku_entries_by_user_id(self, user_id: str) -> List[SudokuRegistry]:
    return self.db.query(SudokuRegistry).filter(SudokuRegistry.user_id == user_id).all()

  def get_sudoku_entries_by_sudoku_id(self, sudoku_id: str) -> List[SudokuRegistry]:
    return self.db.query(SudokuRegistry).filter(SudokuRegistry.sudoku_id == sudoku_id).all()

  def delete_sudoku_entry(self, sudoku_entry: SudokuRegistry) -> None:
    self.db.delete(sudoku_entry)
    self.db.commit()
