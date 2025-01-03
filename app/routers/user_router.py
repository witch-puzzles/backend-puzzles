from fastapi import APIRouter, HTTPException, status, Request
import traceback

from app.schemes.User import (
  UserCreateRequest,
  UserCreateResponse,
  UserUpdateRequest,
  UserUpdateResponse,
)
from app.dependencies.user_service import user_service

router = APIRouter(
  prefix="/v1/user",
  tags=["user"],
  responses={404: {"description": "Not found"}},
)

@router.post(
  "/create",
  response_model=UserCreateResponse,
)
async def createUser(
  request: Request,
  user_create_request: UserCreateRequest,
  user_service: user_service
) -> UserCreateResponse:
  try:
    firebase_user_id = request.state.firebase_user_id
    username = user_create_request.username
    email = user_create_request.email
    return await user_service.createUser(
      firebase_user_id,
      username,
      email,
    )
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
  "/update",
  response_model=UserUpdateResponse,
)
async def updateUser(
  request: Request,
  user_update_request: UserUpdateRequest,
  user_service: user_service
) -> UserUpdateResponse:
  try:
    firebase_user_id = request.state.firebase_user_id
    username = user_update_request.username
    return await user_service.updateUser(
      firebase_user_id,
      username,
    )
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get(
  "/amiadmin"
)
async def am_i_admin(
  request: Request,
  user_service: user_service
):
  try:
    firebase_user_id = request.state.firebase_user_id
    return user_service.am_i_admin(firebase_user_id)
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))