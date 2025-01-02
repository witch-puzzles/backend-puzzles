from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class SudokuLeaderboardElement:
  user_name: str
  rank: int
  solving_time: float

@dataclass
class SudokuLeaderboardResponse:
  leaderboard: list[SudokuLeaderboardElement]
  user_rank: int
  user_solving_time: float

@dataclass
class SubmitSudokuRequest:
  puzzle_id: UUID
  user_solution: str
  solving_time: float
  is_applicable: bool

@dataclass
class SubmitSudokuResponse:
  is_correct: bool
  message: str
