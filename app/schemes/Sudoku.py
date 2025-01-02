from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetSudokuResponse:
  puzzle_id: UUID
  puzzle_data: str

@dataclass
class ValidateSudokuRequest:
  puzzle_id: UUID
  user_solution: str

@dataclass
class ValidateSudokuResponse:
  is_correct: bool
