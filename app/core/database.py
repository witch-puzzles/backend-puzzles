from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.settings import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(SessionFactory)

Base = declarative_base()

def get_database():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()