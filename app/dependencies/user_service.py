from fastapi import Depends
from typing import Annotated

from services.UserService import get_user_service, UserService


user_service = Annotated[UserService, Depends(get_user_service)]
