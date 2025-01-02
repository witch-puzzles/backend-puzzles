import traceback
from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from firebase_admin import auth

class FirebaseAuthMiddleware(BaseHTTPMiddleware):

  def __init__(self, app):
    super().__init__(app)

  async def dispatch(self, request: Request, call_next):
    try:
      request.state.firebase_user_id = None

      authHeader = request.headers.get('Authorization')
      if authHeader is not None:
        firebaseUserId = await self.__getFirebaseAuthUserId(request)
        request.state.firebase_user_id = firebaseUserId

      return await call_next(request)
    
    except Exception as e:
      traceback.print_exc()
      return Exception("Error in FirebaseAuthMiddleware")

  async def __getFirebaseAuthUserId(self, request: Request) -> Optional[str]:
    authHeader = request.headers.get('Authorization')
    token = authHeader.split(" ")[1] if "Bearer" in authHeader else None

    if not token:
      return None

    try:
      decoded_token = auth.verify_id_token(token)
      return decoded_token['uid']
    except Exception as e:
      if 'Token expired' in str(e):
        raise Exception("Firebase token session timeout.")
      else:
        raise Exception("Error decoding Firebase token.")
