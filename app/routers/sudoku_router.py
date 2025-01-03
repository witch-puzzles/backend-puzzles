from fastapi import APIRouter, HTTPException, status, Request
import traceback

from app.schemes.Sudoku import (
  GetSudokuResponse,
  ValidateSudokuResponse,
)
from app.entities import Sudoku
from app.dependencies.sudoku_service import sudoku_service


router = APIRouter(
  prefix="/v1/sudoku",
  tags=["sudoku"],
  responses={404: {"description": "Not found"}},
)

@router.get(
  "/get/random/{difficulty}",
  response_model=GetSudokuResponse,
)
async def get_random_sudoku_by_difficulty(difficulty: int, sudoku_service: sudoku_service):
  try:
    puzzle: Sudoku = sudoku_service.get_random_sudoku_by_difficulty(difficulty)
    return GetSudokuResponse(
      puzzle_data=puzzle.puzzle_data,
      puzzle_id=puzzle.id,
      difficulty=difficulty,
    )
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
  "/get/{puzzle_id}",
  response_model=GetSudokuResponse,
)
async def get_sudoku_by_id(puzzle_id: str, sudoku_service: sudoku_service):
  try:
    puzzle: Sudoku = sudoku_service.get_sudoku_by_id(puzzle_id)
    return GetSudokuResponse(
      puzzle_data=puzzle.puzzle_data,
      puzzle_id=puzzle.id,
      difficulty=puzzle.difficulty,
    )
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
  "/populate/{difficulty}/{count}"
)
async def populate_sudoku(request: Request, difficulty: int, count: int, sudoku_service: sudoku_service):
  try:
    firebase_user_id = request.state.firebase_user_id
    sudoku_service.populate_sudoku_registry(difficulty, count, firebase_user_id)
    return "Success"
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
