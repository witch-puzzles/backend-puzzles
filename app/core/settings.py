from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
  PROJECT_NAME: str = "Witch Puzzles Backend"
  DESCRIPTION: str = "RestAPI of the Witch Puzzles Platform"
  VERSION: str = "0.0.1"

  DATABASE_URL: str = os.environ.get("DATABASE_URL")
  DEVELOPMENT: bool = os.environ.get("DEVELOPMENT", 0) == 1
  LOCK_DB_WRITE: bool = os.environ.get("LOCK_DB_WRITE", 0) == 1
  PORT: int = os.environ.get("PORT", 4040)

  FIREBASE_AUTH_CREDENTIAL_PATH: str = os.environ.get("FIREBASE_AUTH_CREDENTIAL_PATH")

settings = Settings()
