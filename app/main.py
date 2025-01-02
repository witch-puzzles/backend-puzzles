from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings

from app.middlewares import (
  FirebaseAuthMiddleware,
)

from app.routers import (
  user_router,
  sudoku_router,
  sudoku_registry_router,
)

app = FastAPI()

origins = [
  "http://localhost",
  "http://localhost:8000",
  # TODO: our domain will be added here when we have it
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.add_middleware(FirebaseAuthMiddleware)

app.include_router(user_router)
app.include_router(sudoku_router)
app.include_router(sudoku_registry_router)

@app.get(
  "/",
  summary="Root",
  description="Root endpoint",
  response_description="Beneath this mask, there is more than flesh...",
)
def get_root():
  return "V" # V for Vendetta


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
