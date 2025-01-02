from fastapi import APIRouter, HTTPException, status, Request
import traceback

from app.schemes.Sudoku import (
  GetSudokuResponse,
  ValidateSudokuRequest,
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
      puzzle_id=puzzle.id
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
      puzzle_id=puzzle.id
    )
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
  "/populate/{difficulty}/{count}"
)
async def populate_sudoku(difficulty: int, count: int, sudoku_service: sudoku_service):
  try:
    sudoku_service.populate_sudoku_registry(difficulty, count)
    return "Success"
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
  "/validate",
  response_model=ValidateSudokuResponse,
)
async def validate_sudoku(validate_sudoku_request: ValidateSudokuRequest, sudoku_service: sudoku_service):
  try:
    is_correct = sudoku_service.validate_sudoku(validate_sudoku_request.puzzle_id, validate_sudoku_request.user_solution)
    return ValidateSudokuResponse(
      is_correct=is_correct,
    )
  except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
