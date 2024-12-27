from fastapi import APIRouter, HTTPException, status, Request
import traceback

from schemes.UserCreate import UserCreateResponse
from dependencies.user_service import user_service

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
    user_service: user_service
) -> UserCreateResponse:
    try:
        return await user_service.createUser(
            requesterFirebaseAuthId=request.state.firebase_user_id
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
