"""
UserRepository.py is a class that contains all the methods that are used to interact with the database, for the User table.
"""
from typing import Optional
from uuid import UUID

from app.entities.User import User
from app.dependencies.database import database


class UserRepository:
  def __init__(self, db: database):
    self.db = db

  def create_user(self, firebase_id: str, username: str, email: str) -> User:
    user = User(firebase_id=firebase_id, username=username, email=email)
    self.db.add(user)
    self.db.commit()
    self.db.refresh(user)
    return user

  def save_user(self, user: User) -> User:
    self.db.add(user)
    self.db.commit()
    self.db.refresh(user)
    return user

  def get_user_by_id(self, user_id: UUID) -> Optional[User]:
    return self.db.query(User).filter(User.id == user_id).first()

  def get_user_by_firebase_id(self, firebase_id: str) -> Optional[User]:
    return self.db.query(User).filter(User.firebase_id == firebase_id).first()

  def delete_user(self, user: User) -> None:
    self.db.delete(user)
    self.db.commit()

  def is_username_taken(self, username: str) -> bool:
    return self.db.query(User).filter(User.username == username).first() is not None


def get_user_repository(db: database) -> UserRepository:
  return UserRepository(db)
