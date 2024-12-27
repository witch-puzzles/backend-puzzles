from functools import lru_cache

from repositories.UserRepository import get_user_repository, UserRepository
from dependencies.database import database
from schemes.UserCreate import UserCreateResponse


class UserService:
  def __init__(self, user_repository: UserRepository):
    self.__user_repository = user_repository

  async def createUser(self, requesterFirebaseAuthId: str) -> UserCreateResponse:
    user = self.__user_repository.get_user_by_firebase_id(requesterFirebaseAuthId)

    if not user:
      await self.__user_repository.create_user(requesterFirebaseAuthId)

    return UserCreateResponse(message='User created or updated successfully')


@lru_cache
def get_user_service() -> UserService:
  """Returns a cached instance of UserService."""
  return UserService(get_user_repository(database))
