from dataclasses import dataclass
from typing import Optional


@dataclass
class UserCreateRequest:
  username: str
  email: str

@dataclass
class UserCreateResponse:
  message: str

@dataclass
class UserUpdateRequest:
  username: str

@dataclass
class UserUpdateResponse:
  message: str
