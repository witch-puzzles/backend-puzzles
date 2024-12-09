from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, UniqueConstraint
from app.core.database import Base
from datetime import datetime

class User(Base):
  __tablename__ = "user"

  uid = Column(Integer, primary_key=True, index=True)
  user_name = Column(Text, nullable=False)
  email = Column(Text, nullable=False, unique=True)
  created_at = Column(TIMESTAMP, default=datetime.now())
