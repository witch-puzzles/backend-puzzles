from functools import lru_cache

from app.entities.User import User

from app.repositories.UserRepository import get_user_repository, UserRepository
from app.dependencies.database import database
from app.schemes.User import UserCreateResponse, UserUpdateResponse


class UserService:
  def __init__(self, user_repository: UserRepository):
    self.__user_repository = user_repository

  def getUserByFirebaseId(self, firebase_id: str) -> User:
    user = self.__user_repository.get_user_by_firebase_id(firebase_id)

    if not user:
      raise Exception('User not found')

    return user

  async def createUser(self, firebase_id: str, username: str, email: str) -> UserCreateResponse:
    user = self.__user_repository.get_user_by_firebase_id(firebase_id)

    if not user:
      self.__user_repository.create_user(firebase_id, username, email)

    return UserCreateResponse(message='User created successfully')

  async def updateUser(self, requesterFirebaseAuthId: str, username: str) -> UserCreateResponse:
    user = self.getUserByFirebaseId(requesterFirebaseAuthId)

    if username.strip() == '':
      raise Exception('Username cannot be empty')

    if self.__user_repository.is_username_taken(username):
      raise Exception('Username is already taken')

    user.username = username
    await self.__user_repository.save_user(user)

    return UserUpdateResponse(message='User updated successfully')

  def am_i_admin(self, firebase_user_id: str) -> bool:
    user = self.__user_repository.get_user_by_firebase_id(firebase_user_id)

    return user.role == 1

@lru_cache
def get_user_service() -> UserService:
  """Returns a cached instance of UserService."""
  return UserService(get_user_repository(database))
