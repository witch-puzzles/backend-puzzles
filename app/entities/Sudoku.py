from sqlalchemy import Column, String, DateTime, UniqueConstraint, UUID
from app.core.database import Base
from datetime import datetime

class Sudoku(Base):
  __tablename__ = "sudoku"

  id = Column(UUID, primary_key=True, index=True)
  difficulty = Column(UUID, nullable=False)
  puzzle_data = Column(String, nullable=False)
  created_at = Column(DateTime, default=datetime.now())

  __table_args__ = (
    UniqueConstraint('puzzle_data', 'difficulty'),
  )