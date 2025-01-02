from sqlalchemy import Column, String, DateTime, UniqueConstraint, UUID, Integer
from app.core.database import Base
from datetime import datetime
import uuid

class Sudoku(Base):
  __tablename__ = "sudoku"

  id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
  difficulty = Column(Integer, nullable=False)
  puzzle_data = Column(String, nullable=False)
  created_at = Column(DateTime, default=datetime.now())

  __table_args__ = (
    UniqueConstraint('puzzle_data'),
  )