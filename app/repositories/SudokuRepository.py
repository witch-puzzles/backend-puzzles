"""
SudokuRepository.py is a class that contains all the methods that are used to interact with the database, for the Sudoku table.
"""

from sqlalchemy.sql.expression import func
from typing import Optional
from uuid import UUID

from app.entities.Sudoku import Sudoku
from app.dependencies.database import database

class SudokuRepository:
  def __init__(self, db: database):
    self.db = db

  def create_sudoku(self, difficulty: int, puzzle_data: str) -> Sudoku:
    sudoku = Sudoku(difficulty=difficulty, puzzle_data=puzzle_data)
    self.db.add(sudoku)
    self.db.commit()
    self.db.refresh(sudoku)
    return sudoku

  def save_sudoku(self, sudoku: Sudoku) -> Sudoku:
    self.db.add(sudoku)
    self.db.commit()
    self.db.refresh(sudoku)
    return sudoku

  def get_sudoku_by_id(self, sudoku_id: UUID) -> Optional[Sudoku]:
    return self.db.query(Sudoku).filter(Sudoku.id == sudoku_id).first()

  def get_random_sudoku_by_difficulty(self, difficulty: int) -> Optional[Sudoku]:
    return self.db.query(Sudoku).filter(Sudoku.difficulty == difficulty).order_by(func.random()).first()

  def delete_sudoku(self, sudoku: Sudoku) -> None:
    self.db.delete(sudoku)
    self.db.commit()


def get_sudoku_repository(db: database) -> SudokuRepository:
  return SudokuRepository(db)
