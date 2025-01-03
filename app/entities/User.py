from sqlalchemy import Column, Integer, String, UniqueConstraint, UUID, DateTime, Float, Boolean
from app.core.database import Base
from datetime import datetime
import uuid

class User(Base):
  __tablename__ = "users"

  id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
  username = Column(String, nullable=False)
  firebase_id = Column(String, nullable=False)
  email = Column(String, nullable=False)
  username = Column(String, nullable=False)
  role = Column(Integer, nullable=False, default=0)
  created_at = Column(DateTime, default=datetime.now())

  __table_args__ = (
    UniqueConstraint('firebase_id'),
    UniqueConstraint('email'),
    UniqueConstraint('username'),
  )
