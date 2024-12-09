from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, UniqueConstraint
from app.core.database import Base
from datetime import datetime

class PuzzleRegistry(Base):
  __tablename__ = "sudoku_registry"

  id = Column(Integer, primary_key=True, index=True) 
  puzzle_id = Column(Integer)
  user_id = Column(Integer)
  time_taken = Column(float, nullable=False) 
  is_valid_for_leaderboard = Column(bool, default=True)
  created_at = Column(datetime, default=datetime.now())

  __table_args__ = (
    UniqueConstraint('puzzle_id', 'user_id'),
  )