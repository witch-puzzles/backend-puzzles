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
async def get_leaderboard_today(difficulty: int, sudoku_registry_service: sudoku_registry_service):
  try:
    return await sudoku_registry_service.get_leaderboard_today(difficulty)
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
  "/leaderboard/{difficulty}/week",
  response_model=SudokuLeaderboardResponse,
)
async def get_leaderboard_week(difficulty: int, sudoku_registry_service: sudoku_registry_service):
  try:
    return await sudoku_registry_service.get_leaderboard_week(difficulty)
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
  "/leaderboard/{difficulty}/month",
  response_model=SudokuLeaderboardResponse,
)
async def get_leaderboard_month(difficulty: int, sudoku_registry_service: sudoku_registry_service):
  try:
    return await sudoku_registry_service.get_leaderboard_month(difficulty)
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
  "/leaderboard/{difficulty}/alltime",
  response_model=SudokuLeaderboardResponse,
)
async def get_leaderboard_all_time(difficulty: int, sudoku_registry_service: sudoku_registry_service):
  try:
    return await sudoku_registry_service.get_leaderboard_all_time(difficulty)
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
  "/submit",
  response_model=SubmitSudokuResponse,
)
async def submit_sudoku(request: Request, submit_sudoku_request: SubmitSudokuRequest, sudoku_registry_service: sudoku_registry_service):
  try:
    user_id = request.state.user_id
    sudoku_id = submit_sudoku_request.puzzle_id
    solving_time = submit_sudoku_request.solving_time
    sudoku_registry_service.submit_sudoku(user_id, sudoku_id, solving_time)
    return SubmitSudokuResponse(message="Sudoku submitted successfully")
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
