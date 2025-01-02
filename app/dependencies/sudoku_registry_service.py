from fastapi import Depends
from typing import Annotated

from app.services.SudokuRegistryService import get_sudoku_registry_service, SudokuRegistryService


sudoku_registry_service = Annotated[SudokuRegistryService, Depends(get_sudoku_registry_service)]
