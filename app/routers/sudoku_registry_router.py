from fastapi import APIRouter, HTTPException, status, Request
import traceback

from app.schemes.SudokuLeaderboard import (
  SudokuLeaderboardResponse,
  SubmitSudokuRequest,
  SubmitSudokuResponse,
)
from app.entities import Sudoku
from app.dependencies.sudoku_registry_service import sudoku_registry_service


router = APIRouter(
  prefix="/v1/sudoku_registry",
  tags=["sudoku_registry"],
  responses={404: {"description": "Not found"}},
)

@router.get(
  "/leaderboard/{difficulty}/today",
  response_model=SudokuLeaderboardResponse,
)
async def get_leaderboard_today(request: Request, difficulty: int, sudoku_registry_service: sudoku_registry_service):
  try:
    firebase_user_id = request.state.firebase_user_id
    if firebase_user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    return await sudoku_registry_service.get_leaderboard_today(difficulty, firebase_user_id)
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
  "/leaderboard/{difficulty}/week",
  response_model=SudokuLeaderboardResponse,
)
async def get_leaderboard_week(request: Request, difficulty: int, sudoku_registry_service: sudoku_registry_service):
  try:
    firebase_user_id = request.state.firebase_user_id
    if firebase_user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    return await sudoku_registry_service.get_leaderboard_week(difficulty, firebase_user_id)
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
  "/leaderboard/{difficulty}/month",
  response_model=SudokuLeaderboardResponse,
)
async def get_leaderboard_month(request: Request, difficulty: int, sudoku_registry_service: sudoku_registry_service):
  try:
    firebase_user_id = request.state.firebase_user_id
    if firebase_user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    return await sudoku_registry_service.get_leaderboard_month(difficulty, firebase_user_id)
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
  "/leaderboard/{difficulty}/alltime",
  response_model=SudokuLeaderboardResponse,
)
async def get_leaderboard_all_time(request: Request, difficulty: int, sudoku_registry_service: sudoku_registry_service):
  try:
    firebase_user_id = request.state.firebase_user_id
    if firebase_user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    return await sudoku_registry_service.get_leaderboard_all_time(difficulty, firebase_user_id)
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
  "/submit",
  response_model=SubmitSudokuResponse,
)
async def submit_sudoku(request: Request, submit_sudoku_request: SubmitSudokuRequest, sudoku_registry_service: sudoku_registry_service):
  try:
    firebase_user_id = request.state.firebase_user_id
    if firebase_user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    sudoku_id = submit_sudoku_request.puzzle_id
    solving_time = submit_sudoku_request.solving_time
    is_applicable = submit_sudoku_request.is_applicable
    user_solution = submit_sudoku_request.user_solution
    return sudoku_registry_service.submit_sudoku(firebase_user_id, sudoku_id, solving_time, is_applicable, user_solution)
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
