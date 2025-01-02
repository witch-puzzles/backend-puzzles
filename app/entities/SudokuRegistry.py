from sqlalchemy import Column, UniqueConstraint, UUID, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.core.database import Base
from datetime import datetime
import uuid

class SudokuRegistry(Base):
  __tablename__ = "sudoku_registry"

  id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
  sudoku_id = Column(UUID, ForeignKey("sudoku.id"), nullable=False)
  user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
  solving_time = Column(Float, nullable=False)
  is_applicable = Column(Boolean, nullable=False)
  created_at = Column(DateTime, default=datetime.now())

  user = relationship("User", foreign_keys=[user_id])
  sudoku = relationship("Sudoku", foreign_keys=[sudoku_id])
