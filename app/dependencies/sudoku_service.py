from fastapi import Depends
from typing import Annotated

from app.services.SudokuService import get_sudoku_service, SudokuService


sudoku_service = Annotated[SudokuService, Depends(get_sudoku_service)]
