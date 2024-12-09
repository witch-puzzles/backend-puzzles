from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, UniqueConstraint
from app.core.database import Base
from datetime import datetime

class SudokuPuzzle(Base):
  __tablename__ = "sudoku"

  id = Column(Integer, primary_key=True, index=True)
  difficulty = Column(Integer, nullable=False)
  puzzle_data = Column(Text, nullable=False)
  created_at = Column(datetime, default=datetime.now())

  __table_args__ = (
    UniqueConstraint('puzzle_data', 'difficulty'),
  )