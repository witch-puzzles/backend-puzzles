from sqlalchemy import Column, UniqueConstraint, UUID, DateTime, Float, Boolean
from app.core.database import Base
from datetime import datetime
import uuid

class SudokuRegistry(Base):
  __tablename__ = "sudoku_registry"

  id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
  sudoku_id = Column(UUID, nullable=False)
  user_id = Column(UUID, nullable=False)
  solving_time = Column(Float, nullable=False)
  is_applicable = Column(Boolean, nullable=False)
  created_at = Column(DateTime, default=datetime.now())
