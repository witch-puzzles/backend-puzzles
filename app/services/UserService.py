from functools import lru_cache

from app.repositories.UserRepository import get_user_repository, UserRepository
from app.dependencies.database import database
from app.schemes.User import UserCreateResponse, UserUpdateResponse


class UserService:
  def __init__(self, user_repository: UserRepository):
    self.__user_repository = user_repository

  async def createUser(self, firebase_id: str, username: str, email: str) -> UserCreateResponse:
    user = self.__user_repository.get_user_by_firebase_id(firebase_id)

    if not user:
      self.__user_repository.create_user(firebase_id, username, email)

    return UserCreateResponse(message='User created successfully')

  async def updateUser(self, requesterFirebaseAuthId: str, username: str) -> UserCreateResponse:
    user = self.__user_repository.get_user_by_firebase_id(requesterFirebaseAuthId)

    if not user:
      raise Exception('User not found')

    if username.strip() == '':
      raise Exception('Username cannot be empty')

    user.username = username
    await self.__user_repository.save_user(user)

    return UserUpdateResponse(message='User updated successfully')

@lru_cache
def get_user_service() -> UserService:
  """Returns a cached instance of UserService."""
  return UserService(get_user_repository(database))
