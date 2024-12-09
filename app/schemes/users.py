from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, UniqueConstraint
from app.core.database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
  __tablename__ = "users"

  id = Column(UUID , primary_key=True, index=True)
  user_name = Column(Text, nullable=False)
  email = Column(Text, nullable=False, unique=True)
  created_at = Column(datetime, default=datetime.now())
