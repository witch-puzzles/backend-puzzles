from sqlalchemy import Column, Integer, String, UniqueConstraint, UUID, DateTime, Float, Boolean
from app.core.database import Base
from datetime import datetime

class User(Base):
  __tablename__ = "users"

  id = Column(UUID, primary_key=True, index=True)
  username = Column(String, nullable=False)
  firebase_id = Column(String, nullable=False)
  created_at = Column(DateTime, default=datetime.now())

  __table_args__ = (
    UniqueConstraint('firebase_id'),
    UniqueConstraint('username'),
  )
