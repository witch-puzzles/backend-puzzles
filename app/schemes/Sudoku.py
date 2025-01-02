from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetSudokuResponse:
  puzzle_id: UUID
  puzzle_data: str
  difficulty: int

@dataclass
class ValidateSudokuResponse:
  is_correct: bool
